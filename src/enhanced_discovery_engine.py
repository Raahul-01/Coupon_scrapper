#!/usr/bin/env python3
"""
ENHANCED DISCOVERY ENGINE
Advanced discovery mechanisms for finding coupon content through multiple pathways:
- Channel browsing and systematic exploration
- Related video following and recommendation traversal
- Playlist exploration and curation discovery
- Cross-platform content discovery
"""

import os
import time
import logging
import requests
import json
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime, timedelta
import random
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

# Import engines
from channel_traversal_engine import ChannelTraversalEngine
from web_scraping_engine import WebScrapingEngine
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult

logger = logging.getLogger(__name__)

class EnhancedDiscoveryEngine:
    """
    Comprehensive discovery engine that combines multiple discovery mechanisms
    """
    
    def __init__(self, api_key: str):
        """Initialize enhanced discovery engine"""
        self.api_key = api_key
        self.channel_traversal = ChannelTraversalEngine(api_key)
        self.web_scraper = WebScrapingEngine(enable_rate_limiting=True)
        
        # Discovery tracking
        self.discovered_channels: Set[str] = set()
        self.discovered_videos: Set[str] = set()
        self.discovery_stats = {
            'channels_explored': 0,
            'videos_discovered': 0,
            'playlists_explored': 0,
            'cross_platform_sources': 0
        }
        
        # Cross-platform sources for coupon discovery
        self.cross_platform_sources = {
            'reddit': [
                'https://www.reddit.com/r/deals/',
                'https://www.reddit.com/r/coupons/',
                'https://www.reddit.com/r/DiscountedProducts/',
                'https://www.reddit.com/r/DealsReddit/',
                'https://www.reddit.com/r/frugal/'
            ],
            'twitter_accounts': [
                '@dealsplus', '@slickdeals', '@retailmenot', '@coupons',
                '@woot', '@groupon', '@livingsocial', '@dealnews'
            ],
            'deal_forums': [
                'https://slickdeals.net/deals/',
                'https://www.dealsplus.com/',
                'https://www.dealcatcher.com/',
                'https://www.deals2buy.com/'
            ],
            'coupon_blogs': [
                'https://www.thekrazycouponlady.com/',
                'https://hip2save.com/',
                'https://www.southernsavers.com/',
                'https://www.couponmom.com/'
            ]
        }
        
        logger.info("Enhanced Discovery Engine initialized")
    
    def discover_channels_by_content_analysis(self, seed_videos: List[str], max_channels: int = 100) -> List[str]:
        """
        Discover channels by analyzing content of seed videos and finding similar channels
        """
        discovered_channels = []
        
        for video_id in seed_videos[:20]:  # Analyze first 20 seed videos
            try:
                # Get video details
                video_response = self.channel_traversal.youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                
                if not video_response['items']:
                    continue
                
                video_snippet = video_response['items'][0]['snippet']
                channel_id = video_snippet['channelId']
                video_title = video_snippet['title']
                video_description = video_snippet.get('description', '')
                
                # Add the channel
                if channel_id not in self.discovered_channels:
                    self.discovered_channels.add(channel_id)
                    discovered_channels.append(channel_id)
                
                # Extract keywords from title and description
                keywords = self.extract_content_keywords(video_title + ' ' + video_description)
                
                # Search for similar channels using these keywords
                for keyword in keywords[:3]:  # Use top 3 keywords
                    try:
                        search_response = self.channel_traversal.youtube.search().list(
                            q=keyword,
                            part='id,snippet',
                            type='channel',
                            maxResults=5,
                            order='relevance'
                        ).execute()
                        
                        for item in search_response['items']:
                            similar_channel_id = item['id']['channelId']
                            if (similar_channel_id not in self.discovered_channels and 
                                len(discovered_channels) < max_channels):
                                self.discovered_channels.add(similar_channel_id)
                                discovered_channels.append(similar_channel_id)
                                logger.info(f"Discovered similar channel: {item['snippet']['title']}")
                        
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.debug(f"Error searching for similar channels with keyword {keyword}: {e}")
                        continue
                
                time.sleep(0.3)
                
            except Exception as e:
                logger.error(f"Error analyzing video {video_id}: {e}")
                continue
        
        return discovered_channels
    
    def extract_content_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from video content for discovery"""
        import re
        
        # Coupon and deal related keywords
        coupon_keywords = [
            'discount', 'coupon', 'promo', 'deal', 'offer', 'sale', 'code',
            'save', 'off', 'percent', 'cashback', 'rebate', 'voucher'
        ]
        
        # Brand and product keywords
        brand_keywords = []
        
        # Extract potential brand names (capitalized words)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        brand_keywords.extend(words[:10])  # Top 10 capitalized words
        
        # Extract product categories
        category_keywords = [
            'hosting', 'domain', 'vpn', 'software', 'app', 'game', 'gaming',
            'protein', 'supplement', 'fitness', 'workout', 'nutrition',
            'fashion', 'clothing', 'beauty', 'makeup', 'skincare',
            'tech', 'gadget', 'phone', 'laptop', 'electronics',
            'travel', 'hotel', 'flight', 'booking', 'vacation',
            'food', 'restaurant', 'delivery', 'grocery'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        # Find coupon keywords
        for keyword in coupon_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Find category keywords
        for keyword in category_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Add brand keywords
        found_keywords.extend(brand_keywords[:5])
        
        return found_keywords[:10]  # Return top 10 keywords
    
    def explore_trending_and_popular_content(self, categories: List[str] = None) -> List[str]:
        """
        Explore trending and popular content to discover new coupon sources
        """
        if not categories:
            categories = ['Science & Technology', 'Howto & Style', 'People & Blogs', 'Entertainment']
        
        discovered_videos = []
        
        for category in categories:
            try:
                # Get popular videos in category
                popular_response = self.channel_traversal.youtube.videos().list(
                    part='id,snippet',
                    chart='mostPopular',
                    regionCode='US',
                    maxResults=20,
                    videoCategoryId=self.get_category_id(category)
                ).execute()
                
                for item in popular_response['items']:
                    video_id = item['id']
                    video_title = item['snippet']['title'].lower()
                    
                    # Check if video might contain coupon content
                    coupon_indicators = ['deal', 'coupon', 'discount', 'promo', 'offer', 'sale', 'haul', 'review']
                    if any(indicator in video_title for indicator in coupon_indicators):
                        discovered_videos.append(video_id)
                        logger.info(f"Found trending coupon video: {item['snippet']['title']}")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error exploring trending content for category {category}: {e}")
                continue
        
        return discovered_videos
    
    def get_category_id(self, category_name: str) -> str:
        """Get YouTube category ID for category name"""
        category_mapping = {
            'Science & Technology': '28',
            'Howto & Style': '26',
            'People & Blogs': '22',
            'Entertainment': '24',
            'Gaming': '20',
            'Education': '27',
            'News & Politics': '25'
        }
        return category_mapping.get(category_name, '22')  # Default to People & Blogs
    
    def discover_through_playlists(self, search_terms: List[str], max_playlists: int = 50) -> List[str]:
        """
        Discover coupon content through playlist exploration
        """
        discovered_videos = []
        
        for term in search_terms:
            try:
                # Search for playlists related to the term
                search_response = self.channel_traversal.youtube.search().list(
                    q=f"{term} playlist",
                    part='id,snippet',
                    type='playlist',
                    maxResults=10,
                    order='relevance'
                ).execute()
                
                for item in search_response['items']:
                    playlist_id = item['id']['playlistId']
                    playlist_title = item['snippet']['title'].lower()
                    
                    # Check if playlist might contain coupon content
                    coupon_indicators = ['deal', 'coupon', 'discount', 'promo', 'offer', 'sale', 'haul', 'review']
                    if any(indicator in playlist_title for indicator in coupon_indicators):
                        
                        # Get videos from this playlist
                        playlist_videos = self.channel_traversal.get_playlist_videos(playlist_id, max_videos=30)
                        discovered_videos.extend(playlist_videos)
                        
                        self.discovery_stats['playlists_explored'] += 1
                        logger.info(f"Explored playlist: {item['snippet']['title']} ({len(playlist_videos)} videos)")
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error discovering playlists for term {term}: {e}")
                continue
        
        return discovered_videos
    
    def scrape_cross_platform_sources(self, max_sources_per_platform: int = 3) -> List[Dict]:
        """
        Scrape cross-platform sources for coupon content
        """
        cross_platform_coupons = []
        
        # Scrape Reddit deal communities
        reddit_coupons = self.scrape_reddit_deals(max_sources_per_platform)
        cross_platform_coupons.extend(reddit_coupons)
        
        # Scrape deal forums
        forum_coupons = self.scrape_deal_forums(max_sources_per_platform)
        cross_platform_coupons.extend(forum_coupons)
        
        # Scrape coupon blogs
        blog_coupons = self.scrape_coupon_blogs(max_sources_per_platform)
        cross_platform_coupons.extend(blog_coupons)
        
        self.discovery_stats['cross_platform_sources'] = len(cross_platform_coupons)
        
        return cross_platform_coupons
    
    def scrape_reddit_deals(self, max_sources: int) -> List[Dict]:
        """Scrape Reddit deal communities for coupon content"""
        reddit_coupons = []
        
        for reddit_url in self.cross_platform_sources['reddit'][:max_sources]:
            try:
                headers = self.web_scraper.get_random_headers()
                response = requests.get(reddit_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract post titles and content
                posts = soup.find_all('div', {'data-testid': 'post-content'})
                
                for post in posts[:20]:  # Process first 20 posts
                    try:
                        title_element = post.find('h3')
                        if title_element:
                            title = title_element.get_text(strip=True)
                            
                            # Check if post contains coupon content
                            if any(keyword in title.lower() for keyword in ['coupon', 'code', 'deal', 'discount', 'promo']):
                                
                                # Extract potential coupon codes from title
                                coupon_codes = self.extract_codes_from_text(title)
                                
                                for code in coupon_codes:
                                    reddit_coupons.append({
                                        'coupon_code': code,
                                        'source': 'reddit',
                                        'source_url': reddit_url,
                                        'title': title,
                                        'platform': 'cross_platform'
                                    })
                    
                    except Exception as e:
                        logger.debug(f"Error processing Reddit post: {e}")
                        continue
                
                time.sleep(2)  # Rate limiting for Reddit
                
            except Exception as e:
                logger.error(f"Error scraping Reddit URL {reddit_url}: {e}")
                continue
        
        return reddit_coupons
    
    def scrape_deal_forums(self, max_sources: int) -> List[Dict]:
        """Scrape deal forums for coupon content"""
        forum_coupons = []
        
        for forum_url in self.cross_platform_sources['deal_forums'][:max_sources]:
            try:
                headers = self.web_scraper.get_random_headers()
                response = requests.get(forum_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Use existing web scraper logic
                page_text = BeautifulSoup(response.content, 'html.parser').get_text()
                
                # Extract coupon information using existing logic
                from text_processing_utils import extract_coupon_information_improved
                coupon_info_list = extract_coupon_information_improved(page_text)
                
                for info in coupon_info_list:
                    forum_coupons.append({
                        'coupon_code': info['coupon_code'],
                        'brand': info['brand'],
                        'source': 'deal_forum',
                        'source_url': forum_url,
                        'description': info['description'],
                        'platform': 'cross_platform'
                    })
                
                time.sleep(3)  # Rate limiting for forums
                
            except Exception as e:
                logger.error(f"Error scraping forum URL {forum_url}: {e}")
                continue
        
        return forum_coupons
    
    def scrape_coupon_blogs(self, max_sources: int) -> List[Dict]:
        """Scrape coupon blogs for coupon content"""
        blog_coupons = []
        
        for blog_url in self.cross_platform_sources['coupon_blogs'][:max_sources]:
            try:
                headers = self.web_scraper.get_random_headers()
                response = requests.get(blog_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for coupon-related content
                coupon_elements = soup.find_all(['div', 'span', 'p'], 
                                              text=re.compile(r'code|coupon|promo', re.IGNORECASE))
                
                for element in coupon_elements[:10]:
                    try:
                        text = element.get_text(strip=True)
                        codes = self.extract_codes_from_text(text)
                        
                        for code in codes:
                            blog_coupons.append({
                                'coupon_code': code,
                                'source': 'coupon_blog',
                                'source_url': blog_url,
                                'description': text[:200],
                                'platform': 'cross_platform'
                            })
                    
                    except Exception as e:
                        logger.debug(f"Error processing blog element: {e}")
                        continue
                
                time.sleep(2)  # Rate limiting for blogs
                
            except Exception as e:
                logger.error(f"Error scraping blog URL {blog_url}: {e}")
                continue
        
        return blog_coupons
    
    def extract_codes_from_text(self, text: str) -> List[str]:
        """Extract potential coupon codes from text"""
        import re
        
        # Patterns for coupon codes
        patterns = [
            r'\b([A-Z]{2,}[0-9]{2,})\b',  # SAVE20, GET50
            r'\b([0-9]{2,}[A-Z]{2,})\b',  # 20OFF, 50SAVE
            r'\b([A-Z0-9]{4,12})\b',      # General alphanumeric codes
        ]
        
        codes = []
        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            for match in matches:
                if self.web_scraper.is_valid_coupon_code(match):
                    codes.append(match)
        
        return list(set(codes))  # Remove duplicates
    
    def run_comprehensive_discovery(self, seed_videos: List[str] = None, 
                                  discovery_categories: List[str] = None) -> Dict:
        """
        Run comprehensive discovery across all mechanisms
        """
        logger.info("Starting comprehensive discovery across all mechanisms...")
        
        discovery_results = {
            'discovered_videos': [],
            'discovered_channels': [],
            'cross_platform_coupons': [],
            'playlist_videos': []
        }
        
        # Phase 1: Channel-based discovery
        if seed_videos:
            logger.info("Phase 1: Discovering channels through content analysis...")
            discovered_channels = self.discover_channels_by_content_analysis(seed_videos, max_channels=50)
            discovery_results['discovered_channels'] = discovered_channels
            self.discovery_stats['channels_explored'] = len(discovered_channels)
        
        # Phase 2: Trending content exploration
        logger.info("Phase 2: Exploring trending and popular content...")
        trending_videos = self.explore_trending_and_popular_content(discovery_categories)
        discovery_results['discovered_videos'].extend(trending_videos)
        
        # Phase 3: Playlist discovery
        logger.info("Phase 3: Discovering content through playlists...")
        search_terms = ['deals', 'coupons', 'discounts', 'promo codes', 'savings', 'hauls', 'reviews']
        playlist_videos = self.discover_through_playlists(search_terms, max_playlists=30)
        discovery_results['playlist_videos'] = playlist_videos
        discovery_results['discovered_videos'].extend(playlist_videos)
        
        # Phase 4: Cross-platform discovery
        logger.info("Phase 4: Scraping cross-platform sources...")
        cross_platform_coupons = self.scrape_cross_platform_sources(max_sources_per_platform=2)
        discovery_results['cross_platform_coupons'] = cross_platform_coupons
        
        # Update stats
        self.discovery_stats['videos_discovered'] = len(set(discovery_results['discovered_videos']))
        
        logger.info("Comprehensive discovery completed!")
        self.log_discovery_stats()
        
        return discovery_results
    
    def log_discovery_stats(self):
        """Log comprehensive discovery statistics"""
        stats = self.discovery_stats
        logger.info("="*60)
        logger.info("COMPREHENSIVE DISCOVERY STATISTICS")
        logger.info("="*60)
        logger.info(f"Channels explored: {stats['channels_explored']}")
        logger.info(f"Videos discovered: {stats['videos_discovered']}")
        logger.info(f"Playlists explored: {stats['playlists_explored']}")
        logger.info(f"Cross-platform sources: {stats['cross_platform_sources']}")
        logger.info("="*60)
