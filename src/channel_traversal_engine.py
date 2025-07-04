#!/usr/bin/env python3
"""
CHANNEL-BASED TRAVERSAL ENGINE
Comprehensive system for discovering coupon content through channel exploration,
related videos, playlists, and systematic video traversal beyond keyword searches.
"""

import os
import time
import logging
import json
import re
from typing import List, Optional, Dict, Any, Set, Tuple
from collections import defaultdict, deque
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import random

# Import models
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult

logger = logging.getLogger(__name__)

class ChannelTraversalEngine:
    """
    Advanced channel-based traversal engine for comprehensive coupon discovery
    """
    
    def __init__(self, api_key: str):
        """Initialize channel traversal engine"""
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        # Tracking sets to avoid infinite loops
        self.visited_videos: Set[str] = set()
        self.visited_channels: Set[str] = set()
        self.visited_playlists: Set[str] = set()
        
        # Discovery queues for breadth-first exploration
        self.channel_queue: deque = deque()
        self.video_queue: deque = deque()
        self.playlist_queue: deque = deque()
        
        # Known coupon channels (seed channels that frequently post coupon content)
        self.seed_coupon_channels = [
            # Tech/Software Coupon Channels
            'UCvjgXvBlbQiydffZU7m1_aw',  # Example tech deals channel
            'UC_x5XG1OV2P6uZZ5FSM9Ttw',  # Example software deals
            
            # Hosting/Domain Channels
            'UCWzaKX3HEmBBXGGEwjYKIDg',  # Example hosting reviews
            
            # Fitness/Supplement Channels
            'UCduKuJToxWPizJ7I2E6n1kA',  # Example fitness channel
            
            # Fashion/Beauty Channels
            'UCsT0YIqwnpJCM-mx7-gSA4Q',  # Example fashion hauls
            
            # General Deal/Coupon Channels
            'UCfMbPdxPrKQDGwf9-XQRvBA',  # Example deals channel
        ]
        
        # Channel categories for targeted discovery
        self.channel_categories = {
            'tech_deals': ['technology', 'gadgets', 'reviews', 'unboxing', 'tech deals'],
            'hosting_reviews': ['web hosting', 'domain', 'website', 'hosting review'],
            'fitness_supplements': ['fitness', 'bodybuilding', 'supplements', 'protein', 'workout'],
            'fashion_hauls': ['fashion', 'haul', 'shopping', 'style', 'outfit'],
            'food_delivery': ['food review', 'restaurant', 'delivery', 'food haul'],
            'travel_deals': ['travel', 'booking', 'hotel', 'flight deals', 'vacation'],
            'software_tutorials': ['software', 'tutorial', 'app review', 'productivity'],
            'gaming_content': ['gaming', 'game review', 'gaming deals', 'steam'],
            'beauty_reviews': ['makeup', 'skincare', 'beauty', 'cosmetics review'],
            'general_deals': ['deals', 'coupons', 'discounts', 'savings', 'promo codes']
        }
        
        logger.info("Channel Traversal Engine initialized")
    
    def discover_coupon_channels(self, category: str, max_channels: int = 50) -> List[str]:
        """Discover channels that likely contain coupon content based on category"""
        if category not in self.channel_categories:
            logger.warning(f"Unknown category: {category}")
            return []
        
        keywords = self.channel_categories[category]
        discovered_channels = []
        
        for keyword in keywords:
            try:
                # Search for channels in this category
                search_response = self.youtube.search().list(
                    q=keyword,
                    part='id,snippet',
                    type='channel',
                    maxResults=10,
                    order='relevance'
                ).execute()
                
                for item in search_response['items']:
                    channel_id = item['id']['channelId']
                    channel_title = item['snippet']['title']
                    
                    if channel_id not in discovered_channels and len(discovered_channels) < max_channels:
                        discovered_channels.append(channel_id)
                        logger.info(f"Discovered channel: {channel_title} ({channel_id})")
                
                # Rate limiting
                time.sleep(0.5)
                
            except HttpError as e:
                logger.error(f"Error discovering channels for {keyword}: {e}")
                continue
        
        return discovered_channels[:max_channels]
    
    def get_all_channel_videos(self, channel_id: str, max_videos: int = 200) -> List[str]:
        """Get all video IDs from a channel's uploads"""
        if channel_id in self.visited_channels:
            return []
        
        self.visited_channels.add(channel_id)
        video_ids = []
        
        try:
            # Get the uploads playlist ID
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                return []
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            next_page_token = None
            
            while len(video_ids) < max_videos:
                playlist_response = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_videos - len(video_ids)),
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_response['items']:
                    video_id = item['contentDetails']['videoId']
                    if video_id not in self.visited_videos:
                        video_ids.append(video_id)
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Rate limiting
                time.sleep(0.2)
            
            logger.info(f"Retrieved {len(video_ids)} videos from channel {channel_id}")
            return video_ids
            
        except HttpError as e:
            logger.error(f"Error getting videos from channel {channel_id}: {e}")
            return []
    
    def get_related_videos(self, video_id: str, max_related: int = 20) -> List[str]:
        """Get related videos using search with video context"""
        if video_id in self.visited_videos:
            return []
        
        try:
            # Get video details first
            video_response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                return []
            
            video_snippet = video_response['items'][0]['snippet']
            video_title = video_snippet['title']
            channel_id = video_snippet['channelId']
            
            # Extract keywords from title for related video search
            keywords = self.extract_keywords_from_title(video_title)
            
            related_videos = []
            
            # Search for related videos using extracted keywords
            for keyword in keywords[:3]:  # Use top 3 keywords
                try:
                    search_response = self.youtube.search().list(
                        q=keyword,
                        part='id',
                        type='video',
                        maxResults=10,
                        order='relevance'
                    ).execute()
                    
                    for item in search_response['items']:
                        related_video_id = item['id']['videoId']
                        if (related_video_id not in self.visited_videos and 
                            related_video_id != video_id and 
                            len(related_videos) < max_related):
                            related_videos.append(related_video_id)
                    
                    time.sleep(0.3)
                    
                except HttpError as e:
                    logger.debug(f"Error searching related videos for {keyword}: {e}")
                    continue
            
            # Also get more videos from the same channel
            channel_videos = self.get_recent_channel_videos(channel_id, max_videos=10)
            for vid in channel_videos:
                if vid not in self.visited_videos and vid != video_id and len(related_videos) < max_related:
                    related_videos.append(vid)
            
            return related_videos
            
        except HttpError as e:
            logger.error(f"Error getting related videos for {video_id}: {e}")
            return []
    
    def get_recent_channel_videos(self, channel_id: str, max_videos: int = 20) -> List[str]:
        """Get recent videos from a channel (last 30 days)"""
        try:
            # Get recent videos (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            published_after = thirty_days_ago.isoformat() + 'Z'
            
            search_response = self.youtube.search().list(
                channelId=channel_id,
                part='id',
                type='video',
                maxResults=max_videos,
                order='date',
                publishedAfter=published_after
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            return video_ids
            
        except HttpError as e:
            logger.debug(f"Error getting recent videos from channel {channel_id}: {e}")
            return []
    
    def extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract relevant keywords from video title for related video discovery"""
        # Remove common words and extract meaningful keywords
        common_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'is', 'are', 'was',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'a', 'an', 'video', 'review',
            'how', 'what', 'when', 'where', 'why', 'who', 'which'
        }
        
        # Extract words, remove punctuation, convert to lowercase
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        keywords = [word for word in words if word not in common_words]
        
        # Prioritize brand names and product-related terms
        priority_terms = [
            'discount', 'coupon', 'promo', 'deal', 'offer', 'sale', 'code',
            'hosting', 'protein', 'supplement', 'vpn', 'software', 'app',
            'fashion', 'beauty', 'tech', 'gaming', 'travel', 'food'
        ]
        
        # Sort keywords by priority
        prioritized = []
        for term in priority_terms:
            if term in keywords:
                prioritized.append(term)
                keywords.remove(term)
        
        return prioritized + keywords[:5]  # Return top priority + 5 other keywords
    
    def explore_channel_playlists(self, channel_id: str, max_playlists: int = 10) -> List[str]:
        """Explore playlists from a channel to find more coupon content"""
        try:
            playlists_response = self.youtube.playlists().list(
                part='id,snippet',
                channelId=channel_id,
                maxResults=max_playlists
            ).execute()
            
            playlist_video_ids = []
            
            for playlist in playlists_response['items']:
                playlist_id = playlist['id']
                playlist_title = playlist['snippet']['title'].lower()
                
                # Check if playlist might contain coupon content
                coupon_indicators = ['deal', 'coupon', 'discount', 'promo', 'offer', 'sale', 'haul', 'review']
                if any(indicator in playlist_title for indicator in coupon_indicators):
                    
                    if playlist_id not in self.visited_playlists:
                        self.visited_playlists.add(playlist_id)
                        
                        # Get videos from this playlist
                        playlist_videos = self.get_playlist_videos(playlist_id, max_videos=50)
                        playlist_video_ids.extend(playlist_videos)
                        
                        logger.info(f"Explored playlist: {playlist['snippet']['title']} ({len(playlist_videos)} videos)")
            
            return playlist_video_ids
            
        except HttpError as e:
            logger.error(f"Error exploring playlists for channel {channel_id}: {e}")
            return []
    
    def get_playlist_videos(self, playlist_id: str, max_videos: int = 50) -> List[str]:
        """Get all video IDs from a playlist"""
        video_ids = []
        next_page_token = None
        
        try:
            while len(video_ids) < max_videos:
                playlist_response = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=min(50, max_videos - len(video_ids)),
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_response['items']:
                    video_id = item['contentDetails']['videoId']
                    if video_id not in self.visited_videos:
                        video_ids.append(video_id)
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
                
                time.sleep(0.2)
            
            return video_ids
            
        except HttpError as e:
            logger.error(f"Error getting videos from playlist {playlist_id}: {e}")
            return []
    
    def run_comprehensive_channel_traversal(self, target_categories: List[str] = None, 
                                          max_videos_per_category: int = 500) -> List[str]:
        """
        Run comprehensive channel-based traversal to discover coupon content
        """
        if not target_categories:
            target_categories = list(self.channel_categories.keys())
        
        logger.info(f"Starting comprehensive channel traversal for categories: {target_categories}")
        
        all_discovered_videos = []
        
        # Phase 1: Discover channels for each category
        for category in target_categories:
            logger.info(f"Discovering channels for category: {category}")
            
            # Discover channels in this category
            category_channels = self.discover_coupon_channels(category, max_channels=20)
            
            # Add seed channels if available
            category_channels.extend(self.seed_coupon_channels[:5])
            
            category_videos = []
            
            # Phase 2: Explore each discovered channel comprehensively
            for channel_id in category_channels:
                if len(category_videos) >= max_videos_per_category:
                    break
                
                logger.info(f"Exploring channel: {channel_id}")
                
                # Get all videos from channel
                channel_videos = self.get_all_channel_videos(channel_id, max_videos=100)
                category_videos.extend(channel_videos)
                
                # Explore channel playlists
                playlist_videos = self.explore_channel_playlists(channel_id, max_playlists=5)
                category_videos.extend(playlist_videos)
                
                # Rate limiting between channels
                time.sleep(1)
            
            # Phase 3: Follow related videos for deeper discovery
            related_videos = []
            for video_id in category_videos[:50]:  # Use first 50 videos as seeds
                if len(related_videos) >= 100:  # Limit related videos per category
                    break
                
                video_related = self.get_related_videos(video_id, max_related=5)
                related_videos.extend(video_related)
                
                # Mark video as visited
                self.visited_videos.add(video_id)
                
                time.sleep(0.5)
            
            # Combine all videos for this category
            category_all_videos = list(set(category_videos + related_videos))
            all_discovered_videos.extend(category_all_videos)
            
            logger.info(f"Category {category}: discovered {len(category_all_videos)} videos")
        
        # Remove duplicates and return
        unique_videos = list(set(all_discovered_videos))
        logger.info(f"Total unique videos discovered: {len(unique_videos)}")
        
        return unique_videos
