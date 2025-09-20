#!/usr/bin/env python3
"""
Test script for meme fetching functionality.
This script tests the MemeFetcher class without requiring a Telegram bot token.
"""

import sys
import os

# Add the current directory to Python path to import the bot module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_meme_bot import MemeFetcher

def test_meme_fetching():
    """Test the meme fetching functionality."""
    print("🧪 Testing Meme Fetching...")
    print("=" * 40)
    
    # Create meme fetcher instance
    fetcher = MemeFetcher()
    
    # Test fetching from each subreddit
    subreddits = ['memes', 'dankmemes', 'wholesomememes']
    
    for subreddit in subreddits:
        print(f"\n📱 Testing r/{subreddit}...")
        
        try:
            # Fetch memes from subreddit
            memes = fetcher._get_memes_from_subreddit(subreddit, limit=10)
            
            if memes:
                print(f"✅ Found {len(memes)} valid memes in r/{subreddit}")
                
                # Show first meme details
                first_meme = memes[0]
                print(f"   📝 Title: {first_meme['title'][:50]}...")
                print(f"   🔗 URL: {first_meme['url']}")
                print(f"   📍 Source: r/{first_meme['subreddit']}")
            else:
                print(f"❌ No valid memes found in r/{subreddit}")
                
        except Exception as e:
            print(f"❌ Error testing r/{subreddit}: {e}")
    
    # Test Giphy fallback
    print(f"\n🎬 Testing Giphy fallback...")
    try:
        giphy_meme = fetcher._try_giphy_meme()
        
        if giphy_meme:
            print("✅ Giphy meme fetched successfully!")
            print(f"   📝 Title: {giphy_meme['title']}")
            print(f"   🔗 URL: {giphy_meme['url']}")
            print(f"   📍 Source: {giphy_meme['source']}")
        else:
            print("❌ Failed to fetch Giphy meme")
            
    except Exception as e:
        print(f"❌ Error fetching Giphy meme: {e}")
    
    # Test random meme selection (with fallback)
    print(f"\n🎲 Testing random meme selection with fallback...")
    try:
        random_meme = fetcher.get_random_meme()
        
        if random_meme:
            print("✅ Random meme fetched successfully!")
            print(f"   📝 Title: {random_meme['title']}")
            print(f"   🔗 URL: {random_meme['url']}")
            if random_meme.get('source') == 'Giphy':
                print(f"   📍 Source: {random_meme['source']}")
            else:
                print(f"   📍 Source: r/{random_meme['subreddit']}")
        else:
            print("❌ Failed to fetch random meme")
            
    except Exception as e:
        print(f"❌ Error fetching random meme: {e}")
    
    print(f"\n🎉 Test completed!")

if __name__ == '__main__':
    test_meme_fetching()