#!/usr/bin/env python3
"""
IMPROVED COUPON EXTRACTION ENGINE
Context-aware extraction without relying on predefined samples
"""

import os
import time
import logging
import json
import re
import requests
from typing import List, Optional, Dict, Any, Set
from collections import Counter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import random

# Import improved modules
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult
from text_processing_utils import (
    extract_coupon_information_improved,
    clean_text_advanced
)
from web_scraping_engine import WebScrapingEngine
from enhanced_brand_database import get_all_brands, get_brands_by_category, is_known_brand
from channel_traversal_engine import ChannelTraversalEngine
from enhanced_discovery_engine import EnhancedDiscoveryEngine
from persistent_data_manager import PersistentDataManager

# Professional logging setup
os.makedirs('data', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/improved_automation_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ImprovedCouponEngine:
    """
    Improved Coupon Extraction Engine
    
    Key Improvements:
    - Context-aware brand-code linking (no predefined samples)
    - Real-time pattern recognition
    - Eliminates false positive extractions
    - Prevents same code from being assigned to multiple brands
    - Focuses on actual coupon codes, not random words
    """
    
    def __init__(self, api_key: str, enable_deduplication: bool = True, enable_web_scraping: bool = True,
                 enable_channel_traversal: bool = True, enable_persistent_data: bool = True):
        """Initialize comprehensive extraction engine with all advanced capabilities"""
        self.api_key = api_key
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE':
            raise ValueError("Please provide a valid YouTube API key")

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Initialize all engines
        self.enable_web_scraping = enable_web_scraping
        self.enable_channel_traversal = enable_channel_traversal
        self.enable_persistent_data = enable_persistent_data

        if enable_web_scraping:
            self.web_scraper = WebScrapingEngine(enable_rate_limiting=True)
            logger.info("Web scraping engine initialized")

        if enable_channel_traversal:
            self.channel_traversal = ChannelTraversalEngine(api_key)
            self.discovery_engine = EnhancedDiscoveryEngine(api_key)
            logger.info("Channel traversal and discovery engines initialized")

        if enable_persistent_data:
            self.data_manager = PersistentDataManager()
            logger.info("Persistent data manager initialized")

        # Enhanced tracking
        self.enable_deduplication = enable_deduplication
        self.processed_combinations: Set[str] = set()  # Track code-brand combinations
        self.session_stats = {
            'total_videos_analyzed': 0,
            'total_coupons_found': 0,
            'unique_coupons': 0,
            'false_positives_prevented': 0,
            'web_scraped_coupons': 0,
            'channel_traversal_videos': 0,
            'cross_platform_coupons': 0,
            'incremental_new_coupons': 0
        }

        logger.info("Comprehensive Coupon Extraction Engine initialized (all features enabled)")
    
    def analyze_video_description_improved(self, description: str, video_title: str, video_id: str) -> List[CouponInfo]:
        """
        Improved video description analysis with context-aware extraction
        """
        if not description:
            return []
        
        logger.info(f"Analyzing video description with improved method (ID: {video_id})")
        
        # Use improved extraction that links codes to brands contextually
        coupon_info_list = extract_coupon_information_improved(description)
        
        if not coupon_info_list:
            logger.info("No valid coupon codes found in description")
            return []
        
        # Convert to CouponInfo objects with validation
        validated_coupons = []
        
        for info in coupon_info_list:
            # Create unique identifier for deduplication
            combination_id = f"{info['coupon_code']}_{info['brand']}_{info['category']}"
            
            # Check if this exact combination was already processed
            if self.enable_deduplication and combination_id.lower() in self.processed_combinations:
                logger.info(f"Skipping duplicate combination: {combination_id}")
                self.session_stats['false_positives_prevented'] += 1
                continue
            
            # Validate the extraction quality
            if self.validate_extraction_quality(info):
                coupon = CouponInfo(
                    coupon_code=info['coupon_code'],
                    coupon_name=info['title'],
                    brand=info['brand'],
                    percent_off=float(info['percentage']) if info['percentage'] else None,
                    expiry_date=info['expiry_date'],
                    description=info['description'][:200] + "..." if len(info['description']) > 200 else info['description'],
                    category=info['category'],
                    video_id=video_id,
                    video_title=video_title,
                    extraction_confidence=info.get('confidence', 0.8)
                )
                
                validated_coupons.append(coupon)
                
                # Track this combination
                if self.enable_deduplication:
                    self.processed_combinations.add(combination_id.lower())
                
                logger.info(f"Valid coupon extracted: {info['coupon_code']} -> {info['brand']}")
            else:
                logger.info(f"Rejected low-quality extraction: {info['coupon_code']} -> {info['brand']}")
                self.session_stats['false_positives_prevented'] += 1
        
        self.session_stats['total_coupons_found'] += len(validated_coupons)
        self.session_stats['unique_coupons'] += len(validated_coupons)
        
        logger.info(f"Improved analysis result: {len(validated_coupons)} high-quality coupons")
        return validated_coupons
    
    def validate_extraction_quality(self, coupon_info: Dict[str, any]) -> bool:
        """
        ULTRA HIGH-VOLUME validation - Minimal restrictions for maximum coupon capture
        """
        code = coupon_info.get('coupon_code', '')
        brand = coupon_info.get('brand', '')
        confidence = coupon_info.get('confidence', 0)

        # Must have valid code (minimum requirements only)
        if not code or len(code) < 3:  # Reduced from 4 to 3
            return False

        # Allow coupons even without perfect brand identification
        # Brand can be 'Unknown' - we'll extract it anyway for volume
        if not brand:
            return False

        # ULTRA LOW confidence threshold for maximum volume
        if confidence < 0.3:  # Reduced from 0.4 to 0.3
            return False

        # Enhanced brand validation using our comprehensive database
        if brand != 'Unknown' and is_known_brand(brand):
            # If it's a known brand, accept with lower standards
            return True

        # Comprehensive list of words that are NOT coupon codes
        common_non_codes = {
            # Social media actions
            'SUBSCRIBE', 'COMMENT', 'LIKE', 'SHARE', 'FOLLOW', 'BELL', 'NOTIFICATION',
            # Status words
            'WORKING', 'VERIFIED', 'TESTED', 'ACTIVE', 'VALID', 'EXPIRED', 'NEW', 'LATEST',
            # Promotional words
            'MAXIMUM', 'MINIMUM', 'BONUS', 'EXTRA', 'SPECIAL', 'LIMITED', 'EXCLUSIVE',
            # Generic words
            'UPDATE', 'CODES', 'CODE', 'COUPON', 'PROMO', 'DISCOUNT', 'OFFER', 'DEAL',
            'SAVE', 'FREE', 'GET', 'WIN', 'GRAB', 'HURRY', 'NOW', 'TODAY', 'HERE',
            # Gaming/app words
            'COOKIE', 'KINGDOM', 'GAME', 'PLAY', 'LEVEL', 'COINS', 'GEMS', 'POINTS',
            # Platform words
            'TELEGRAM', 'WHATSAPP', 'INSTAGRAM', 'FACEBOOK', 'YOUTUBE', 'TWITTER',
            # Action words
            'CLICK', 'VISIT', 'CHECK', 'WATCH', 'DOWNLOAD', 'INSTALL', 'REGISTER',
            # Common misidentified words
            'QUERIES', 'DOMINOS', 'PIZZA', 'AMAZON', 'FLIPKART'  # These are brand names, not codes
        }

        if code.upper() in common_non_codes:
            return False

        # Brand must not be a suspicious extraction
        suspicious_brands = {
            'But', 'Gift', 'Grab', 'Mega', 'Get', 'Save', 'Free', 'Deal',
            'Code', 'Offer', 'Sale', 'New', 'Best', 'Top', 'Here', 'This',
            'Update', 'Working', 'Latest', 'Current', 'Active', 'Valid',
            'Discount', 'Couponnxt'  # Generic coupon site names
        }

        if brand in suspicious_brands:
            return False

        # REMOVED: Overly restrictive pattern validation
        # Allow more coupon code patterns for higher volume

        # REMOVED: Overly restrictive brand-context validation
        # Accept more brand associations for higher volume

        return True

    def _has_valid_code_pattern(self, code: str) -> bool:
        """Check if the code has a valid coupon code pattern"""
        # Must have both letters and numbers
        has_letters = any(c.isalpha() for c in code)
        has_numbers = any(c.isdigit() for c in code)

        if not (has_letters and has_numbers):
            return False

        # Should not be all the same character repeated
        if len(set(code)) < 3:
            return False

        # Should not match common non-code patterns
        invalid_patterns = [
            r'^[A-Z]+\d{1,2}$',  # Like GET50, SAVE25 (too simple)
            r'^\d{1,2}[A-Z]+$',  # Like 50OFF, 25SAVE (too simple)
            r'^(GET|SAVE|WIN|USE|TRY|BUY)\d+$',  # Common word + number
            r'^\d{1,2}(ST|ND|RD|TH)$',  # Date ordinals like 31ST, 22ND
            r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\d*$',  # Month abbreviations
            r'^\d{4}$',  # Years like 2025, 2024
        ]

        for pattern in invalid_patterns:
            if re.match(pattern, code):
                return False

        return True

    def _validate_brand_context_match(self, brand: str, context: str) -> bool:
        """Validate that the brand actually appears in the context"""
        if not brand or not context:
            return False

        # Check if brand appears in the context (case insensitive)
        # Try brand variations to handle different formats
        brand_variations = [
            brand.lower(),
            brand.upper(),
            brand.title(),
            brand.replace("'", ""),  # Handle apostrophes
            brand.replace(" ", ""),   # Handle spaces
        ]

        context_lower = context.lower()
        for variation in brand_variations:
            if variation in context_lower:
                return True

        return False

    def search_fresh_videos(self, query: str, max_results: int = 50) -> List[str]:
        """Search for videos with promotional/influencer content - EXTENDED TIME RANGE"""
        try:
            # Search for recent videos (last 90 days for broader coverage)
            ninety_days_ago = datetime.now() - timedelta(days=90)
            published_after = ninety_days_ago.isoformat() + 'Z'

            # Use broader search terms to capture influencer promotional content
            # Don't force "coupon code" - let the content analysis find the codes
            search_response = self.youtube.search().list(
                q=query,  # Use the query as-is for broader targeting
                part='id',
                type='video',
                maxResults=min(max_results, 50),
                order='relevance',  # Changed from 'date' to 'relevance' for better quality
                publishedAfter=published_after
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items']]
            logger.info(f"Found {len(video_ids)} promotional videos (90-day range) for query: '{query}'")

            return video_ids

        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in video search: {e}")
            return []
    
    def get_video_details(self, video_id: str) -> Optional[VideoInfo]:
        """Get video details with error handling"""
        try:
            video_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                return None
            
            video_data = video_response['items'][0]
            snippet = video_data['snippet']
            statistics = video_data.get('statistics', {})
            
            return VideoInfo(
                video_id=video_id,
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                channel_title=snippet.get('channelTitle', ''),
                published_at=snippet.get('publishedAt', ''),
                view_count=int(statistics.get('viewCount', 0)),
                coupons=[]
            )
        
        except HttpError as e:
            logger.error(f"YouTube API error for video {video_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting video details for {video_id}: {e}")
            return None
    
    def process_video_batch_improved(self, video_ids: List[str]) -> ScrapingResult:
        """Process batch of videos with improved extraction"""
        result = ScrapingResult()
        
        for i, video_id in enumerate(video_ids):
            try:
                logger.info(f"Processing video {i+1}/{len(video_ids)}: {video_id}")
                
                # Get video details
                video_info = self.get_video_details(video_id)
                if not video_info:
                    continue
                
                # Improved analysis
                extracted_coupons = self.analyze_video_description_improved(
                    video_info.description,
                    video_info.title,
                    video_info.video_id
                )

                if extracted_coupons:
                    # Set channel name for each coupon
                    for coupon in extracted_coupons:
                        coupon.channel_name = video_info.channel_title

                    video_info.coupons = extracted_coupons
                    result.videos.append(video_info)
                    logger.info(f"Extracted {len(extracted_coupons)} valid coupons from video")
                else:
                    logger.info("No valid coupons found in this video")
                
                result.total_videos_processed += 1
                self.session_stats['total_videos_analyzed'] += 1
                
                # Reduced rate limiting for faster processing
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing video {video_id}: {e}")
                continue
        
        result.total_coupons_found = sum(len(video.coupons) for video in result.videos)
        return result
    
    def export_improved_results(self, result: ScrapingResult, filename: str) -> str:
        """Export results with improved data quality including YouTuber channel name"""
        rows = []

        for video in result.videos:
            for coupon in video.coupons:
                row = {
                    'Coupon Title': coupon.coupon_name or 'N/A',
                    'Coupon Code': coupon.coupon_code or 'N/A',
                    'Brand': coupon.brand or 'N/A',
                    'Discount Percent': f"{coupon.percent_off}%" if coupon.percent_off else 'N/A',
                    'Expiry Date': coupon.expiry_date or 'N/A',
                    'Discount Description': coupon.description or 'N/A',
                    'Category': coupon.category or 'N/A',
                    'YouTuber Channel': coupon.channel_name or video.channel_title or 'N/A',  # 8th field
                    'Extraction Confidence': f"{coupon.extraction_confidence:.2f}" if hasattr(coupon, 'extraction_confidence') else 'N/A',
                    'Video ID': coupon.video_id or 'N/A'
                }
                rows.append(row)

        if rows:
            df = pd.DataFrame(rows)
            # Remove duplicates based on code-brand combination
            df = df.drop_duplicates(subset=['Coupon Code', 'Brand'], keep='first')
            df.to_csv(filename, index=False)
            logger.info(f"Exported {len(df)} unique, high-quality coupons with YouTuber channels to {filename}")
        else:
            logger.warning("No coupon data to export")

        return filename
    
    def run_comprehensive_extraction(self, search_queries: List[str] = None, max_results_per_query: int = 50,
                                   enable_web_scraping: bool = True, target_industries: List[str] = None) -> ScrapingResult:
        """
        COMPREHENSIVE extraction combining YouTube API + Web Scraping for MAXIMUM volume
        """
        logger.info("Starting COMPREHENSIVE coupon extraction (YouTube + Web Scraping)")

        # Run YouTube extraction first
        youtube_result = self.run_improved_extraction(search_queries, max_results_per_query)

        # Run web scraping if enabled
        if enable_web_scraping and self.enable_web_scraping:
            logger.info("Starting web scraping phase for additional coupons...")

            # Define target industries if not provided
            if not target_industries:
                target_industries = ['hosting', 'fitness', 'software', 'gaming', 'fashion']

            # Get target brands for each industry
            target_brands = []
            for industry in target_industries:
                industry_brands = get_brands_by_category(industry)[:20]  # Top 20 brands per industry
                target_brands.extend(industry_brands)

            # Run web scraping
            web_result = self.web_scraper.run_comprehensive_scraping(
                target_brands=target_brands,
                target_industries=target_industries
            )

            # Merge results
            youtube_result.videos.extend(web_result.videos)
            youtube_result.total_videos_processed += web_result.total_videos_processed
            youtube_result.total_coupons_found += web_result.total_coupons_found

            self.session_stats['web_scraped_coupons'] = web_result.total_coupons_found

            logger.info(f"Web scraping added {web_result.total_coupons_found} additional coupons")

        # Print comprehensive statistics
        self.print_comprehensive_stats(youtube_result)

        return youtube_result

    def run_ultimate_extraction(self, search_queries: List[str] = None, max_results_per_query: int = 50,
                               enable_channel_traversal: bool = True, enable_cross_platform: bool = True,
                               target_industries: List[str] = None, max_channels_per_category: int = 20) -> ScrapingResult:
        """
        ULTIMATE extraction combining ALL discovery mechanisms:
        - Keyword-based YouTube search
        - Comprehensive channel traversal
        - Related video following
        - Playlist exploration
        - Cross-platform discovery
        - Web scraping
        - Intelligent duplicate detection
        - Persistent data management
        """
        logger.info("🚀 Starting ULTIMATE coupon extraction with ALL discovery mechanisms!")

        # Initialize comprehensive result
        ultimate_result = ScrapingResult()
        all_discovered_videos = []

        # Phase 1: Traditional keyword-based search (baseline)
        logger.info("📍 Phase 1: Traditional keyword-based YouTube search...")
        keyword_result = self.run_improved_extraction(search_queries, max_results_per_query)
        ultimate_result.videos.extend(keyword_result.videos)
        ultimate_result.total_videos_processed += keyword_result.total_videos_processed
        ultimate_result.total_coupons_found += keyword_result.total_coupons_found

        # Collect seed videos for further discovery
        seed_videos = []
        for video in keyword_result.videos:
            seed_videos.append(video.video_id)

        # Phase 2: Channel-based traversal discovery
        if enable_channel_traversal and self.enable_channel_traversal:
            logger.info("📍 Phase 2: Comprehensive channel traversal discovery...")

            # Define target categories
            if not target_industries:
                target_industries = ['tech_deals', 'hosting_reviews', 'fitness_supplements',
                                   'fashion_hauls', 'food_delivery', 'software_tutorials',
                                   'gaming_content', 'general_deals']

            # Run comprehensive channel traversal
            traversal_videos = self.channel_traversal.run_comprehensive_channel_traversal(
                target_categories=target_industries,
                max_videos_per_category=200
            )

            # Process discovered videos
            if traversal_videos:
                traversal_result = self.process_video_batch_improved(traversal_videos[:500])  # Limit for performance
                ultimate_result.videos.extend(traversal_result.videos)
                ultimate_result.total_videos_processed += traversal_result.total_videos_processed
                ultimate_result.total_coupons_found += traversal_result.total_coupons_found

                self.session_stats['channel_traversal_videos'] = len(traversal_videos)
                logger.info(f"✅ Channel traversal discovered {len(traversal_videos)} videos, extracted {traversal_result.total_coupons_found} coupons")

        # Phase 3: Enhanced discovery mechanisms
        if self.enable_channel_traversal:
            logger.info("📍 Phase 3: Enhanced discovery (trending, playlists, related videos)...")

            discovery_results = self.discovery_engine.run_comprehensive_discovery(
                seed_videos=seed_videos[:50],  # Use first 50 as seeds
                discovery_categories=['Science & Technology', 'Howto & Style', 'People & Blogs']
            )

            # Process discovered videos
            enhanced_videos = discovery_results['discovered_videos']
            if enhanced_videos:
                enhanced_result = self.process_video_batch_improved(enhanced_videos[:300])  # Limit for performance
                ultimate_result.videos.extend(enhanced_result.videos)
                ultimate_result.total_videos_processed += enhanced_result.total_videos_processed
                ultimate_result.total_coupons_found += enhanced_result.total_coupons_found

                logger.info(f"✅ Enhanced discovery found {len(enhanced_videos)} videos, extracted {enhanced_result.total_coupons_found} coupons")

            # Process cross-platform coupons
            cross_platform_coupons = discovery_results['cross_platform_coupons']
            if cross_platform_coupons:
                cross_platform_result = self.process_cross_platform_coupons(cross_platform_coupons)
                ultimate_result.videos.extend(cross_platform_result.videos)
                ultimate_result.total_coupons_found += cross_platform_result.total_coupons_found

                self.session_stats['cross_platform_coupons'] = len(cross_platform_coupons)
                logger.info(f"✅ Cross-platform discovery found {len(cross_platform_coupons)} coupons")

        # Phase 4: Web scraping (existing functionality)
        if self.enable_web_scraping:
            logger.info("📍 Phase 4: Web scraping major coupon sites...")

            if not target_industries:
                target_industries = ['hosting', 'fitness', 'software', 'gaming', 'fashion']

            # Get target brands for each industry
            target_brands = []
            for industry in target_industries:
                industry_brands = get_brands_by_category(industry)[:15]  # Top 15 brands per industry
                target_brands.extend(industry_brands)

            # Run web scraping
            web_result = self.web_scraper.run_comprehensive_scraping(
                target_brands=target_brands,
                target_industries=target_industries
            )

            ultimate_result.videos.extend(web_result.videos)
            ultimate_result.total_videos_processed += web_result.total_videos_processed
            ultimate_result.total_coupons_found += web_result.total_coupons_found

            self.session_stats['web_scraped_coupons'] = web_result.total_coupons_found
            logger.info(f"✅ Web scraping added {web_result.total_coupons_found} additional coupons")

        # Phase 5: Intelligent duplicate filtering and persistent storage
        if self.enable_persistent_data:
            logger.info("📍 Phase 5: Intelligent duplicate filtering and persistent storage...")

            # Save with intelligent duplicate detection
            saved_filename = self.data_manager.save_incremental_results(ultimate_result, append_to_existing=True)

            # Update stats
            self.session_stats['incremental_new_coupons'] = self.data_manager.duplicate_stats['new_coupons_added']

            logger.info(f"✅ Saved results with intelligent duplicate filtering to: {saved_filename}")

        # Print ultimate statistics
        self.print_ultimate_stats(ultimate_result)

        return ultimate_result

    def process_cross_platform_coupons(self, cross_platform_coupons: List[Dict]) -> ScrapingResult:
        """Process cross-platform coupon data into ScrapingResult format"""
        result = ScrapingResult()

        if not cross_platform_coupons:
            return result

        # Convert cross-platform coupons to CouponInfo objects
        processed_coupons = []

        for coupon_data in cross_platform_coupons:
            try:
                coupon = CouponInfo(
                    coupon_code=coupon_data.get('coupon_code', ''),
                    coupon_name=f"Cross-Platform Deal: {coupon_data.get('coupon_code', '')}",
                    brand=coupon_data.get('brand', 'Unknown'),
                    percent_off=None,
                    expiry_date='N/A',
                    description=coupon_data.get('description', '')[:200],
                    category='cross_platform',
                    video_id=coupon_data.get('source_url', 'cross_platform'),
                    video_title=f"Cross-Platform Discovery: {coupon_data.get('source', 'Unknown')}",
                    extraction_confidence=0.7
                )
                coupon.channel_name = f"Cross-Platform - {coupon_data.get('source', 'Unknown')}"
                processed_coupons.append(coupon)

            except Exception as e:
                logger.error(f"Error processing cross-platform coupon: {e}")
                continue

        # Group into video-like container
        if processed_coupons:
            video_info = VideoInfo(
                video_id="cross_platform_batch",
                title="Cross-Platform Discovered Coupons",
                description="Coupons discovered from cross-platform sources",
                channel_title="Cross-Platform Discovery",
                published_at=datetime.now().isoformat(),
                view_count=0,
                coupons=processed_coupons
            )
            result.videos.append(video_info)

        result.total_videos_processed = 1
        result.total_coupons_found = len(processed_coupons)

        return result

    def run_improved_extraction(self, search_queries: List[str] = None, max_results_per_query: int = 50) -> ScrapingResult:
        """
        Main entry point for improved coupon extraction with expanded influencer promotional content targeting.
        Now targets broader range of videos where influencers promote products and offer discount codes,
        not just videos with 'coupon' in the title.
        """
        if search_queries is None:
            search_queries = [
                # Brand-specific promotional content
                "temu review discount", "temu haul promo", "temu unboxing deal",
                "amazon review discount", "amazon haul deal", "amazon unboxing promo",
                "flipkart review offer", "flipkart haul discount", "flipkart unboxing deal",
                "myntra haul discount", "myntra review offer", "myntra try on promo",
                "nykaa review discount", "nykaa haul offer", "nykaa unboxing deal",
                "dominos review promo", "zomato discount review",

                # General promotional/influencer content
                "sponsored review discount", "brand collaboration promo", "influencer discount code",
                "product review discount", "unboxing discount code", "haul promo code",
                "try on discount", "sponsored content promo", "brand partnership discount"
            ]
        
        logger.info("Starting improved coupon extraction (expanded targeting, context-aware, no false positives)")
        
        all_video_ids = []
        
        # Gather videos from all search queries
        for query in search_queries:
            logger.info(f"Searching for: {query}")
            video_ids = self.search_fresh_videos(query, max_results_per_query)
            all_video_ids.extend(video_ids)
        
        # Remove duplicate video IDs
        unique_video_ids = list(set(all_video_ids))
        logger.info(f"Total unique videos to analyze: {len(unique_video_ids)}")
        
        # Process videos with improved extraction
        result = self.process_video_batch_improved(unique_video_ids)
        
        # Print session statistics
        self.print_session_stats(result)
        
        return result
    
    def print_session_stats(self, result: ScrapingResult):
        """Print comprehensive session statistics"""
        logger.info("="*60)
        logger.info("IMPROVED EXTRACTION SESSION STATISTICS")
        logger.info("="*60)
        logger.info(f"Total Videos Analyzed: {self.session_stats['total_videos_analyzed']}")
        logger.info(f"Videos with Valid Coupons: {len(result.videos)}")
        logger.info(f"Total Coupons Found: {result.total_coupons_found}")
        logger.info(f"False Positives Prevented: {self.session_stats['false_positives_prevented']}")
        logger.info(f"Unique Code-Brand Combinations: {len(self.processed_combinations)}")
        
        if result.videos:
            # Brand distribution
            brand_counter = Counter()
            category_counter = Counter()
            
            for video in result.videos:
                for coupon in video.coupons:
                    brand_counter[coupon.brand] += 1
                    category_counter[coupon.category] += 1
            
            logger.info("\nBRAND DISTRIBUTION:")
            for brand, count in brand_counter.most_common():
                logger.info(f"  {brand}: {count} coupons")

            logger.info("\nCATEGORY DISTRIBUTION:")
            for category, count in category_counter.most_common():
                logger.info(f"  {category}: {count} coupons")
        
        logger.info("="*60)

    def print_comprehensive_stats(self, result: ScrapingResult):
        """Print comprehensive session statistics including web scraping"""
        logger.info("="*70)
        logger.info("COMPREHENSIVE EXTRACTION SESSION STATISTICS")
        logger.info("="*70)
        logger.info(f"Total Videos Analyzed (YouTube): {self.session_stats['total_videos_analyzed']}")
        logger.info(f"Videos with Valid Coupons: {len(result.videos)}")
        logger.info(f"Total Coupons Found: {result.total_coupons_found}")
        logger.info(f"YouTube Coupons: {result.total_coupons_found - self.session_stats.get('web_scraped_coupons', 0)}")
        logger.info(f"Web Scraped Coupons: {self.session_stats.get('web_scraped_coupons', 0)}")
        logger.info(f"False Positives Prevented: {self.session_stats['false_positives_prevented']}")
        logger.info(f"Unique Code-Brand Combinations: {len(self.processed_combinations)}")

        if result.videos:
            # Brand distribution
            brand_counter = Counter()
            category_counter = Counter()
            source_counter = Counter()

            for video in result.videos:
                for coupon in video.coupons:
                    brand_counter[coupon.brand] += 1
                    category_counter[coupon.category] += 1
                    if hasattr(coupon, 'channel_name'):
                        if 'Web Scraping' in coupon.channel_name:
                            source_counter['Web Scraping'] += 1
                        else:
                            source_counter['YouTube'] += 1

            logger.info("\nSOURCE DISTRIBUTION:")
            for source, count in source_counter.most_common():
                logger.info(f"  {source}: {count} coupons")

            logger.info("\nTOP BRANDS (Top 10):")
            for brand, count in brand_counter.most_common(10):
                logger.info(f"  {brand}: {count} coupons")

            logger.info("\nCATEGORY DISTRIBUTION:")
            for category, count in category_counter.most_common():
                logger.info(f"  {category}: {count} coupons")

        logger.info("="*70)

    def print_ultimate_stats(self, result: ScrapingResult):
        """Print comprehensive ultimate extraction statistics"""
        logger.info("="*80)
        logger.info("🚀 ULTIMATE EXTRACTION SESSION STATISTICS 🚀")
        logger.info("="*80)
        logger.info(f"📹 Total Videos Analyzed: {self.session_stats['total_videos_analyzed']}")
        logger.info(f"📁 Videos with Valid Coupons: {len(result.videos)}")
        logger.info(f"🎯 Total Coupons Found: {result.total_coupons_found}")
        logger.info("")
        logger.info("📊 BREAKDOWN BY SOURCE:")
        logger.info(f"   🔍 YouTube Keyword Search: {result.total_coupons_found - self.session_stats.get('web_scraped_coupons', 0) - self.session_stats.get('cross_platform_coupons', 0)}")
        logger.info(f"   📺 Channel Traversal Videos: {self.session_stats.get('channel_traversal_videos', 0)}")
        logger.info(f"   🌐 Web Scraped Coupons: {self.session_stats.get('web_scraped_coupons', 0)}")
        logger.info(f"   🔗 Cross-Platform Coupons: {self.session_stats.get('cross_platform_coupons', 0)}")
        logger.info("")
        logger.info("🛡️ DUPLICATE DETECTION:")
        logger.info(f"   ❌ False Positives Prevented: {self.session_stats['false_positives_prevented']}")
        logger.info(f"   🆕 New Coupons Added: {self.session_stats.get('incremental_new_coupons', 0)}")
        logger.info(f"   🔑 Unique Code-Brand Combinations: {len(self.processed_combinations)}")

        if self.enable_persistent_data and hasattr(self, 'data_manager'):
            logger.info("")
            logger.info("💾 PERSISTENT DATA STATS:")
            summary = self.data_manager.get_existing_coupon_summary()
            logger.info(f"   📋 Total Unique Codes in Database: {summary['unique_codes']}")
            logger.info(f"   🏢 Total Unique Brands: {summary['unique_brands']}")
            logger.info(f"   📂 Total Categories: {summary['unique_categories']}")

        if result.videos:
            # Enhanced analytics
            brand_counter = Counter()
            category_counter = Counter()
            source_counter = Counter()

            for video in result.videos:
                for coupon in video.coupons:
                    brand_counter[coupon.brand] += 1
                    category_counter[coupon.category] += 1
                    if hasattr(coupon, 'channel_name'):
                        if 'Web Scraping' in coupon.channel_name:
                            source_counter['Web Scraping'] += 1
                        elif 'Cross-Platform' in coupon.channel_name:
                            source_counter['Cross-Platform'] += 1
                        else:
                            source_counter['YouTube'] += 1

            logger.info("")
            logger.info("📈 SOURCE DISTRIBUTION:")
            for source, count in source_counter.most_common():
                logger.info(f"   {source}: {count} coupons")

            logger.info("")
            logger.info("🏆 TOP BRANDS (Top 15):")
            for brand, count in brand_counter.most_common(15):
                logger.info(f"   {brand}: {count} coupons")

            logger.info("")
            logger.info("📂 CATEGORY DISTRIBUTION:")
            for category, count in category_counter.most_common():
                logger.info(f"   {category}: {count} coupons")

        logger.info("="*80)
        logger.info("🎉 ULTIMATE EXTRACTION COMPLETED SUCCESSFULLY! 🎉")
        logger.info("="*80)

# Usage example
if __name__ == "__main__":
    # Example usage
    API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"  # Replace with actual API key
    
    engine = ImprovedCouponEngine(api_key=API_KEY)
    
    # Run improved extraction
    result = engine.run_improved_extraction()
    
    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f"IMPROVED_COUPON_INTELLIGENCE_{timestamp}.csv"
    engine.export_improved_results(result, filename)
    
    print(f"\nImproved extraction complete! Results saved to {filename}")