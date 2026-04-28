# 🚀 SETUP GUIDE - Tarjimon Telegram Bot

## ✅ What Has Been Done

Your Telegram bot has been **completely rebuilt** with:

- ✅ **Polling-based architecture** (no webhook)
- ✅ **Forced channel subscription** check on every interaction
- ✅ **5 languages** with translation (English, Russian, Turkish, Korean, Arabic)
- ✅ **Automatic voice synthesis** with edge-tts (male neural voices)
- ✅ **SQLite database** for user tracking and translation logs
- ✅ **Admin panel** with `/admin` command
- ✅ **Production-ready code structure**
- ✅ **Fast async processing**
- ✅ **Error handling** on all operations

## 📋 Quick Start

### Step 1: Configure Environment

Edit `.env` file in the `bot/` folder:

```
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_ID=your_telegram_user_id
CHANNEL_ID=-1001234567890
DATABASE_PATH=bot.db
```

### Step 2: Get Your Values

**BOT_TOKEN:**
- Message @BotFather on Telegram
- Create new bot with `/newbot`
- Copy the token

**ADMIN_ID:**
- Message @userinfobot on Telegram
- It will show your user ID

**CHANNEL_ID:**
- Create a Telegram channel
- Add your bot as admin
- Send a test message
- Forward it to @userinfobot
- Copy the negative channel ID (starts with -100)

### Step 3: Install Dependencies

```bash
cd bot
pip install -r requirements.txt
```

### Step 4: Run the Bot

```bash
python main.py
```

You should see:
```
INFO:root:Database initialized
INFO:root:Bot initialized with all handlers
INFO:root:Starting polling...
```

The bot is now **running locally** and listening for messages!

## 📁 Project Structure

```
bot/
├── config.py              # Configuration & languages
├── main.py               # Entry point (polling)
├── database.py           # SQLite database
├── requirements.txt      # Dependencies
├── .env                  # Your secrets (GIT IGNORE!)
├── README.md             # Full documentation
├── handlers/
│   ├── start.py         # /start command & subscription
│   ├── translate.py     # Translation & voice generation
│   └── admin.py         # Admin panel
├── keyboards/
│   └── inline.py        # Inline button keyboards
└── utils/
    ├── subscription.py  # Channel check
    ├── translator.py    # Deep-translator wrapper
    └── voice.py         # Edge-tts wrapper
```

## 🔄 Bot Workflow

### User Journey

1. **User sends /start**
   - Bot checks if subscribed to channel
   - If not → Shows subscription buttons
   - If yes → Shows language selection

2. **User selects language**
   - Bot saves choice to database
   - Shows instruction for that language

3. **User sends Uzbek text**
   - Bot automatically translates
   - Sends translation in message
   - Generates and sends voice audio

4. **User can change language**
   - Button to switch languages anytime
   - Translation continues with new language

### Admin Access

Command: `/admin`

Only accessible to ADMIN_ID user. Shows:
- 📊 Statistics (total users, translations today)
- 👥 User count
- 🌍 Language breakdown
- 📈 Daily translations
- 🔁 Total translations count

## 🗣️ Supported Languages & Voices

| Language | Emoji | Voice Type |
|----------|-------|-----------|
| English | 🇬🇧 | en-US-GuyNeural |
| Russian | 🇷🇺 | ru-RU-DmitryNeural |
| Turkish | 🇹🇷 | tr-TR-AhmetNeural |
| Korean | 🇰🇷 | ko-KR-InJoonNeural |
| Arabic | 🇸🇦 | ar-SA-HamedNeural |

All voices are **male, natural, and realistic**.

## 📊 Database Schema

### users table
```sql
user_id              (INTEGER PRIMARY KEY)
username             (TEXT)
first_name           (TEXT)
selected_language    (TEXT)
translation_count    (INTEGER)
joined_at            (TEXT)
last_active          (TEXT)
```

### logs table
```sql
id                   (INTEGER PRIMARY KEY)
user_id              (INTEGER FOREIGN KEY)
source_text          (TEXT) - Original Uzbek text
translated_text      (TEXT) - Translated text
target_language      (TEXT) - Language code
created_at           (TEXT) - Timestamp
```

## ⚙️ Configuration

All settings in `config.py`:

```python
BOT_TOKEN              # From @BotFather
ADMIN_ID               # Your Telegram ID
CHANNEL_ID             # Your channel ID
DATABASE_PATH          # SQLite DB file
LANGUAGES              # Language definitions
LANG_INSTRUCTIONS      # Instruction messages
```

## 🔐 Security Features

✅ **Subscription enforcement** - Users must join channel
✅ **Admin bypass** - Admin bypasses subscription check
✅ **Error safety** - Bot never crashes, always responds
✅ **Rate limiting** - Handles Telegram limits gracefully
✅ **Input validation** - Cleans user text before processing

## ⚡ Performance

- **Async processing** - All operations non-blocking
- **Fast translation** - deep-translator with fallback
- **Voice generation** - edge-tts produces instant audio
- **Database optimization** - Indexed queries
- **Cleanup** - Removes temporary files automatically

## 📝 Important Notes

### .env File
- **DO NOT commit .env to git** - Contains bot token
- Keep .env.example as template for others

### Database
- `bot.db` file created automatically on first run
- SQLite stores users and translations locally
- Portable - can move database file

### Polling vs Webhook
- **Current: Polling** - Bot asks Telegram for updates
- Advantage: Works locally, no server needed
- Disadvantage: Slightly slower than webhook

### Logs
- Bot logs to console (INFO level)
- Structured messages show bot status
- Errors are immediately visible

## 🐛 Troubleshooting

**Bot not responding:**
- Check BOT_TOKEN is correct
- Make sure polling is running
- Check internet connection

**Subscription not working:**
- Verify CHANNEL_ID format
- Make sure bot is admin in channel
- Confirm user is in channel

**Voice not generating:**
- Check internet (edge-tts needs connection)
- Try with different language
- Text might be too long

**Database errors:**
- Delete bot.db and restart (fresh database)
- Ensure folder is writable

**Import errors:**
- Run: `pip install -r requirements.txt`
- Verify all packages installed: `pip list`

## 🎯 Next Steps

1. ✅ Set up `.env` with your values
2. ✅ Run `python main.py`
3. ✅ Test with `/start` command
4. ✅ Verify subscription check works
5. ✅ Test translation and voice
6. ✅ Check `/admin` panel as admin

## 📞 Commands

| Command | Who | Function |
|---------|-----|----------|
| `/start` | Anyone | Start bot, check subscription |
| `/admin` | Admin only | Open admin panel |

## 🎨 Bot Messages

All user-facing messages are in Uzbek:

- `❌ Botdan foydalanish uchun kanalga obuna bo'ling.` - Subscribe prompt
- `✅ Obuna tasdiqlandi!` - Subscription confirmed
- `🌍 Tarjima tilini tanlang:` - Language selection
- `{emoji} Tarjima:` - Translation header

Messages can be customized in handler files.

## ✨ Features Implemented

✅ Channel subscription enforcement
✅ Re-check subscription every time
✅ 5 language support
✅ Instant translation
✅ Automatic voice synthesis
✅ Male neural voices
✅ Admin statistics
✅ User database
✅ Translation logging
✅ Error handling
✅ Polling-based (local)
✅ Production structure

---

**Your bot is ready to use! 🎉**

Start it with:
```bash
python main.py
```
