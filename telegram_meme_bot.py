#!/usr/bin/env python3
"""
Telegram Meme Bot
Fetches random memes from Reddit without requiring a Reddit API key.
"""

import asyncio
import json
import random
import logging
import re
from typing import Optional, Dict, Any
from urllib.parse import urlparse

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Subreddits to fetch memes from
SUBREDDITS = ['memes', 'dankmemes', 'wholesomememes']

# User agent to avoid being blocked by Reddit
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Fallback meme URLs (popular meme images)
FALLBACK_MEMES = [
    {
        'title': 'Classic Doge Meme',
        'url': 'https://i.imgur.com/8tBcQ4A.jpg',
        'subreddit': 'classic',
        'source': 'Fallback'
    },
    {
        'title': 'Grumpy Cat',
        'url': 'https://i.imgur.com/8tBcQ4A.jpg',
        'subreddit': 'classic',
        'source': 'Fallback'
    },
    {
        'title': 'Success Kid',
        'url': 'https://i.imgur.com/8tBcQ4A.jpg',
        'subreddit': 'classic',
        'source': 'Fallback'
    },
    {
        'title': 'One Does Not Simply',
        'url': 'https://i.imgur.com/8tBcQ4A.jpg',
        'subreddit': 'classic',
        'source': 'Fallback'
    },
    {
        'title': 'Y U No',
        'url': 'https://i.imgur.com/8tBcQ4A.jpg',
        'subreddit': 'classic',
        'source': 'Fallback'
    }
]


