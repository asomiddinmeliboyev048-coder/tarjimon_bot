# 🚀 HOW TO RUN YOUR BOT

## ✅ Everything is Ready!

Your Telegram bot has been **completely rebuilt** and is ready to run locally.

---

## 📋 REQUIREMENTS CHECK

Before running, verify you have:

- ✅ **Python 3.12** installed
- ✅ **BOT_TOKEN** from @BotFather
- ✅ **ADMIN_ID** (your Telegram user ID)
- ✅ **CHANNEL_ID** (your Telegram channel)
- ✅ All files created (verified ✓)
- ✅ Dependencies installed (verified ✓)
- ✅ All imports working (verified ✓)

---

## 🎯 QUICK START (3 Steps)

### Step 1: Configure
Edit `.env` file:

```
BOT_TOKEN=1234567:ABCdefGHIjklmNOPqrsTUVwxyz
ADMIN_ID=123456789
CHANNEL_ID=-1001234567890
DATABASE_PATH=bot.db
```

### Step 2: Install
```bash
cd bot
pip install -r requirements.txt
```

### Step 3: Run
```bash
python main.py
```

Expected output:
```
INFO:root:Database initialized
INFO:root:Bot initialized with all handlers
INFO:root:Starting polling...
```

---

## 💬 TEST THE BOT

### Test in Telegram:

1. Open Telegram
2. Find your bot (search for bot username)
3. Send `/start`
4. Bot will check subscription
5. Select a language
6. Send Uzbek text
7. Bot will translate and send voice

---

## ✅ COMPLETE FILE LIST

```
bot/
├── main.py                    ✓ Entry point (polling)
├── config.py                  ✓ Configuration
├── database.py                ✓ SQLite database
├── requirements.txt           ✓ Dependencies
├── README.md                  ✓ Full documentation
├── SETUP.md                   ✓ Setup guide
├── COMPLETION_SUMMARY.md      ✓ What was done
├── RUN.md                     ✓ How to run (this file)
├── .env                       ✓ Your configuration
├── .env.example               ✓ Config template
├── bot.db                     ✓ Database (auto-created)
│
├── handlers/
│   ├── __init__.py            ✓
│   ├── start.py               ✓ /start command
│   ├── translate.py           ✓ Translation
│   └── admin.py               ✓ Admin panel
│
├── keyboards/
│   ├── __init__.py            ✓
│   └── inline.py              ✓ Buttons
│
└── utils/
    ├── __init__.py            ✓
    ├── subscription.py        ✓ Channel check
    ├── translator.py          ✓ Translation
    └── voice.py               ✓ Voice synthesis
```

---

## 🔍 WHAT EACH FILE DOES

| File | Purpose |
|------|---------|
| `main.py` | Starts bot with polling |
| `config.py` | Bot settings & languages |
| `database.py` | SQLite user tracking |
| `handlers/start.py` | /start command handler |
| `handlers/translate.py` | Translation handler |
| `handlers/admin.py` | Admin panel |
| `utils/subscription.py` | Channel verification |
| `utils/translator.py` | deep-translator wrapper |
| `utils/voice.py` | edge-tts wrapper |
| `keyboards/inline.py` | All buttons |
| `.env` | Your secrets |

---

## 🛠️ INSTALLATION

### Option 1: Fresh Install
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using Existing Environment
```bash
# Just install requirements
pip install -r requirements.txt
```

---

## ▶️ RUNNING THE BOT

### Command
```bash
python main.py
```

### Expected Output
```
INFO:root:Database initialized
INFO:root:Bot initialized with all handlers
INFO:root:Starting polling...
```

### What This Means
- ✅ Database created/loaded
- ✅ Bot connected to Telegram
- ✅ All handlers loaded
- ✅ Polling started (listening for messages)

### The Bot is Now Running
- Ready to receive `/start` commands
- Will check channel subscriptions
- Will translate Uzbek text
- Will generate voice messages
- Admin can use `/admin` command

---

## ⏹️ STOPPING THE BOT

Press: `Ctrl + C`

The bot will:
1. Stop listening for messages
2. Close database connection
3. Clean up gracefully
4. Exit

---

## 🧪 TESTING WORKFLOW

