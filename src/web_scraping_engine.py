#!/usr/bin/env python3
"""
WEB SCRAPING ENGINE FOR COUPON AGGREGATION
Multi-source coupon scraping from major coupon sites and brand websites
"""

import os
import time
import logging
import requests
import re
from typing import List, Optional, Dict, Any, Set
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta
import json

# Import models
from business_intelligence_models import CouponInfo, VideoInfo, ScrapingResult
from text_processing_utils import extract_coupon_information_improved, clean_text_advanced

logger = logging.getLogger(__name__)

class WebScrapingEngine:
    """
    Advanced web scraping engine for coupon aggregation from multiple sources
    """
    
    def __init__(self, enable_rate_limiting: bool = True):
        """Initialize web scraping engine"""
        self.enable_rate_limiting = enable_rate_limiting
        self.session = requests.Session()
        
        # Rotate user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]
        
        # Major coupon aggregator sites
        self.coupon_sites = {
            'retailmenot': {
                'base_url': 'https://www.retailmenot.com',
                'search_url': 'https://www.retailmenot.com/s/{brand}',
                'selectors': {
                    'coupon_container': '.offer-card',
                    'code': '.offer-code',
                    'description': '.offer-description',
                    'brand': '.merchant-name',
                    'discount': '.offer-value'
                }
            },
            'coupons_com': {
                'base_url': 'https://www.coupons.com',
                'search_url': 'https://www.coupons.com/search/{brand}',
                'selectors': {
                    'coupon_container': '.coupon-card',
                    'code': '.coupon-code',
                    'description': '.coupon-title',
                    'brand': '.brand-name',
                    'discount': '.discount-value'
                }
            },
            'groupon': {
                'base_url': 'https://www.groupon.com',
                'search_url': 'https://www.groupon.com/coupons/{brand}',
                'selectors': {
                    'coupon_container': '.deal-tile',
                    'code': '.promo-code',
                    'description': '.deal-title',
                    'brand': '.merchant-name',
                    'discount': '.discount-percent'
                }
            }
        }
        
        # Industry-specific coupon sources
        self.industry_sources = {
            'hosting': [
                'https://www.hostingadvice.com/coupons/',
                'https://www.webhostingsecretrevealed.net/coupons/',
                'https://www.hostingpill.com/coupons/'
            ],
            'fitness': [
                'https://www.supplementreviews.com/coupons/',
                'https://www.bodybuilding.com/store/deals',
                'https://www.iherb.com/specials'
            ],
            'software': [
                'https://www.softwarecoupons.com/',
                'https://www.dealify.com/software-deals',
                'https://www.stacksocial.com/sales'
            ],
            'fashion': [
                'https://www.dealsplus.com/fashion-deals',
                'https://www.shopstyle.com/browse/womens-clothes?fts=sale',
                'https://www.lyst.com/sales/'
            ]
        }
        
        logger.info("Web Scraping Engine initialized with multi-source support")
    
    def get_random_headers(self) -> Dict[str, str]:
        """Get randomized headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_coupon_site(self, site_name: str, brand: str) -> List[Dict[str, Any]]:
        """Scrape coupons from a specific coupon aggregator site"""
        if site_name not in self.coupon_sites:
            logger.warning(f"Unknown coupon site: {site_name}")
            return []
        
        site_config = self.coupon_sites[site_name]
        search_url = site_config['search_url'].format(brand=quote(brand.lower()))
        
        try:
            headers = self.get_random_headers()
            response = self.session.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            coupons = []
            
            # Find coupon containers
            coupon_containers = soup.select(site_config['selectors']['coupon_container'])
            
            for container in coupon_containers[:20]:  # Limit to 20 coupons per site
                try:
                    coupon_data = self.extract_coupon_from_container(container, site_config['selectors'])
                    if coupon_data and self.validate_scraped_coupon(coupon_data):
                        coupon_data['source'] = site_name
                        coupon_data['source_url'] = search_url
                        coupons.append(coupon_data)
                except Exception as e:
                    logger.debug(f"Error extracting coupon from container: {e}")
                    continue
            
            logger.info(f"Scraped {len(coupons)} coupons from {site_name} for brand {brand}")
            return coupons
            
        except Exception as e:
            logger.error(f"Error scraping {site_name} for brand {brand}: {e}")
            return []
    
    def extract_coupon_from_container(self, container, selectors: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Extract coupon information from a container element"""
        try:
            # Extract code
            code_element = container.select_one(selectors.get('code', ''))
            code = code_element.get_text(strip=True) if code_element else None
            
            # Extract description
            desc_element = container.select_one(selectors.get('description', ''))
            description = desc_element.get_text(strip=True) if desc_element else ''
            
            # Extract brand
            brand_element = container.select_one(selectors.get('brand', ''))
            brand = brand_element.get_text(strip=True) if brand_element else 'Unknown'
            
            # Extract discount
            discount_element = container.select_one(selectors.get('discount', ''))
            discount_text = discount_element.get_text(strip=True) if discount_element else ''
            
            # Parse discount percentage
            discount_percent = self.extract_percentage_from_text(discount_text)
            
            # If no explicit code, try to extract from description
            if not code and description:
                code = self.extract_code_from_text(description)
            
            if not code:
                return None
            
            return {
                'coupon_code': code,
                'brand': brand,
                'description': description,
                'percent_off': discount_percent,
                'discount_text': discount_text,
                'extraction_confidence': 0.8
            }
            
        except Exception as e:
            logger.debug(f"Error extracting coupon data: {e}")
            return None
    
    def extract_percentage_from_text(self, text: str) -> Optional[float]:
        """Extract percentage discount from text"""
        if not text:
            return None
        
        # Look for percentage patterns
        patterns = [
            r'(\d{1,2})%\s*(?:off|discount|save)',
            r'(?:save|get|enjoy)\s+(\d{1,2})%',
            r'(\d{1,2})\s*percent\s*off'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    percent = float(match.group(1))
                    if 5 <= percent <= 90:  # Reasonable range
                        return percent
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def extract_code_from_text(self, text: str) -> Optional[str]:
        """Extract coupon code from text description"""
        if not text:
            return None
        
        # Look for code patterns in text
        patterns = [
            r'(?:code|coupon|promo)[\s:]*([A-Z0-9]{3,15})\b',
            r'(?:use|apply|enter)[\s:]*(?:code|coupon)?[\s:]*([A-Z0-9]{3,15})\b',
            r'\b([A-Z]{2,}[0-9]{2,})\b',  # SAVE20, GET50
            r'\b([0-9]{2,}[A-Z]{2,})\b',  # 20OFF, 50SAVE
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                code = match.group(1).upper()
                if self.is_valid_coupon_code(code):
                    return code
        
        return None
    
    def is_valid_coupon_code(self, code: str) -> bool:
        """Validate if extracted text is a valid coupon code"""
        if not code or len(code) < 3 or len(code) > 20:
            return False
        
        # Must be alphanumeric
        if not re.match(r'^[A-Z0-9\-_]+$', code):
            return False
        
        # Exclude common non-codes
        common_non_codes = {
            'SUBSCRIBE', 'COMMENT', 'LIKE', 'SHARE', 'FOLLOW', 'WORKING', 'VERIFIED',
            'TESTED', 'ACTIVE', 'VALID', 'EXPIRED', 'NEW', 'LATEST', 'UPDATE',
            'CODES', 'CODE', 'COUPON', 'PROMO', 'DISCOUNT', 'OFFER', 'DEAL'
        }
        
        return code not in common_non_codes
    
    def validate_scraped_coupon(self, coupon_data: Dict[str, Any]) -> bool:
        """Validate scraped coupon data quality"""
        if not coupon_data.get('coupon_code'):
            return False
        
        code = coupon_data['coupon_code']
        brand = coupon_data.get('brand', '')
        
        # Basic validation
        if not self.is_valid_coupon_code(code):
            return False
        
        # Brand should not be suspicious
        suspicious_brands = {'Unknown', 'Deal', 'Offer', 'Sale', 'Discount', 'Code'}
        if brand in suspicious_brands:
            return False
        
        return True
    
    def scrape_industry_sources(self, industry: str, max_coupons: int = 50) -> List[Dict[str, Any]]:
        """Scrape industry-specific coupon sources"""
        if industry not in self.industry_sources:
            logger.warning(f"Unknown industry: {industry}")
            return []
        
        all_coupons = []
        sources = self.industry_sources[industry]
        
        for source_url in sources:
            try:
                coupons = self.scrape_generic_coupon_page(source_url, industry)
                all_coupons.extend(coupons)
                
                if len(all_coupons) >= max_coupons:
                    break
                
                # Rate limiting
                if self.enable_rate_limiting:
                    time.sleep(random.uniform(1, 3))
                    
            except Exception as e:
                logger.error(f"Error scraping industry source {source_url}: {e}")
                continue
        
        return all_coupons[:max_coupons]
    
    def scrape_generic_coupon_page(self, url: str, category: str) -> List[Dict[str, Any]]:
        """Scrape coupons from a generic coupon page"""
        try:
            headers = self.get_random_headers()
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            page_text = soup.get_text()
            
            # Use existing extraction logic
            coupon_info_list = extract_coupon_information_improved(page_text)
            
            coupons = []
            for info in coupon_info_list:
                coupon_data = {
                    'coupon_code': info['coupon_code'],
                    'brand': info['brand'],
                    'description': info['description'],
                    'percent_off': float(info['percentage']) if info['percentage'] else None,
                    'category': category,
                    'source': 'web_scraping',
                    'source_url': url,
                    'extraction_confidence': info.get('confidence', 0.7)
                }
                
                if self.validate_scraped_coupon(coupon_data):
                    coupons.append(coupon_data)
            
            logger.info(f"Scraped {len(coupons)} coupons from {url}")
            return coupons
            
        except Exception as e:
            logger.error(f"Error scraping generic page {url}: {e}")
            return []
    
    def scrape_brand_specific_coupons(self, brand_list: List[str]) -> List[Dict[str, Any]]:
        """Scrape coupons for specific brands from multiple sources"""
        all_coupons = []
        
        for brand in brand_list:
            logger.info(f"Scraping coupons for brand: {brand}")
            
            # Scrape from major coupon sites
            for site_name in self.coupon_sites.keys():
                try:
                    coupons = self.scrape_coupon_site(site_name, brand)
                    all_coupons.extend(coupons)
                    
                    # Rate limiting between sites
                    if self.enable_rate_limiting:
                        time.sleep(random.uniform(0.5, 2))
                        
                except Exception as e:
                    logger.error(f"Error scraping {site_name} for {brand}: {e}")
                    continue
        
        return all_coupons
    
    def run_comprehensive_scraping(self, target_brands: List[str] = None, target_industries: List[str] = None) -> ScrapingResult:
        """Run comprehensive web scraping across all sources"""
        logger.info("Starting comprehensive web scraping")
        
        result = ScrapingResult()
        all_scraped_coupons = []
        
        # Scrape industry-specific sources
        if target_industries:
            for industry in target_industries:
                logger.info(f"Scraping {industry} industry sources")
                industry_coupons = self.scrape_industry_sources(industry, max_coupons=100)
                all_scraped_coupons.extend(industry_coupons)
        
        # Scrape brand-specific coupons
        if target_brands:
            brand_coupons = self.scrape_brand_specific_coupons(target_brands)
            all_scraped_coupons.extend(brand_coupons)
        
        # Convert to CouponInfo objects and create VideoInfo containers
        processed_coupons = self.convert_scraped_to_coupon_info(all_scraped_coupons)
        
        # Group coupons into video-like containers for compatibility
        if processed_coupons:
            video_info = VideoInfo(
                video_id="web_scraped_batch",
                title="Web Scraped Coupons",
                description="Coupons scraped from various web sources",
                channel_title="Web Scraping Engine",
                published_at=datetime.now().isoformat(),
                view_count=0,
                coupons=processed_coupons
            )
            result.videos.append(video_info)
        
        result.total_videos_processed = 1
        result.total_coupons_found = len(processed_coupons)
        
        logger.info(f"Web scraping completed: {len(processed_coupons)} coupons found")
        return result
    
    def convert_scraped_to_coupon_info(self, scraped_coupons: List[Dict[str, Any]]) -> List[CouponInfo]:
        """Convert scraped coupon data to CouponInfo objects"""
        coupon_objects = []
        
        for coupon_data in scraped_coupons:
            try:
                coupon = CouponInfo(
                    coupon_code=coupon_data['coupon_code'],
                    coupon_name=f"{coupon_data.get('percent_off', '')}% OFF {coupon_data['brand']}" if coupon_data.get('percent_off') else f"{coupon_data['brand']} Discount",
                    brand=coupon_data['brand'],
                    percent_off=coupon_data.get('percent_off'),
                    expiry_date='N/A',
                    description=coupon_data.get('description', '')[:200],
                    category=coupon_data.get('category', 'general'),
                    video_id=coupon_data.get('source_url', 'web_scraped'),
                    video_title=f"Web Scraped from {coupon_data.get('source', 'unknown')}",
                    extraction_confidence=coupon_data.get('extraction_confidence', 0.7)
                )
                coupon.channel_name = f"Web Scraping - {coupon_data.get('source', 'Unknown')}"
                coupon_objects.append(coupon)
                
            except Exception as e:
                logger.error(f"Error converting scraped coupon to CouponInfo: {e}")
                continue
        
        return coupon_objects
