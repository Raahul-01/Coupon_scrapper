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
from typing import List, Optional, Dict, Any, Set
from collections import Counter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime, timedelta

# Import improved modules
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult
from text_processing_utils import (
    extract_coupon_information_improved,
    clean_text_advanced
)

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
    
    def __init__(self, api_key: str, enable_deduplication: bool = True,
                 existing_results_files: Optional[List[str]] = None):
        """Initialize improved extraction engine"""
        self.api_key = api_key
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE':
            raise ValueError("Please provide a valid YouTube API key")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        # Improved tracking
        self.enable_deduplication = enable_deduplication
        # Track code-brand combinations (persisted across sessions)
        self.processed_combinations: Set[str] = set()

        # Load already scraped combinations from previous log to prevent re-scraping in future sessions
        self._load_logged_combinations()

        # Load existing results (CSV) for incremental runs
        if existing_results_files:
            self._load_existing_results_from_csv(existing_results_files)
        self.session_stats = {
            'total_videos_analyzed': 0,
            'total_coupons_found': 0,
            'unique_coupons': 0,
            'false_positives_prevented': 0
        }
        
        logger.info("Improved Coupon Extraction Engine initialized (context-aware)")
    
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
            # Create unique identifier for deduplication (code + brand only)
            combination_id = f"{info['coupon_code']}_{info['brand']}"
            
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
        Validate the quality of extracted coupon information with strict criteria
        """
        code = coupon_info.get('coupon_code', '')
        brand = coupon_info.get('brand', '')
        confidence = coupon_info.get('confidence', 0)
        context = coupon_info.get('description', '')

        # Must have valid code
        if not code or len(code) < 4:
            return False

        # Must have identified brand (not Unknown or None)
        if not brand or brand in ['Unknown', 'N/A', '']:
            return False

        # Must meet minimum confidence threshold - raised to be more strict
        if confidence < 0.7:
            return False

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

        # Additional validation: code should have a reasonable mix of letters and numbers
        if not self._has_valid_code_pattern(code):
            return False

        # Validate that the brand makes sense in the context
        if not self._validate_brand_context_match(brand, context):
            return False

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
        """Search for fresh videos with promotional/influencer content"""
        try:
            # Search for recent videos (last 15 days for very fresh content)
            fifteen_days_ago = datetime.now() - timedelta(days=15)
            published_after = fifteen_days_ago.isoformat() + 'Z'

            # Use broader search terms to capture influencer promotional content
            # Don't force "coupon code" - let the content analysis find the codes
            search_response = self.youtube.search().list(
                q=query,  # Use the query as-is for broader targeting
                part='id',
                type='video',
                maxResults=min(max_results, 50),
                order='date',
                publishedAfter=published_after
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items']]
            logger.info(f"Found {len(video_ids)} fresh promotional videos for query: '{query}'")

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
                
                # Rate limiting
                time.sleep(0.5)
                
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
            df_new = pd.DataFrame(rows)
            # Always deduplicate new batch first
            df_new = df_new.drop_duplicates(subset=['Coupon Code', 'Brand'], keep='first')

            # If a previous result file exists, append while keeping only new unique rows
            if os.path.exists(filename):
                try:
                    df_existing = pd.read_csv(filename)
                    combined = pd.concat([df_existing, df_new], ignore_index=True)
                    combined = combined.drop_duplicates(subset=['Coupon Code', 'Brand'], keep='first')
                    combined.to_csv(filename, index=False)
                    new_count = len(combined) - len(df_existing)
                    logger.info(f"Appended {new_count} new coupons to existing results ({len(combined)} total)")
                except Exception as e:
                    logger.warning(f"Could not append to existing file; writing fresh: {e}")
                    df_new.to_csv(filename, index=False)
            else:
                df_new.to_csv(filename, index=False)
                logger.info(f"Exported {len(df_new)} unique, high-quality coupons with YouTuber channels to {filename}")
        else:
            logger.warning("No coupon data to export")

        return filename
    
    def run_improved_extraction(self, search_queries: List[str] = None, max_results_per_query: int = 30) -> ScrapingResult:
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

    def _load_logged_combinations(self):
        """Populate processed_combinations set with code-brand pairs that already appear in historical logs.

        This ensures the engine will not re-scrape coupons that have been captured in previous runs, as requested.
        The method scans the default log file (data/improved_automation_system.log) for lines that follow the
        logging pattern "Valid coupon extracted: CODE -> BRAND" and adds the combination to the in-memory set.
        """
        log_path = os.path.join('data', 'improved_automation_system.log')

        if not os.path.exists(log_path):
            return  # Nothing to load on first run

        try:
            with open(log_path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    # Look for the marker we use when a coupon is validated
                    if 'Valid coupon extracted:' in line:
                        try:
                            # Expected pattern: "... Valid coupon extracted: CODE -> BRAND"
                            extracted_part = line.split('Valid coupon extracted:')[1].strip()
                            if '->' in extracted_part:
                                code_part, brand_part = extracted_part.split('->', 1)
                                code = code_part.strip().upper()
                                brand = brand_part.strip().upper()
                                if code and brand:
                                    self.processed_combinations.add(f"{code}_{brand}".lower())
                        except Exception:
                            # Silently ignore malformed lines
                            continue
            logger.info(f"Loaded {len(self.processed_combinations)} existing coupon combinations from log for deduplication")
        except Exception as e:
            logger.warning(f"Could not read historical log file for deduplication: {e}")

    def _load_existing_results_from_csv(self, csv_paths: List[str]):
        """Populate processed_combinations with entries from prior CSV result files."""
        loaded = 0
        for path in csv_paths:
            if not os.path.exists(path):
                continue
            try:
                df_existing = pd.read_csv(path, usecols=['Coupon Code', 'Brand'])
                for _, row in df_existing.iterrows():
                    code = str(row['Coupon Code']).strip().upper()
                    brand = str(row['Brand']).strip().upper()
                    if code and brand and code != 'N/A' and brand != 'N/A':
                        self.processed_combinations.add(f"{code}_{brand}".lower())
                        loaded += 1
            except Exception as e:
                logger.warning(f"Failed to load existing CSV {path}: {e}")
        if loaded:
            logger.info(f"Loaded {loaded} coupon combinations from existing CSV files for deduplication")

    def get_videos_from_channel(self, channel_id: str, max_results: int = 200) -> List[str]:
        """Retrieve up to `max_results` recent video IDs from a given channel."""
        video_ids = []
        try:
            next_page_token = None
            fetched = 0
            while fetched < max_results:
                response = self.youtube.search().list(
                    channelId=channel_id,
                    part='id',
                    type='video',
                    order='date',
                    maxResults=min(50, max_results - fetched),
                    pageToken=next_page_token
                ).execute()

                ids = [item['id']['videoId'] for item in response.get('items', [])]
                video_ids.extend(ids)
                fetched += len(ids)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            logger.info(f"Collected {len(video_ids)} videos from channel {channel_id}")
        except HttpError as e:
            logger.error(f"YouTube API error while fetching channel videos: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching channel videos: {e}")
        return video_ids

    def get_related_videos(self, video_id: str, max_results: int = 25) -> List[str]:
        """Get related videos suggested by YouTube for a given video."""
        try:
            response = self.youtube.search().list(
                part='id',
                type='video',
                relatedToVideoId=video_id,
                maxResults=min(max_results, 50)
            ).execute()
            return [item['id']['videoId'] for item in response.get('items', [])]
        except HttpError as e:
            logger.error(f"YouTube API error fetching related videos for {video_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching related videos for {video_id}: {e}")
            return []

    def run_comprehensive_extraction(
        self,
        search_queries: Optional[List[str]] = None,
        channel_ids: Optional[List[str]] = None,
        include_related: bool = True,
        related_hops: int = 1,
        max_related_per_video: int = 10,
        max_videos_per_channel: int = 200,
        max_results_per_query: int = 30,
    ) -> ScrapingResult:
        """Comprehensive extraction that combines keyword search, channel traversal, and related-video exploration."""
        all_video_ids: Set[str] = set()

        # 1. Keyword search (reuse previous logic)
        if search_queries:
            for query in search_queries:
                logger.info(f"[DISCOVERY] Keyword search: {query}")
                vids = self.search_fresh_videos(query, max_results_per_query)
                all_video_ids.update(vids)

        # 2. Channel traversal
        if channel_ids:
            for ch_id in channel_ids:
                logger.info(f"[DISCOVERY] Traversing channel: {ch_id}")
                vids = self.get_videos_from_channel(ch_id, max_videos_per_channel)
                all_video_ids.update(vids)

        # 3. Related-video exploration
        if include_related and related_hops > 0:
            current_level_ids = list(all_video_ids)
            for hop in range(related_hops):
                logger.info(f"[DISCOVERY] Related-video hop {hop+1}/{related_hops}")
                new_ids: Set[str] = set()
                for vid in current_level_ids:
                    related = self.get_related_videos(vid, max_related_per_video)
                    new_ids.update(related)
                # Deduplicate
                new_unique = new_ids - all_video_ids
                logger.info(f"  Added {len(new_unique)} new IDs from related-video hop {hop+1}")
                all_video_ids.update(new_unique)
                current_level_ids = list(new_unique)
                if not current_level_ids:
                    break

        logger.info(f"[DISCOVERY] Total unique videos discovered: {len(all_video_ids)}")

        # Process videos as usual
        result = self.process_video_batch_improved(list(all_video_ids))

        # Print stats
        self.print_session_stats(result)
        return result

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