class MemeFetcher:
    """Handles fetching memes from multiple sources."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_random_meme(self) -> Optional[Dict[str, Any]]:
        """
        Get a random meme from available sources.
        
        Returns:
            Dictionary containing meme data or None if no meme found
        """
        # Try Reddit first
        meme = self._try_reddit_meme()
        
        # If Reddit fails, try Giphy as fallback
        if not meme:
            logger.info("Reddit unavailable, trying Giphy fallback...")
            meme = self._try_giphy_meme()
        
        # If Giphy fails, use hardcoded fallback
        if not meme:
            logger.info("Giphy unavailable, using hardcoded fallback...")
            meme = self._get_fallback_meme()
        
        return meme
    
    def _try_reddit_meme(self) -> Optional[Dict[str, Any]]:
        """Try to get a meme from Reddit."""
        # Randomly select a subreddit
        subreddit = random.choice(SUBREDDITS)
        logger.info(f"Trying to fetch memes from r/{subreddit}")
        
        # Get memes from the selected subreddit
        memes = self._get_memes_from_subreddit(subreddit)
        
        if not memes:
            logger.warning(f"No valid memes found in r/{subreddit}")
            return None
        
        # Randomly select a meme
        meme = random.choice(memes)
        logger.info(f"Selected Reddit meme: {meme['title'][:50]}... from r/{subreddit}")
        
        return meme
    
    def _get_memes_from_subreddit(self, subreddit: str, limit: int = 50) -> list:
        """
        Fetch memes from a specific subreddit using multiple methods.
        
        Args:
            subreddit: Name of the subreddit
            limit: Number of posts to fetch (max 50)
            
        Returns:
            List of meme posts with image/video URLs
        """
        # Try JSON endpoint first
        memes = self._try_json_endpoint(subreddit, limit)
        
        # If JSON fails, try RSS feed
        if not memes:
            logger.info(f"JSON endpoint failed for r/{subreddit}, trying RSS feed...")
            memes = self._try_rss_feed(subreddit, limit)
        
        # If RSS fails, try alternative JSON endpoint
        if not memes:
            logger.info(f"RSS feed failed for r/{subreddit}, trying alternative JSON...")
            memes = self._try_alternative_json(subreddit, limit)
        
        return memes
    
    def _try_json_endpoint(self, subreddit: str, limit: int) -> list:
        """Try to fetch from Reddit's JSON endpoint."""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Check if post has media content
                url = post_data.get('url', '')
                title = post_data.get('title', 'No title')
                
                # Filter for image/video content
                if self._is_valid_media_url(url):
                    posts.append({
                        'title': title,
                        'url': url,
                        'subreddit': subreddit,
                        'permalink': f"https://reddit.com{post_data.get('permalink', '')}"
                    })
            
            return posts
            
        except Exception as e:
            logger.debug(f"JSON endpoint failed for r/{subreddit}: {e}")
            return []
    
    def _try_rss_feed(self, subreddit: str, limit: int) -> list:
        """Try to fetch from Reddit's RSS feed."""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot/.rss?limit={limit}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse RSS content
            content = response.text
            posts = []
            
            # Extract items from RSS
            item_pattern = r'<item>(.*?)</item>'
            items = re.findall(item_pattern, content, re.DOTALL)
            
            for item in items:
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', item)
                title = title_match.group(1) if title_match else 'No title'
                
                # Extract link
                link_match = re.search(r'<link>(.*?)</link>', item)
                link = link_match.group(1) if link_match else ''
                
                # Extract media content from description
                desc_match = re.search(r'<description>(.*?)</description>', item)
                if desc_match:
                    description = desc_match.group(1)
                    # Look for image URLs in description
                    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
                    img_matches = re.findall(img_pattern, description)
                    
                    for img_url in img_matches:
                        if self._is_valid_media_url(img_url):
                            posts.append({
                                'title': title,
                                'url': img_url,
                                'subreddit': subreddit,
                                'permalink': link
                            })
                            break  # Use first valid image per post
            
            return posts
            
        except Exception as e:
            logger.debug(f"RSS feed failed for r/{subreddit}: {e}")
            return []
    
    def _try_alternative_json(self, subreddit: str, limit: int) -> list:
        """Try alternative JSON endpoint with different parameters."""
        try:
            # Try with different sorting
            urls_to_try = [
                f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={limit}",
                f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}",
                f"https://www.reddit.com/r/{subreddit}/rising.json?limit={limit}"
            ]
            
            for url in urls_to_try:
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    posts = []
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        
                        url = post_data.get('url', '')
                        title = post_data.get('title', 'No title')
                        
                        if self._is_valid_media_url(url):
                            posts.append({
                                'title': title,
                                'url': url,
                                'subreddit': subreddit,
                                'permalink': f"https://reddit.com{post_data.get('permalink', '')}"
                            })
                    
                    if posts:
                        return posts
                        
                except Exception as e:
                    logger.debug(f"Alternative JSON failed for {url}: {e}")
                    continue
            
            return []
            
        except Exception as e:
            logger.debug(f"All alternative JSON endpoints failed for r/{subreddit}: {e}")
            return []
    
    def _try_giphy_meme(self) -> Optional[Dict[str, Any]]:
        """Try to get a meme from Giphy as fallback."""
        try:
            # Giphy trending endpoint (no API key required for basic usage)
            url = "https://api.giphy.com/v1/gifs/trending"
            params = {
                'api_key': 'dc6zaTOxFJmzC',  # Public beta key
                'limit': 50,
                'rating': 'g'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and data['data']:
                # Randomly select a gif
                gif = random.choice(data['data'])
                
                meme = {
                    'title': gif.get('title', 'Random Meme'),
                    'url': gif['images']['original']['url'],
                    'subreddit': 'giphy',
                    'permalink': gif.get('url', ''),
                    'source': 'Giphy'
                }
                
                logger.info(f"Selected Giphy meme: {meme['title'][:50]}...")
                return meme
            
            return None
            
        except Exception as e:
            logger.debug(f"Giphy fallback failed: {e}")
            return None
    
    def _get_fallback_meme(self) -> Dict[str, Any]:
        """Get a random meme from the hardcoded fallback list."""
        meme = random.choice(FALLBACK_MEMES)
        logger.info(f"Using fallback meme: {meme['title']}")
        return meme
    
    def _is_valid_media_url(self, url: str) -> bool:
        """
        Check if URL points to a valid image or video file.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL is a valid media file
        """
        if not url:
            return False
        
        # Common image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        # Common video extensions
        video_extensions = ['.mp4', '.gifv', '.webm']
        
        url_lower = url.lower()
        
        # Check for image extensions
        if any(ext in url_lower for ext in image_extensions):
            return True
        
        # Check for video extensions
        if any(ext in url_lower for ext in video_extensions):
            return True
        
        # Check for common image hosting domains
        image_domains = [
            'imgur.com', 'i.imgur.com', 'redd.it', 'i.redd.it',
            'media.giphy.com', 'giphy.com', 'tenor.com', 'gfycat.com',
            'v.redd.it', 'preview.redd.it'
        ]
        
        if any(domain in url_lower for domain in image_domains):
            return True
        
        return False


# Global meme fetcher instance
meme_fetcher = MemeFetcher()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    welcome_message = "Hi! Send /meme to get a random meme from Reddit! 🎭"
    await update.message.reply_text(welcome_message)


async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /meme command."""
    # Send a typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
    
    try:
        # Get a random meme
        meme = meme_fetcher.get_random_meme()
        
        if not meme:
            await update.message.reply_text(
                "Sorry! I couldn't fetch a meme right now. Please try again later! 😔"
            )
            return
        
        # Create caption with title and source
        if meme.get('source') == 'Giphy':
            caption = f"🎭 {meme['title']}\n\n📱 Source: Giphy"
        elif meme.get('source') == 'Fallback':
            caption = f"🎭 {meme['title']}\n\n📱 Source: Classic Memes"
        else:
            caption = f"🎭 {meme['title']}\n\n📱 Source: r/{meme['subreddit']}"
        
        # Send the meme
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=meme['url'],
            caption=caption,
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"Error sending meme: {e}")
        await update.message.reply_text(
            "Oops! Something went wrong while fetching your meme. Please try again! 😅"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = """
🤖 <b>Meme Bot Commands:</b>

/meme - Get a random meme from Reddit (or fallback sources)
/start - Start the bot
/help - Show this help message

<i>Memes are fetched from r/memes, r/dankmemes, and r/wholesomememes. If Reddit is unavailable, Giphy and classic memes are used as fallbacks.</i>
    """
    await update.message.reply_text(help_text, parse_mode='HTML')


def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    import os
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set your bot token: export TELEGRAM_BOT_TOKEN='your_token_here'")
        return
    
    # Create the Application
    application = Application.builder().token(bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("meme", meme_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Print startup message
    print("🤖 Telegram Meme Bot is starting...")
    print("📱 Bot will fetch memes from:")
    for subreddit in SUBREDDITS:
        print(f"   • r/{subreddit}")
    print("🔄 Giphy will be used as fallback if Reddit is unavailable")
    print("🛡️ Classic memes are available as final fallback")
    print("🚀 Bot is now running! Press Ctrl+C to stop.")
    
    # Start the bot
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Error running bot: {e}")


if __name__ == '__main__':
    main()