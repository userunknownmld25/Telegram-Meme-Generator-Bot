# Telegram Meme Bot - Quick Setup Guide 🚀

## Files Overview

- `telegram_meme_bot.py` - Main bot file with all functionality
- `requirements.txt` - Python dependencies
- `install.sh` - Automated installation script
- `test_reddit_fetch.py` - Test script for meme fetching
- `demo_bot.py` - Demo script to see bot functionality
- `README.md` - Comprehensive documentation
- `SETUP.md` - This quick setup guide

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
# Run the automated installer
./install.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test the Bot (Optional)
```bash
# Test meme fetching functionality
python demo_bot.py

# Or run the test script
python test_reddit_fetch.py
```

### 3. Set Up Telegram Bot
```bash
# 1. Create a bot with @BotFather on Telegram
# 2. Copy your bot token
# 3. Set the environment variable:
export TELEGRAM_BOT_TOKEN='your_bot_token_here'

# 4. Run the bot:
python telegram_meme_bot.py
```

## Bot Commands

- `/start` - Welcome message
- `/meme` - Get a random meme
- `/help` - Show help

## Features

✅ **Multiple Sources**: Reddit (r/memes, r/dankmemes, r/wholesomememes)  
✅ **Fallback System**: Giphy API when Reddit is unavailable  
✅ **Reliability**: Hardcoded classic memes as final fallback  
✅ **No API Keys**: Uses public endpoints only  
✅ **Error Handling**: Graceful degradation when services are down  
✅ **Async Support**: Uses python-telegram-bot v20+  

## Troubleshooting

**Bot not responding?**
- Check if `TELEGRAM_BOT_TOKEN` is set correctly
- Make sure you've started a conversation with your bot

**No memes being sent?**
- The bot will use fallback sources automatically
- Check console logs for error messages

**Installation issues?**
- Make sure Python 3.7+ is installed
- Use the virtual environment: `source venv/bin/activate`

## Demo

Run `python demo_bot.py` to see the bot fetch memes from different sources without needing a Telegram token.

## Support

The bot is designed to be reliable even when Reddit is unavailable. It will automatically fall back to Giphy and then to classic memes if needed.