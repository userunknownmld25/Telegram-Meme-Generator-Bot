#!/usr/bin/env python3
"""
Demo script for the Telegram Meme Bot
This script demonstrates the bot's functionality without requiring a real Telegram token.
"""

import sys
import os

# Add the current directory to Python path to import the bot module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_meme_bot import MemeFetcher

def demo_meme_fetching():
    """Demonstrate the meme fetching functionality."""
    print("🤖 Telegram Meme Bot Demo")
    print("=" * 50)
    print()
    
    # Create meme fetcher instance
    fetcher = MemeFetcher()
    
    print("🎭 Fetching 5 random memes to demonstrate functionality...")
    print()
    
    for i in range(5):
        print(f"📱 Meme #{i+1}:")
        
        try:
            # Get a random meme
            meme = fetcher.get_random_meme()
            
            if meme:
                print(f"   📝 Title: {meme['title']}")
                print(f"   🔗 URL: {meme['url']}")
                
                if meme.get('source') == 'Giphy':
                    print(f"   📍 Source: {meme['source']}")
                elif meme.get('source') == 'Fallback':
                    print(f"   📍 Source: Classic Memes")
                else:
                    print(f"   📍 Source: r/{meme['subreddit']}")
                
                print()
            else:
                print("   ❌ Failed to fetch meme")
                print()
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("🎉 Demo completed!")
    print()
    print("📋 Bot Features Demonstrated:")
    print("   ✅ Multiple Reddit subreddit support")
    print("   ✅ Giphy fallback when Reddit is unavailable")
    print("   ✅ Hardcoded fallback memes for reliability")
    print("   ✅ Random selection from multiple sources")
    print("   ✅ Error handling and graceful degradation")
    print()
    print("🚀 To run the actual Telegram bot:")
    print("   1. Create a bot with @BotFather")
    print("   2. Set your token: export TELEGRAM_BOT_TOKEN='your_token'")
    print("   3. Run: python telegram_meme_bot.py")

if __name__ == '__main__':
    demo_meme_fetching()