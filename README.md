# Telegram Meme Bot 🤖

A Python Telegram bot that fetches random memes from Reddit without requiring a Reddit API key. The bot uses public Reddit JSON endpoints to get memes from popular meme subreddits.

## Features ✨

- 🎭 Fetches random memes from multiple subreddits (r/memes, r/dankmemes, r/wholesomememes)
- 📱 Sends memes as photos or videos with captions
- 🔄 Randomly selects subreddits and memes for variety
- 🛡️ Graceful error handling for network issues
- 🚀 No Reddit API key required - uses public endpoints
- 📊 Console logging for monitoring

## Commands 📋

- `/start` - Start the bot and get welcome message
- `/meme` - Get a random meme from Reddit
- `/help` - Show help message with available commands

## Setup Instructions 🛠️

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (you'll need this later)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable

Set your bot token as an environment variable:

```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

Or on Windows:
```cmd
set TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 4. Run the Bot

```bash
python telegram_meme_bot.py
```

## How It Works 🔧

1. **Reddit Integration**: The bot fetches memes from Reddit's public JSON endpoints:
   - `https://www.reddit.com/r/memes/hot.json?limit=50`
   - `https://www.reddit.com/r/dankmemes/hot.json?limit=50`
   - `https://www.reddit.com/r/wholesomememes/hot.json?limit=50`

2. **Media Filtering**: Only posts with valid image/video URLs are included:
   - Common image formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
   - Common video formats: `.mp4`, `.gifv`, `.webm`
   - Popular hosting sites: Imgur, Reddit, Giphy, Tenor

3. **Random Selection**: When `/meme` is called:
   - Randomly picks one of the three subreddits
   - Randomly selects a meme from the first 50 hot posts
   - Sends the meme with its title as caption

## Error Handling 🛡️

The bot handles various error scenarios:
- Network timeouts and connection errors
- Invalid JSON responses from Reddit
- Missing or invalid media URLs
- Telegram API errors

## Dependencies 📦

- `python-telegram-bot==20.3` - Telegram Bot API wrapper (async version)
- `requests==2.31.0` - HTTP library for fetching Reddit data

## Security Notes 🔒

- The bot uses a custom User-Agent to avoid being blocked by Reddit
- No Reddit API key is required or stored
- Bot token should be kept secure and not shared publicly

## Troubleshooting 🔍

### Bot not responding
- Check if the bot token is correctly set
- Verify the bot is running without errors
- Ensure you've started a conversation with the bot

### No memes being sent
- Check internet connectivity
- Reddit might be temporarily unavailable
- Some subreddits might have rate limiting

### Permission errors
- Make sure the bot has permission to send photos
- Check if the bot is blocked or restricted

## Contributing 🤝

Feel free to contribute by:
- Adding more subreddits
- Improving error handling
- Adding new features
- Fixing bugs

## License 📄

This project is open source and available under the MIT License.