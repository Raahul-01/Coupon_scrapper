#!/usr/bin/env python3
"""
PROFESSIONAL TEXT PROCESSING UTILITIES
Advanced text analysis and extraction functions for coupon intelligence
"""

import re
import logging
from typing import List, Dict, Optional, Tuple, Set
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Professional text cleaning with intelligence"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', text)
    
    # Remove URLs but preserve context
    cleaned = re.sub(r'http[s]?://\S+', ' [LINK] ', cleaned)
    
    # Normalize punctuation
    cleaned = re.sub(r'[!]{2,}', '!', cleaned)
    cleaned = re.sub(r'[?]{2,}', '?', cleaned)
    cleaned = re.sub(r'[.]{3,}', '...', cleaned)
    
    # Remove excessive special characters but keep important ones
    cleaned = re.sub(r'[^\w\s\-\.\,\:\;\!\?\%\$\#\@\&\(\)\[\]]', ' ', cleaned)
    
    # Final cleanup
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def extract_coupon_codes(text: str) -> List[str]:
    """Professional coupon code extraction with intelligence patterns"""
    if not text:
        return []
    
    codes = set()
    
    # Professional extraction patterns
    patterns = [
        # Standard coupon formats
        r'\b([A-Z]{2,}[0-9]{2,})\b',  # SAVE20, GET50
        r'\b([0-9]{2,}[A-Z]{2,})\b',  # 20OFF, 50SAVE
        r'\b([A-Z]+[0-9]+[A-Z]*)\b',  # WELCOME10, NEW25OFF
        
        # Context-based patterns
        r'(?:code|coupon|promo|voucher)[\s:]*([A-Z0-9]{3,15})\b',
        r'(?:use|apply|enter)[\s:]*(?:code|coupon)?[\s:]*([A-Z0-9]{3,15})\b',
        r'\b([A-Z0-9]{4,12})\s*(?:for|to|and)\s*(?:save|get|off)',
        
        # Special format patterns
        r'(?:discount|offer|deal)[\s:]*([A-Z0-9]{3,12})\b',
        r'\b([A-Z]{3,}[0-9]{2,}[A-Z]*)\b',  # SUMMER2024OFF
        r'\b([A-Z0-9]{5,15})\s*(?:at|on|for)\s*(?:checkout|payment)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match[0] else match[1]
            
            code = match.strip().upper()
            # Validate code format
            if 3 <= len(code) <= 20 and code.isalnum() and not code.isdigit():
                codes.add(code)
    
    return list(codes)[:15]  # Limit for quality

def extract_percentage_discounts(text: str) -> List[float]:
    """Professional percentage extraction with intelligence"""
    if not text:
        return []
    
    percentages = []
    
    # Professional percentage patterns
    patterns = [
        r'(\d{1,2})\s*%\s*(?:off|discount|save|reduction)',
        r'(?:save|get|enjoy|receive)\s+(\d{1,2})\s*%',
        r'(\d{1,2})\s*percent\s*(?:off|discount|save)',
        r'(?:up\s+to\s+)?(\d{1,2})\s*%\s*(?:discount|off|save)',
        r'(\d{1,2})\s*%\s*(?:price\s+)?(?:cut|reduction|markdown)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                percent = float(match)
                if 1 <= percent <= 99:  # Reasonable range
                    percentages.append(percent)
            except (ValueError, TypeError):
                continue
    
    # Remove duplicates and sort
    return sorted(list(set(percentages)), reverse=True)

def extract_amount_discounts(text: str) -> List[float]:
    """Professional amount discount extraction"""
    if not text:
        return []
    
    amounts = []
    
    # Professional amount patterns
    patterns = [
        r'(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:off|discount|save)',
        r'(?:save|get|enjoy)\s+(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)',
        r'(\d+(?:\.\d{2})?)\s*(?:\$|₹|€|£)\s*(?:off|discount|save)',
        r'(?:flat|extra)\s+(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:off|discount)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match)
                if 1 <= amount <= 10000:  # Reasonable range
                    amounts.append(amount)
            except (ValueError, TypeError):
                continue
    
    return sorted(list(set(amounts)), reverse=True)

def extract_brands(text: str) -> List[str]:
    """ULTRA COMPREHENSIVE brand extraction - catches ANY brand name"""
    if not text:
        return []

    brands_found = []

    # ULTRA COMPREHENSIVE BRAND PATTERNS - catches millions of brands
    ultra_brand_patterns = [
        # Direct brand mentions with context
        r'(?:shop|buy|get|visit|check|go\s+to|available\s+at|exclusive\s+at)\s+(?:at|from|on|with)?\s*([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)(?:\s+(?:store|shop|website|app|online|now|today|here))',
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:coupon|discount|offer|deal|sale|promo|code|voucher|cashback|rebate)',
        r'(?:official|exclusive|new|latest|best|top|premium|luxury)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:coupon|discount|offer|deal)',
        r'(?:use|apply|enter|get|grab|claim)\s+(?:code|coupon)?\s*(?:at|on|from)?\s*([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)(?:\s+(?:checkout|payment|cart|now))',

        # Brand with percentage/amount
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:\d+%|\$\d+|₹\d+|€\d+|£\d+)\s*(?:off|discount|save)',
        r'(?:\d+%|\$\d+|₹\d+|€\d+|£\d+)\s*(?:off|discount|save)\s+(?:at|on|from)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25})',

        # Brand with action words
        r'(?:save|get|enjoy|receive|earn)\s+(?:up\s+to\s+)?(?:\d+%|\$\d+|₹\d+)\s+(?:at|on|from|with)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25})',
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:free\s+shipping|free\s+delivery|buy\s+one\s+get\s+one|bogo)',

        # Website/app patterns
        r'(?:visit|check|download|install)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:app|website|site)',
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\.(?:com|in|co\.uk|org|net|app)',

        # Social media and review patterns
        r'(?:follow|like|subscribe)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:on|for)',
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:review|rating|customer|user)',

        # Product category with brand
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:shoes|clothing|electronics|phone|laptop|watch|bag|perfume|makeup)',
        r'(?:new|latest|best|top)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:collection|launch|arrival|product)',

        # Generic brand indicators
        r'(?:brand|company|store|shop|retailer|manufacturer):\s*([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25})',
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:brand|store|shop|outlet|showroom)',

        # International patterns
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:India|USA|UK|Canada|Australia|Germany|France|Japan|China)',
        r'(?:imported|international|global|worldwide)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25})',

        # Seasonal and event patterns
        r'([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:sale|festival|diwali|christmas|black\s+friday|cyber\s+monday)',
        r'(?:summer|winter|spring|autumn|holiday)\s+([A-Z][a-zA-Z0-9&\'\-\.\s]{2,25}?)\s+(?:collection|sale)',
    ]

    # Extract using all patterns
    for pattern in ultra_brand_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match[0] else match[1]

            # Clean and validate brand name
            brand = match.strip()
            brand = re.sub(r'\s+', ' ', brand)  # Clean multiple spaces
            brand = brand.title()  # Proper case

            # Validation filters
            if (3 <= len(brand) <= 30 and  # Reasonable length
                not brand.isdigit() and  # Not just numbers
                not re.match(r'^[0-9%$₹€£\-\s]+$', brand) and  # Not just symbols/numbers
                re.search(r'[A-Za-z]', brand) and  # Contains letters
                not re.match(r'^(The|And|Or|For|With|At|On|In|To|From|By|Of)$', brand, re.IGNORECASE)):  # Not common words
                brands_found.append(brand)

    # Also check against known major brands for accuracy
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from config.application_settings import COMMON_BRANDS
        text_lower = text.lower()
        for brand in COMMON_BRANDS:
            if brand.lower() in text_lower:
                brands_found.append(brand)
    except ImportError:
        pass

    # Remove duplicates while preserving order
    seen = set()
    unique_brands = []
    for brand in brands_found:
        brand_lower = brand.lower()
        if brand_lower not in seen and len(brand_lower) > 2:
            seen.add(brand_lower)
            unique_brands.append(brand)

    return unique_brands[:10]  # Return top 10 brands found

