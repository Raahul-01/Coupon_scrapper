#!/usr/bin/env python3
"""
PROFESSIONAL COUPON EXTRACTION ENGINE
Enterprise-grade YouTube content analysis and coupon intelligence platform
"""

import os
import time
import logging
import json
from typing import List, Optional, Dict, Any, Set
from collections import Counter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime

# Import professional modules
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult
from text_processing_utils import (
    clean_text, extract_coupon_codes, extract_percentage_discounts,
    extract_amount_discounts, extract_brands, extract_categories,
    extract_expiry_dates, extract_minimum_purchase, extract_terms_conditions,
    find_coupon_context, score_coupon_relevance, split_description_into_sections
)

# Import settings
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.application_settings import (
    YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    MAX_RESULTS_PER_REQUEST, REQUEST_TIMEOUT, RATE_LIMIT_DELAY,
    COUPON_PATTERNS, COMMON_BRANDS, CATEGORY_KEYWORDS
)

# Professional logging setup
os.makedirs('data', exist_ok=True)  # Create data directory if it doesn't exist
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/automation_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProfessionalCouponEngine:
    """
    Professional Coupon Extraction Engine
    
    Enterprise Features:
    - Complete content intelligence analysis
    - Smart duplicate prevention system
    - 7 key field extraction with AI
    - Broad market coverage automation
    - Professional business intelligence
    """
    
    def __init__(self, api_key: Optional[str] = None, enable_smart_features: bool = True):
        """Initialize professional extraction engine"""
        self.api_key = api_key or YOUTUBE_API_KEY
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE':
            raise ValueError("Please configure YouTube API key in config/application_settings.py")
        
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=self.api_key
        )
        
        # Professional intelligence features
        self.enable_smart_features = enable_smart_features
        self.intelligence_tracking_file = "data/content_intelligence_history.json"
        self.processed_videos: Set[str] = set()
        self.processed_coupons: Set[str] = set()
        
        if enable_smart_features:
            self.load_intelligence_history()
        
        logger.info("Professional Coupon Extraction Engine initialized successfully")
    
    def load_intelligence_history(self):
        """Load content intelligence history"""
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(self.intelligence_tracking_file):
            try:
                with open(self.intelligence_tracking_file, 'r') as f:
                    history = json.load(f)
                    self.processed_videos = set(history.get('videos', []))
                    self.processed_coupons = set(history.get('coupons', []))
                    logger.info(f"Intelligence history loaded: {len(self.processed_videos)} videos, {len(self.processed_coupons)} coupons")
            except Exception as e:
                logger.warning(f"Error loading intelligence history: {e}")
                self.processed_videos = set()
                self.processed_coupons = set()
        else:
            logger.info("No previous intelligence history found - starting fresh analysis")
    
    def save_intelligence_history(self):
        """Save content intelligence history"""
        os.makedirs("data", exist_ok=True)
        
        history = {
            'videos': list(self.processed_videos),
            'coupons': list(self.processed_coupons),
            'last_updated': datetime.now().isoformat(),
            'total_sessions': len(self.processed_videos)
        }
        
        with open(self.intelligence_tracking_file, 'w') as f:
            json.dump(history, f, indent=2)
        logger.info(f"Intelligence history saved: {len(self.processed_videos)} videos, {len(self.processed_coupons)} coupons")
    
    def get_comprehensive_market_keywords(self) -> List[str]:
        """Get comprehensive market keyword intelligence"""
        return [
            # E-commerce Intelligence
            "coupon codes", "discount codes", "promo codes", "voucher codes", "offer codes",
            "deals today", "sale offers", "savings deals", "cashback offers", "rebate codes",
            "markdown prices", "clearance sale", "bargain deals", "cheap prices", "affordable deals",
            "budget offers", "low price deals", "best price offers", "free shipping codes",
            "free delivery offers", "buy one get one", "bogo deals", "half price offers",
            
            # Platform Intelligence
            "amazon deals", "flipkart offers", "myntra coupons", "nykaa discounts",
            "ajio codes", "meesho deals", "snapdeal offers", "paytm coupons",
            "ebay deals", "walmart offers", "target coupons", "bestbuy discounts",
            
            # Fashion Intelligence
            "fashion deals", "clothing discounts", "shoe offers", "accessories coupons",
            "jewelry deals", "watch discounts", "bag offers", "style codes",
            "designer deals", "branded clothes", "luxury fashion", "trendy offers",
            
            # Electronics Intelligence
            "electronics deals", "mobile offers", "laptop discounts", "gadget coupons",
            "tech deals", "smartphone offers", "computer discounts", "gaming codes",
            "tablet deals", "headphone offers", "speaker discounts", "camera coupons",
            
            # Food Intelligence
            "food delivery codes", "restaurant coupons", "zomato offers", "swiggy deals",
            "pizza discounts", "burger offers", "coffee coupons", "meal deals",
            "grocery codes", "food offers", "dining deals", "takeaway coupons",
            
            # Travel Intelligence
            "travel deals", "flight discounts", "hotel offers", "booking coupons",
            "vacation deals", "trip discounts", "makemytrip offers", "goibibo codes",
            "airbnb deals", "uber coupons", "ola offers", "cab discounts",
            
            # Beauty Intelligence
            "beauty deals", "cosmetics offers", "skincare discounts", "makeup coupons",
            "perfume deals", "grooming offers", "salon discounts", "spa codes",
            "haircare deals", "nail offers", "fragrance discounts", "wellness coupons",
            
            # Home Intelligence
            "home deals", "furniture discounts", "appliance offers", "decor coupons",
            "kitchen deals", "bedroom offers", "living room discounts", "garden codes",
            "cleaning deals", "storage offers", "lighting discounts", "textile coupons",
            
            # Health Intelligence
            "health deals", "fitness offers", "gym discounts", "supplement coupons",
            "medical deals", "pharmacy offers", "wellness discounts", "nutrition codes",
            "protein deals", "vitamin offers", "medicine discounts", "healthcare coupons",
            
            # Entertainment Intelligence
            "entertainment deals", "movie offers", "music discounts", "streaming coupons",
            "gaming deals", "book offers", "magazine discounts", "subscription codes",
            "netflix deals", "spotify offers", "youtube premium", "amazon prime deals"
        ]
    
    def search_content(self, query: str, max_results: int = 50) -> List[str]:
        """Professional content search with intelligence"""
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id',
                type='video',
                maxResults=min(max_results, MAX_RESULTS_PER_REQUEST),
                order='relevance',
                publishedAfter=(datetime.now().replace(day=1).isoformat() + 'Z')  # This month only
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response['items']]
            logger.info(f"Content search completed: {len(video_ids)} videos for '{query}'")
            return video_ids
            
        except HttpError as e:
            logger.error(f"YouTube API error for query '{query}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in content search: {e}")
            return []
    
    def get_fresh_content(self, query: str, max_results: int = 30) -> List[str]:
        """Get fresh content IDs with intelligence filtering"""
        if not self.enable_smart_features:
            return self.search_content(query, max_results)
        
        logger.info(f"Intelligence search for fresh content: '{query}'")
        
        # Get all content for this query
        all_content_ids = self.search_content(query, max_results * 2)
        
        # Filter out already processed content
        fresh_content_ids = [vid for vid in all_content_ids if vid not in self.processed_videos]
        
        # Limit to requested amount
        fresh_content = fresh_content_ids[:max_results]
        
        logger.info(f"Content intelligence: {len(all_content_ids)} total, {len(fresh_content)} fresh")
        
        return fresh_content
    
    def process_content_batch(self, video_ids: List[str]) -> ScrapingResult:
        """Process batch of videos with professional intelligence"""
        result = ScrapingResult()
        
        for i, video_id in enumerate(video_ids):
            try:
                logger.info(f"Processing content {i+1}/{len(video_ids)}: {video_id}")
                
                # Get video details
                video_info = self.get_content_details(video_id)
                if not video_info:
                    continue
                
                # Professional analysis of complete description
                analyzed_coupons = self.analyze_complete_description(
                    video_info.description,
                    video_info.title,
                    video_info.video_id
                )
                
                if analyzed_coupons:
                    video_info.coupons = analyzed_coupons
                    result.videos.append(video_info)
                    result.total_coupons_found += len(analyzed_coupons)
                    
                    logger.info(f"Professional analysis: {len(analyzed_coupons)} coupons with complete intelligence")
                
                result.total_videos_processed += 1
                time.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error processing content {video_id}: {e}")
                continue
        
        return result
    
    def apply_intelligence_filtering(self, result: ScrapingResult) -> ScrapingResult:
        """Apply professional intelligence filtering"""
        if not self.enable_smart_features:
            return result
        
        filtered_result = ScrapingResult()
        filtered_result.total_videos_processed = result.total_videos_processed
        
        new_coupons_count = 0
        duplicate_coupons_count = 0
        
        for video in result.videos:
            new_video_coupons = []
            
            for coupon in video.coupons:
                # Create unique identifier for coupon
                coupon_id = f"{coupon.coupon_code}_{coupon.brand}_{coupon.category}".lower()
                
                if coupon_id not in self.processed_coupons and coupon.coupon_code:
                    # This is new intelligence
                    new_video_coupons.append(coupon)
                    self.processed_coupons.add(coupon_id)
                    new_coupons_count += 1
                else:
                    duplicate_coupons_count += 1
            
            if new_video_coupons:
                # Create new video with intelligence
                new_video = VideoInfo(
                    video_id=video.video_id,
                    title=video.title,
                    description=video.description,
                    channel_title=video.channel_title,
                    published_at=video.published_at,
                    view_count=video.view_count,
                    coupons=new_video_coupons
                )
                filtered_result.videos.append(new_video)
            
            # Mark content as processed
            self.processed_videos.add(video.video_id)
        
        filtered_result.total_coupons_found = new_coupons_count
        
        logger.info(f"Intelligence filtering: {new_coupons_count} new, {duplicate_coupons_count} duplicates")
        
        return filtered_result
    
    def export_professional_intelligence(self, result: ScrapingResult, filename: str) -> str:
        """Export professional intelligence with 7 key fields"""
        
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
                    'Category': coupon.category or 'N/A'
                }
                rows.append(row)

        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(filename, index=False)
            logger.info(f"✅ Professional intelligence exported: {len(rows)} coupons with 7 KEY FIELDS to {filename}")
        else:
            logger.warning("⚠️ No coupon intelligence found to export")
        
        return filename

    def get_content_details(self, video_id: str) -> Optional[VideoInfo]:
        """Get comprehensive content details with intelligence"""
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
            logger.error(f"Error getting content details for {video_id}: {e}")
            return None

    def analyze_complete_description(self, description: str, video_title: str, video_id: str) -> List[CouponInfo]:
        """Professional complete description analysis for all 7 fields"""

        if not description:
            return []

        logger.info(f"Analyzing complete description ({len(description)} chars)...")

        # Extract coupon codes
        coupon_codes = extract_coupon_codes(description)

        if not coupon_codes:
            return []

        logger.info(f"Found {len(coupon_codes)} coupon codes: {coupon_codes}")

        # Analyze each coupon
        analyzed_coupons = []

        for code in coupon_codes:
            # Extract all 7 fields
            percentages = extract_percentage_discounts(description)
            brands = extract_brands(description)
            categories = extract_categories(description)
            expiry_dates = extract_expiry_dates(description)

            # Create professional coupon
            coupon = CouponInfo(
                coupon_code=code,
                coupon_name=f"{percentages[0] if percentages else ''}% OFF {brands[0] if brands else 'Discount'} {categories[0].title() if categories else 'Coupon'}".strip(),
                brand=brands[0] if brands else 'N/A',
                percent_off=float(percentages[0]) if percentages else None,
                expiry_date=expiry_dates[0] if expiry_dates else 'N/A',
                description=description[:200] + "..." if len(description) > 200 else description,
                category=categories[0] if categories else 'general',
                video_id=video_id,
                video_title=video_title
            )
            analyzed_coupons.append(coupon)

        logger.info(f"Successfully analyzed {len(analyzed_coupons)} coupons")
        return analyzed_coupons
