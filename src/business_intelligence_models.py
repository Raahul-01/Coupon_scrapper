#!/usr/bin/env python3
"""
BUSINESS INTELLIGENCE MODELS
Professional data structures for coupon automation system
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class CouponInfo:
    """
    Professional Coupon Information Model
    Contains all 7 key fields for business intelligence
    """
    # Core 7 Key Fields
    coupon_code: Optional[str] = None
    coupon_name: Optional[str] = None  # Professional title
    brand: Optional[str] = None
    percent_off: Optional[float] = None
    expiry_date: Optional[str] = None
    description: Optional[str] = None  # Clean description
    category: Optional[str] = None
    
    # Additional Business Intelligence Fields
    discount_amount: Optional[float] = None
    terms_conditions: Optional[str] = None
    minimum_purchase: Optional[float] = None
    video_id: Optional[str] = None
    video_title: Optional[str] = None
    extracted_text: Optional[str] = None
    
    # Intelligence Metadata
    extraction_confidence: Optional[float] = None
    processing_timestamp: Optional[str] = field(default_factory=lambda: datetime.now().isoformat())
    intelligence_score: Optional[float] = None
    
    def __post_init__(self):
        """Post-initialization validation and intelligence scoring"""
        # Calculate intelligence score based on field completeness
        fields_filled = sum([
            bool(self.coupon_code),
            bool(self.coupon_name),
            bool(self.brand),
            bool(self.percent_off),
            bool(self.expiry_date),
            bool(self.description),
            bool(self.category)
        ])
        self.intelligence_score = (fields_filled / 7.0) * 100.0
        
        # Set default category if not provided
        if not self.category:
            self.category = 'general'
        
        # Set default brand if not provided
        if not self.brand:
            self.brand = 'N/A'

@dataclass
class VideoInfo:
    """
    Professional Video Information Model
    Contains comprehensive video metadata and associated coupons
    """
    video_id: str
    title: str = ""
    description: str = ""
    channel_title: str = ""
    published_at: str = ""
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    coupons: List[CouponInfo] = field(default_factory=list)
    
    # Business Intelligence Metadata
    processing_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    content_quality_score: Optional[float] = None
    coupon_density: Optional[float] = None
    
    def __post_init__(self):
        """Post-initialization intelligence calculations"""
        # Calculate content quality score
        quality_factors = [
            min(len(self.title) / 50.0, 1.0),  # Title completeness
            min(len(self.description) / 500.0, 1.0),  # Description completeness
            min(self.view_count / 10000.0, 1.0),  # View popularity
            min(len(self.coupons) / 5.0, 1.0)  # Coupon richness
        ]
        self.content_quality_score = (sum(quality_factors) / len(quality_factors)) * 100.0
        
        # Calculate coupon density (coupons per 100 words)
        if self.description:
            word_count = len(self.description.split())
            self.coupon_density = (len(self.coupons) / max(word_count, 1)) * 100.0
        else:
            self.coupon_density = 0.0

@dataclass
class ScrapingResult:
    """
    Professional Processing Result Model
    Contains comprehensive processing results and business intelligence
    """
    videos: List[VideoInfo] = field(default_factory=list)
    total_videos_processed: int = 0
    total_coupons_found: int = 0
    processing_time: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    # Business Intelligence Metrics
    processing_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    average_quality_score: Optional[float] = None
    average_intelligence_score: Optional[float] = None
    category_distribution: Dict[str, int] = field(default_factory=dict)
    brand_distribution: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization business intelligence calculations"""
        self.calculate_business_intelligence()
    
    def calculate_business_intelligence(self):
        """Calculate comprehensive business intelligence metrics"""
        if not self.videos:
            return
        
        # Calculate average quality scores
        quality_scores = [video.content_quality_score for video in self.videos if video.content_quality_score]
        self.average_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        # Calculate average intelligence scores
        all_coupons = [coupon for video in self.videos for coupon in video.coupons]
        intelligence_scores = [coupon.intelligence_score for coupon in all_coupons if coupon.intelligence_score]
        self.average_intelligence_score = sum(intelligence_scores) / len(intelligence_scores) if intelligence_scores else 0.0
        
        # Calculate category distribution
        self.category_distribution = {}
        for coupon in all_coupons:
            category = coupon.category or 'general'
            self.category_distribution[category] = self.category_distribution.get(category, 0) + 1
        
        # Calculate brand distribution
        self.brand_distribution = {}
        for coupon in all_coupons:
            brand = coupon.brand or 'unknown'
            self.brand_distribution[brand] = self.brand_distribution.get(brand, 0) + 1
