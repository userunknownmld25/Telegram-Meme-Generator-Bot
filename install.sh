#!/bin/bash

echo "🤖 Telegram Meme Bot Installer"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check your internet connection."
    exit 1
fi

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo ""
    echo "⚠️  TELEGRAM_BOT_TOKEN environment variable is not set."
    echo ""
    echo "To set it up:"
    echo "1. Create a bot with @BotFather on Telegram"
    echo "2. Copy your bot token"
    echo "3. Run: export TELEGRAM_BOT_TOKEN='your_token_here'"
    echo ""
    echo "Or add it to your ~/.bashrc or ~/.zshrc file for persistence:"
    echo "echo 'export TELEGRAM_BOT_TOKEN=\"your_token_here\"' >> ~/.bashrc"
    echo ""
else
    echo "✅ TELEGRAM_BOT_TOKEN is set"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To run the bot:"
echo "python3 telegram_meme_bot.py"
echo ""
echo "For help, see README.md"