def extract_categories(text: str) -> List[str]:
    """Professional category extraction with intelligence"""
    # Import here to avoid circular imports
    try:
        from config.application_settings import CATEGORY_KEYWORDS
    except ImportError:
        CATEGORY_KEYWORDS = {
            'fashion': ['clothing', 'shoes', 'accessories'],
            'electronics': ['phone', 'laptop', 'gadget'],
            'food': ['restaurant', 'delivery', 'meal'],
            'travel': ['flight', 'hotel', 'vacation'],
            'beauty': ['cosmetics', 'skincare', 'makeup']
        }
    
    if not text:
        return []
    
    category_scores = Counter()
    text_lower = text.lower()
    
    # Score categories based on keyword frequency
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                category_scores[category] += 1
    
    # Additional context-based scoring
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            patterns = [
                rf'{re.escape(keyword)}\s+(?:coupon|discount|deal|offer)',
                rf'(?:buy|shop|get)\s+{re.escape(keyword)}',
                rf'{re.escape(keyword)}\s+(?:sale|clearance)',
            ]
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    category_scores[category] += 2
    
    # Return top categories
    return [category for category, score in category_scores.most_common(3)]

def extract_expiry_dates(text: str) -> List[str]:
    """Professional expiry date extraction with intelligence"""
    if not text:
        return []
    
    dates = []
    
    # Professional date patterns
    patterns = [
        # Standard date formats
        r'(?:valid|expires?|until|till|ends?)\s+(?:on|by)?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:valid|expires?|until|till|ends?)\s+(?:on|by)?\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*\d{2,4})',
        
        # Context-based patterns
        r'(?:offer|deal|code|promotion)\s+(?:valid|expires?|ends?)\s+(?:on|by)?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:limited|hurry|last\s+chance).*?(?:until|till|ends?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        
        # Relative date patterns
        r'(?:valid|expires?)\s+(?:in\s+)?(\d+)\s+(?:days?|weeks?|months?)',
        r'(?:today|tomorrow|this\s+(?:week|month))\s+(?:only|last\s+day)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match and len(match.strip()) > 3:
                dates.append(match.strip())
    
    return dates[:3]  # Limit for quality

def extract_minimum_purchase(text: str) -> List[float]:
    """Professional minimum purchase extraction"""
    if not text:
        return []
    
    amounts = []
    
    # Professional minimum purchase patterns
    patterns = [
        r'(?:minimum|min)\s+(?:purchase|order|spend)\s+(?:of\s+)?(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)',
        r'(?:on\s+orders?\s+(?:of\s+|above\s+|over\s+))?(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:or\s+more|and\s+above)',
        r'(?:spend|purchase|order)\s+(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:or\s+more|and\s+above)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match)
                if 1 <= amount <= 50000:  # Reasonable range
                    amounts.append(amount)
            except (ValueError, TypeError):
                continue
    
    return sorted(list(set(amounts)))

def extract_terms_conditions(text: str) -> str:
    """Professional terms and conditions extraction"""
    if not text:
        return ""
    
    terms_found = []
    
    # Professional terms patterns
    patterns = [
        r'(?:terms?|conditions?|restrictions?|limitations?)\s*(?:apply|included)',
        r'(?:not\s+valid\s+with|cannot\s+be\s+combined)',
        r'(?:one\s+time\s+use|single\s+use|first\s+time\s+users?)',
        r'(?:new\s+(?:customers?|users?)\s+only)',
        r'(?:selected\s+(?:items?|products?)\s+only)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            terms_found.append(match.group())
    
    return "; ".join(terms_found[:3]) if terms_found else ""

def find_coupon_context(text: str, coupon_code: str, context_length: int = 50) -> str:
    """Professional context extraction around coupon codes"""
    if not text or not coupon_code:
        return ""
    
    code_pos = text.upper().find(coupon_code.upper())
    if code_pos == -1:
        return text[:context_length]
    
    start = max(0, code_pos - context_length // 2)
    end = min(len(text), code_pos + len(coupon_code) + context_length // 2)
    
    return text[start:end].strip()

def score_coupon_relevance(text: str) -> float:
    """Professional relevance scoring for coupon content"""
    if not text:
        return 0.0
    
    # Professional relevance indicators
    high_value_terms = [
        'coupon', 'discount', 'promo', 'offer', 'deal', 'save', 'sale',
        'code', 'voucher', 'cashback', 'rebate', 'free', 'off'
    ]
    
    medium_value_terms = [
        'price', 'cost', 'cheap', 'affordable', 'budget', 'bargain',
        'clearance', 'markdown', 'reduction', 'special'
    ]
    
    text_lower = text.lower()
    score = 0.0
    
    # Score based on term frequency and importance
    for term in high_value_terms:
        score += text_lower.count(term) * 2.0
    
    for term in medium_value_terms:
        score += text_lower.count(term) * 1.0
    
    # Bonus for percentage or amount mentions
    if re.search(r'\d+\s*%', text):
        score += 3.0
    
    if re.search(r'[\$₹€£]\s*\d+', text):
        score += 2.0
    
    # Normalize score
    return min(score / len(text.split()) * 100, 100.0)

def split_description_into_sections(text: str) -> List[str]:
    """Professional text segmentation for analysis"""
    if not text:
        return []
    
    # Split by common delimiters
    sections = []
    
    # Split by double newlines first
    major_sections = re.split(r'\n\s*\n', text)
    
    for section in major_sections:
        # Further split by single newlines or long sentences
        subsections = re.split(r'\n|(?<=[.!?])\s+(?=[A-Z])', section)
        
        for subsection in subsections:
            subsection = subsection.strip()
            if len(subsection) > 20:  # Minimum meaningful length
                sections.append(subsection)
    
    return sections[:20]  # Limit for processing efficiency
