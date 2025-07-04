#!/usr/bin/env python3
"""
PERSISTENT DATA MANAGER
Intelligent duplicate detection and incremental data management system
that reads existing CSV files and maintains persistent coupon database.
"""

import os
import pandas as pd
import logging
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
import glob
import json

# Import models
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult

logger = logging.getLogger(__name__)

class PersistentDataManager:
    """
    Advanced data manager for persistent coupon storage with intelligent duplicate detection
    """
    
    def __init__(self, results_directory: str = "results"):
        """Initialize persistent data manager"""
        self.results_directory = results_directory
        self.existing_coupons: Dict[str, Dict] = {}  # code -> {brand: data}
        self.duplicate_stats = {
            'total_processed': 0,
            'true_duplicates_skipped': 0,
            'same_code_different_brand': 0,
            'new_coupons_added': 0
        }
        
        # Ensure results directory exists
        os.makedirs(results_directory, exist_ok=True)
        
        # Load existing data
        self.load_existing_data()
        
        logger.info(f"Persistent Data Manager initialized with {len(self.existing_coupons)} existing coupon codes")
    
    def load_existing_data(self):
        """Load all existing coupon data from CSV files"""
        logger.info("Loading existing coupon data from CSV files...")
        
        # Find all CSV files in results directory
        csv_pattern = os.path.join(self.results_directory, "**", "*.csv")
        csv_files = glob.glob(csv_pattern, recursive=True)
        
        total_loaded = 0
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                
                # Check if this is a coupon results file (has required columns)
                required_columns = ['Coupon Code', 'Brand']
                if not all(col in df.columns for col in required_columns):
                    continue
                
                # Process each row
                for _, row in df.iterrows():
                    coupon_code = str(row.get('Coupon Code', '')).strip()
                    brand = str(row.get('Brand', '')).strip()
                    
                    if coupon_code and brand and coupon_code != 'nan' and brand != 'nan':
                        # Normalize code and brand for comparison
                        code_key = coupon_code.upper()
                        brand_key = brand.title()
                        
                        if code_key not in self.existing_coupons:
                            self.existing_coupons[code_key] = {}
                        
                        # Store full row data for this code-brand combination
                        self.existing_coupons[code_key][brand_key] = {
                            'coupon_code': coupon_code,
                            'brand': brand,
                            'coupon_title': row.get('Coupon Title', ''),
                            'discount_percent': row.get('Discount Percent', ''),
                            'expiry_date': row.get('Expiry Date', ''),
                            'description': row.get('Discount Description', ''),
                            'category': row.get('Category', ''),
                            'channel': row.get('YouTuber Channel', ''),
                            'source_file': csv_file,
                            'loaded_at': datetime.now().isoformat()
                        }
                        total_loaded += 1
                
                logger.info(f"Loaded {len(df)} entries from {os.path.basename(csv_file)}")
                
            except Exception as e:
                logger.error(f"Error loading CSV file {csv_file}: {e}")
                continue
        
        logger.info(f"Total existing coupons loaded: {total_loaded}")
        logger.info(f"Unique coupon codes: {len(self.existing_coupons)}")
    
    def is_duplicate(self, coupon_code: str, brand: str) -> Tuple[bool, str]:
        """
        Check if a coupon is a true duplicate (same code AND brand)
        Returns (is_duplicate, reason)
        """
        code_key = coupon_code.upper().strip()
        brand_key = brand.title().strip()
        
        if code_key in self.existing_coupons:
            if brand_key in self.existing_coupons[code_key]:
                # True duplicate: same code AND same brand
                return True, f"Duplicate: {coupon_code} for {brand} already exists"
            else:
                # Same code but different brand - NOT a duplicate
                existing_brands = list(self.existing_coupons[code_key].keys())
                return False, f"Same code {coupon_code} exists for different brands: {existing_brands}"
        
        # Completely new coupon
        return False, "New coupon"
    
    def add_coupon_to_memory(self, coupon: CouponInfo, source_info: str = "current_run"):
        """Add a coupon to in-memory storage for duplicate checking"""
        code_key = coupon.coupon_code.upper().strip()
        brand_key = coupon.brand.title().strip()
        
        if code_key not in self.existing_coupons:
            self.existing_coupons[code_key] = {}
        
        self.existing_coupons[code_key][brand_key] = {
            'coupon_code': coupon.coupon_code,
            'brand': coupon.brand,
            'coupon_title': coupon.coupon_name,
            'discount_percent': f"{coupon.percent_off}%" if coupon.percent_off else '',
            'expiry_date': coupon.expiry_date,
            'description': coupon.description,
            'category': coupon.category,
            'channel': getattr(coupon, 'channel_name', ''),
            'source_info': source_info,
            'added_at': datetime.now().isoformat()
        }
    
    def filter_duplicates(self, coupons: List[CouponInfo]) -> List[CouponInfo]:
        """
        Filter out true duplicates from a list of coupons
        Only removes coupons with same code AND same brand
        """
        filtered_coupons = []
        
        for coupon in coupons:
            self.duplicate_stats['total_processed'] += 1
            
            is_dup, reason = self.is_duplicate(coupon.coupon_code, coupon.brand)
            
            if is_dup:
                self.duplicate_stats['true_duplicates_skipped'] += 1
                logger.debug(f"Skipping duplicate: {coupon.coupon_code} - {coupon.brand}")
            else:
                if "different brands" in reason:
                    self.duplicate_stats['same_code_different_brand'] += 1
                    logger.info(f"Adding same code with different brand: {coupon.coupon_code} - {coupon.brand}")
                else:
                    self.duplicate_stats['new_coupons_added'] += 1
                
                # Add to memory for future duplicate checking in this session
                self.add_coupon_to_memory(coupon)
                filtered_coupons.append(coupon)
        
        return filtered_coupons
    
    def get_latest_results_file(self) -> Optional[str]:
        """Get the path to the most recent results file"""
        csv_pattern = os.path.join(self.results_directory, "**", "IMPROVED_COUPON_RESULTS_*.csv")
        csv_files = glob.glob(csv_pattern, recursive=True)
        
        if not csv_files:
            return None
        
        # Sort by modification time, get most recent
        csv_files.sort(key=os.path.getmtime, reverse=True)
        return csv_files[0]
    
    def append_to_existing_file(self, new_coupons: List[CouponInfo], target_file: str = None) -> str:
        """
        Append new coupons to existing results file or create new one
        """
        if not new_coupons:
            logger.warning("No new coupons to append")
            return ""
        
        # Determine target file
        if not target_file:
            target_file = self.get_latest_results_file()
        
        # Prepare new data
        new_rows = []
        for coupon in new_coupons:
            row = {
                'Coupon Title': coupon.coupon_name or 'N/A',
                'Coupon Code': coupon.coupon_code or 'N/A',
                'Brand': coupon.brand or 'N/A',
                'Discount Percent': f"{coupon.percent_off}%" if coupon.percent_off else 'N/A',
                'Expiry Date': coupon.expiry_date or 'N/A',
                'Discount Description': coupon.description or 'N/A',
                'Category': coupon.category or 'N/A',
                'YouTuber Channel': getattr(coupon, 'channel_name', 'N/A'),
                'Extraction Confidence': f"{coupon.extraction_confidence:.2f}" if hasattr(coupon, 'extraction_confidence') else 'N/A',
                'Video ID': coupon.video_id or 'N/A'
            }
            new_rows.append(row)
        
        new_df = pd.DataFrame(new_rows)
        
        if target_file and os.path.exists(target_file):
            # Append to existing file
            try:
                existing_df = pd.read_csv(target_file)
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                
                # Remove any duplicates that might have slipped through
                combined_df = combined_df.drop_duplicates(subset=['Coupon Code', 'Brand'], keep='first')
                
                combined_df.to_csv(target_file, index=False)
                logger.info(f"Appended {len(new_df)} new coupons to existing file: {target_file}")
                return target_file
                
            except Exception as e:
                logger.error(f"Error appending to existing file {target_file}: {e}")
                # Fall through to create new file
        
        # Create new file
        today = datetime.now().strftime("%Y%m%d")
        timestamp = datetime.now().strftime("%H%M")
        new_filename = os.path.join(
            self.results_directory, 
            f"coupon_intelligence_{today}",
            f"INCREMENTAL_COUPON_RESULTS_{today}_{timestamp}.csv"
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(new_filename), exist_ok=True)
        
        new_df.to_csv(new_filename, index=False)
        logger.info(f"Created new results file with {len(new_df)} coupons: {new_filename}")
        return new_filename
    
    def save_incremental_results(self, result: ScrapingResult, append_to_existing: bool = True) -> str:
        """
        Save results incrementally, filtering duplicates and appending to existing data
        """
        logger.info("Processing incremental results with duplicate filtering...")
        
        # Collect all coupons from the result
        all_coupons = []
        for video in result.videos:
            all_coupons.extend(video.coupons)
        
        if not all_coupons:
            logger.warning("No coupons found in results")
            return ""
        
        # Filter duplicates
        filtered_coupons = self.filter_duplicates(all_coupons)
        
        # Log statistics
        self.log_duplicate_stats()
        
        if not filtered_coupons:
            logger.info("All coupons were duplicates - no new data to save")
            return ""
        
        # Save filtered results
        if append_to_existing:
            filename = self.append_to_existing_file(filtered_coupons)
        else:
            # Create new file
            today = datetime.now().strftime("%Y%m%d")
            timestamp = datetime.now().strftime("%H%M")
            filename = os.path.join(
                self.results_directory,
                f"coupon_intelligence_{today}",
                f"FILTERED_COUPON_RESULTS_{today}_{timestamp}.csv"
            )
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            rows = []
            for coupon in filtered_coupons:
                row = {
                    'Coupon Title': coupon.coupon_name or 'N/A',
                    'Coupon Code': coupon.coupon_code or 'N/A',
                    'Brand': coupon.brand or 'N/A',
                    'Discount Percent': f"{coupon.percent_off}%" if coupon.percent_off else 'N/A',
                    'Expiry Date': coupon.expiry_date or 'N/A',
                    'Discount Description': coupon.description or 'N/A',
                    'Category': coupon.category or 'N/A',
                    'YouTuber Channel': getattr(coupon, 'channel_name', 'N/A'),
                    'Extraction Confidence': f"{coupon.extraction_confidence:.2f}" if hasattr(coupon, 'extraction_confidence') else 'N/A',
                    'Video ID': coupon.video_id or 'N/A'
                }
                rows.append(row)
            
            df = pd.DataFrame(rows)
            df.to_csv(filename, index=False)
            logger.info(f"Saved {len(filtered_coupons)} new coupons to: {filename}")
        
        return filename
    
    def log_duplicate_stats(self):
        """Log comprehensive duplicate detection statistics"""
        stats = self.duplicate_stats
        logger.info("="*60)
        logger.info("DUPLICATE DETECTION STATISTICS")
        logger.info("="*60)
        logger.info(f"Total coupons processed: {stats['total_processed']}")
        logger.info(f"True duplicates skipped: {stats['true_duplicates_skipped']}")
        logger.info(f"Same code, different brand (kept): {stats['same_code_different_brand']}")
        logger.info(f"New coupons added: {stats['new_coupons_added']}")
        
        if stats['total_processed'] > 0:
            duplicate_rate = (stats['true_duplicates_skipped'] / stats['total_processed']) * 100
            logger.info(f"Duplicate rate: {duplicate_rate:.1f}%")
        
        logger.info("="*60)
    
    def get_existing_coupon_summary(self) -> Dict:
        """Get summary of existing coupon data"""
        total_codes = len(self.existing_coupons)
        total_entries = sum(len(brands) for brands in self.existing_coupons.values())
        
        # Count brands and categories
        all_brands = set()
        all_categories = set()
        
        for code_data in self.existing_coupons.values():
            for brand_data in code_data.values():
                all_brands.add(brand_data['brand'])
                if brand_data.get('category'):
                    all_categories.add(brand_data['category'])
        
        return {
            'unique_codes': total_codes,
            'total_entries': total_entries,
            'unique_brands': len(all_brands),
            'unique_categories': len(all_categories),
            'brands': sorted(list(all_brands)),
            'categories': sorted(list(all_categories))
        }
    
    def reset_session_stats(self):
        """Reset duplicate statistics for a new session"""
        self.duplicate_stats = {
            'total_processed': 0,
            'true_duplicates_skipped': 0,
            'same_code_different_brand': 0,
            'new_coupons_added': 0
        }
