import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter

from config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH
from database import Database
from handlers import start, translate, admin
from utils.logger import logger, log_error

# Ensure required directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("cache/voice", exist_ok=True)


async def main():
    """Main bot entry point"""

    # Initialize database
    try:
        Database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return

    # Check configuration
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured! Please set BOT_TOKEN in .env file")
        return

    if not WEBHOOK_HOST:
        logger.error("WEBHOOK_HOST not configured! Please set WEBHOOK_HOST in environment variables.")
        return

    webhook_url = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    port = int(os.getenv("PORT", 10000))

    # Initialize bot and dispatcher
    try:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        dp = Dispatcher()

        dp.include_router(start.router)
        dp.include_router(translate.router)
        dp.include_router(admin.router)

        logger.info("Bot initialized with all handlers")
    except Exception as e:
        logger.error(f"Bot initialization failed: {e}")
        return

    async def webhook_handler(request: web.Request) -> web.Response:
        try:
            update = await request.json()
        except Exception as e:
            logger.error(f"Invalid webhook payload: {e}")
            return web.Response(status=400)

        try:
            await dp.feed_webhook_update(bot, update)
        except Exception as e:
            logger.error(f"Failed to process webhook update: {e}")
            return web.Response(status=500)

        return web.Response(status=200)

    async def on_startup(app: web.Application) -> None:
        try:
            logger.info(f"Setting webhook to {webhook_url}")
            await bot.set_webhook(webhook_url)
            logger.info("Webhook set successfully")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            raise

    async def on_shutdown(app: web.Application) -> None:
        try:
            logger.info("Deleting webhook...")
            await bot.delete_webhook()
            logger.info("Webhook deleted successfully")
        except Exception as e:
            logger.error(f"Error deleting webhook: {e}")

        try:
            await bot.session.close()
            logger.info("Bot session closed")
        except Exception as e:
            logger.error(f"Error closing bot session: {e}")

    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, webhook_handler)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    try:
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        logger.info(f"Starting webhook server on port {port}")
        await site.start()

        # Keep the service running until it is stopped externally
        while True:
            await asyncio.sleep(3600)

    except TelegramRetryAfter as e:
        logger.error(f"Flood control: retry after {e.retry_after} seconds")
        await asyncio.sleep(e.retry_after)
    except TelegramNetworkError as e:
        logger.error(f"Network error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during webhook service: {e}")
        log_error(f"Webhook service error: {e}")
    finally:
        logger.info("Shutting down webhook service...")
        await runner.cleanup()
        logger.info("Webhook service stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