### Test Subscription Check
1. Send `/start` as non-subscribed user
2. Should see subscription prompt

### Test Translation
1. Select a language
2. Send Uzbek text: "salom"
3. Should see translation
4. Should hear voice

### Test Admin Panel
1. As ADMIN_ID user, send `/admin`
2. Should see statistics buttons
3. Click buttons to see stats

---

## 🐛 DEBUGGING

### If Bot Doesn't Start

**Check 1: Python Version**
```bash
python --version
# Should be 3.10+
```

**Check 2: Dependencies**
```bash
pip list
# Should have: aiogram, deep-translator, edge-tts, python-dotenv
```

**Check 3: .env File**
```bash
# Make sure .env exists and has:
# BOT_TOKEN=xxx
# ADMIN_ID=xxx
# CHANNEL_ID=xxx
```

**Check 4: Bot Token**
- Make sure BOT_TOKEN is from @BotFather
- Not from any other source
- Starts with bot's user ID

### If Bot Doesn't Respond

**Check 1: Internet Connection**
```bash
ping google.com
# Should respond
```

**Check 2: Bot Token Valid**
- Try in another bot framework
- Or create new bot with @BotFather

**Check 3: Polling Running**
- Terminal should show: "Starting polling..."
- No error messages

### If Translation Fails

**Check 1: Text Not Empty**
- Send non-empty Uzbek text

**Check 2: Language Selected**
- Select language first

**Check 3: Internet Connection**
- deep-translator needs internet

### If Voice Doesn't Generate

**Check 1: Internet Connection**
- edge-tts needs connection

**Check 2: Text Length**
- Very long text might fail
- Try shorter text

**Check 3: Language Support**
- Should be one of 5 supported languages

---

## 📊 DATABASE

Database file: `bot.db`

**Auto-Created on First Run**
- Stores users
- Stores translation logs
- No manual setup needed

**View Database (Advanced)**
```bash
# Using sqlite3 command line
sqlite3 bot.db

# Then:
SELECT * FROM users;
SELECT * FROM logs;
```

---

## 📝 LOGS & DEBUGGING

### Console Output
Bot logs to console (INFO level):
- Database initialization
- Bot connection
- Polling status
- Errors (if any)

### See More Details
Edit main.py to change log level:
```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

---

## ⚡ PERFORMANCE TIPS

1. **Keep Bot Running 24/7**
   - Use screen/tmux for long-running
   - Or deploy to server

2. **Monitor Usage**
   - Check `/admin` for stats
   - Database grows with translations

3. **Database Maintenance**
   - Backup `bot.db` regularly
   - It's just an SQLite file

---

## 🔒 SECURITY

### .env File
- ✅ Never commit to git
- ✅ Keep BOT_TOKEN secret
- ✅ Different .env for each server

### Admin Access
- ✅ Only ADMIN_ID user can see /admin
- ✅ Only admin can see user statistics

### Channel Subscription
- ✅ Enforced on every interaction
- ✅ Bot re-checks every time

---

## 📞 COMMANDS

| Command | Function | Who |
|---------|----------|-----|
| `/start` | Start bot / Select language | Anyone |
| `/admin` | Admin panel | Admin only |

---

## 🎯 NEXT STEPS

1. ✅ Configure `.env` file
2. ✅ Run `python main.py`
3. ✅ Test `/start` command
4. ✅ Test subscription
5. ✅ Test translation
6. ✅ Test voice
7. ✅ Check `/admin` panel

---

## ❓ FAQ

**Q: Can I run bot on Windows?**
A: Yes! Python works on Windows. Just use `python main.py`

**Q: Can I run bot 24/7?**
A: Yes, but need:
- VPS or server
- Or screen/tmux on local PC
- Or use systemd service

**Q: Can I modify the bot?**
A: Yes! All code is modular:
- Edit messages in handlers
- Add new commands
- Customize keyboards

**Q: Where are settings?**
A: In `config.py` - all configuration in one file

**Q: Is it production ready?**
A: Yes! Full error handling and async design

---

## ✨ YOUR BOT IS READY!

```bash
cd bot
python main.py
```

That's it! Your bot is running! 🎉

For questions, check:
- README.md - Full documentation
- SETUP.md - Setup guide
- COMPLETION_SUMMARY.md - What was implemented
