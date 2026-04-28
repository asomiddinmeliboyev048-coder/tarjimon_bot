# Tarjimon Bot - Uzbek Translator with Voice

A Telegram bot that translates Uzbek text to English, Russian, Turkish, Korean, and Arabic with automatic voice synthesis.

## Features

✅ **Forced Subscription** - Users must subscribe to channel first  
✅ **Re-check Subscription** - Checks every time user opens bot  
✅ **5 Languages** - English, Russian, Turkish, Korean, Arabic  
✅ **Instant Translation** - Uses deep-translator for fast results  
✅ **Automatic Voice** - Generates natural male voice with edge-tts  
✅ **Admin Panel** - Statistics, user count, language stats  
✅ **Database** - SQLite for user tracking and logs  
✅ **Polling** - Local polling (no webhook needed)  
✅ **Production Ready** - Proper structure and error handling  

## Setup

### 1. Install Python 3.12

Make sure you have Python 3.12 installed.

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=123456789
CHANNEL_ID=-1001234567890
DATABASE_PATH=bot.db
```

### 5. Get Your Values

- **BOT_TOKEN**: Create bot with @BotFather on Telegram
- **ADMIN_ID**: Your Telegram user ID (message @userinfobot)
- **CHANNEL_ID**: Your channel ID
  - Make bot an admin in your channel
  - Send a message
  - Forward it to @userinfobot to get channel ID

### 6. Run Locally

```bash
python main.py
```

You should see:
```
INFO:root:Database initialized
INFO:root:Bot initialized with all handlers
INFO:root:Starting polling...
```

## Bot Workflow

### 1. User Starts Bot
```
/start
```

### 2. Subscription Check
Bot checks if user is subscribed to channel. If not:

```
❌ Botdan foydalanish uchun kanalga obuna bo'ling.

[📢 Kanalga qo'shilish]
[✅ Tekshirish]
```

User clicks "✅ Tekshirish" to re-check.

### 3. Language Selection
After subscription verified:

```
🌍 Tarjima tilini tanlang:

[🇬🇧 English]
[🇷🇺 Russian]
[🇹🇷 Turkish]
[🇰🇷 Korean]
[🇸🇦 Arabic]
```

### 4. Language Instruction
Example if Russian selected:

```
🇷🇺 Siz o'zbek tilida matn yozing.
Men uni rus tiliga tarjima qilaman.
```

### 5. User Sends Text
User writes Uzbek text:

```
salom qalaysan
```

### 6. Bot Responds
Translation sent automatically:

```
🇷🇺 Tarjima:
Привет, как дела?
```

Then bot sends voice message with pronunciation.

### 7. Change Language
Click button in any translation to change language.

## Admin Panel

Only admin can use:

```
/admin
```

Shows:

```
📊 Admin panel:

[📊 Statistika]
[👥 Foydalanuvchilar]
[🌍 Tillar]
[📈 Kunlik]
[🔁 Jami tarjima]
```

## Database Schema

### users table
- user_id (INTEGER PRIMARY KEY)
- username (TEXT)
- first_name (TEXT)
- selected_language (TEXT)
- translation_count (INTEGER)
- joined_at (TEXT)
- last_active (TEXT)

### logs table
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER)
- source_text (TEXT)
- translated_text (TEXT)
- target_language (TEXT)
- created_at (TEXT)

## Voices Used

Each language uses professional male neural voice:

- 🇬🇧 English: en-US-GuyNeural
- 🇷🇺 Russian: ru-RU-DmitryNeural
- 🇹🇷 Turkish: tr-TR-AhmetNeural
- 🇰🇷 Korean: ko-KR-InJoonNeural
- 🇸🇦 Arabic: ar-SA-HamedNeural

## Project Structure

```
bot/
├── config.py           # Configuration
├── main.py            # Bot entry point
├── database.py        # SQLite database
├── requirements.txt   # Dependencies
├── .env               # Environment variables
├── .env.example       # Example config
├── handlers/
│   ├── __init__.py
│   ├── start.py       # /start command
│   ├── translate.py   # Translation handler
│   └── admin.py       # Admin panel
├── keyboards/
│   ├── __init__.py
│   └── inline.py      # Inline keyboards
└── utils/
    ├── __init__.py
    ├── subscription.py # Channel subscription check
    ├── translator.py   # Translation logic
    └── voice.py        # Voice synthesis
```

## Error Handling

Bot handles:

- ❌ Translation errors → Shows "Xatolik yuz berdi"
- ❌ Voice generation errors → Sends translation without voice
- ❌ Telegram errors → Retries or fails gracefully
- ❌ Missing subscription → Prompts to subscribe

## Speed & Performance

- ⚡ Async processing for all operations
- ⚡ Fast deep-translator with fallback retries
- ⚡ edge-tts for instant voice generation
- ⚡ Cleanup of temporary files
- ⚡ Optimized for many concurrent users

## Troubleshooting

### Bot not responding
- Check BOT_TOKEN is valid
- Make sure polling is running
- Check internet connection

### Subscription not working
- Verify CHANNEL_ID is correct
- Make sure bot is admin in channel
- Check user is in correct channel

### Voice not generating
- Check internet (edge-tts needs connection)
- Make sure text is not empty
- Try with different language

### Database errors
- Delete `bot.db` and restart
- Make sure folder is writable

## License

Made for Tarjimon translation bot.
