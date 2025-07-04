#!/usr/bin/env python3
"""
IMPROVED TEXT PROCESSING UTILITIES
Context-aware coupon code and brand extraction without predefined samples
"""

import re
import logging
from typing import List, Dict, Optional, Tuple, Set
from collections import Counter
from enhanced_brand_database import get_all_brands, is_known_brand, get_brand_category

logger = logging.getLogger(__name__)

def extract_coupon_codes_contextual(text: str) -> List[Dict[str, any]]:
    """
    Extract coupon codes with their surrounding context for better brand association
    Returns list of dictionaries with code, context, and position information
    """
    if not text:
        return []
    
    # Clean text first
    text = clean_text_advanced(text)
    
    # Find potential coupon codes with context
    coupon_findings = []
    
    # Pattern 1: Explicit coupon mentions with codes - more specific
    explicit_patterns = [
        r'(?:use|apply|enter)\s+(?:code|coupon|promo)\s*:?\s*([A-Z0-9]{4,15})\b',
        r'(?:coupon|promo)\s+code\s*:?\s*([A-Z0-9]{4,15})\b',
        r'(?:discount|offer)\s+code\s*:?\s*([A-Z0-9]{4,15})\b',
        r'(?:checkout|payment)\s+(?:with\s+)?code\s*:?\s*([A-Z0-9]{4,15})\b'
    ]
    
    for pattern in explicit_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            code = match.group(1).upper()
            if is_valid_coupon_code_improved(code) and _is_code_in_valid_context(code, text):
                start_pos = max(0, match.start() - 100)
                end_pos = min(len(text), match.end() + 100)
                context = text[start_pos:end_pos]

                coupon_findings.append({
                    'code': code,
                    'context': context,
                    'position': match.start(),
                    'confidence': 0.9,  # High confidence for explicit mentions
                    'extraction_method': 'explicit'
                })
    
    # Pattern 2: Alphanumeric codes in promotional context - much more restrictive
    promotional_context_patterns = [
        # Only match codes that are clearly in coupon context with specific format
        r'(?:coupon|promo|discount)\s+.*?\b([A-Z]{2,4}\d{4,8})\b',
        r'(?:code|offer)\s+.*?\b(\d{2,4}[A-Z]{2,6})\b',
        # Codes mentioned with explicit save/discount context
        r'(?:save|get)\s+\d+%?\s+.*?\b([A-Z0-9]{5,12})\b(?=.*(?:code|coupon))'
    ]
    
    for pattern in promotional_context_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            code = match.group(1).upper()
            if (is_valid_coupon_code_improved(code) and
                _is_code_in_valid_context(code, text) and
                not any(cf['code'] == code for cf in coupon_findings)):
                start_pos = max(0, match.start() - 100)
                end_pos = min(len(text), match.end() + 100)
                context = text[start_pos:end_pos]

                coupon_findings.append({
                    'code': code,
                    'context': context,
                    'position': match.start(),
                    'confidence': 0.7,  # Medium confidence
                    'extraction_method': 'contextual'
                })
    
    # Sort by confidence and remove duplicates
    seen_codes = set()
    unique_findings = []
    
    for finding in sorted(coupon_findings, key=lambda x: x['confidence'], reverse=True):
        if finding['code'] not in seen_codes:
            seen_codes.add(finding['code'])
            unique_findings.append(finding)
    
    return unique_findings[:10]  # Limit to top 10 most confident findings

def is_valid_coupon_code_improved(code: str) -> bool:
    """PROFESSIONAL HIGH-VOLUME coupon code validation - Less restrictive for maximum capture"""
    if not code or len(code) < 3 or len(code) > 25:  # Relaxed length requirements
        return False

    # Allow alphanumeric with some special characters
    if not re.match(r'^[A-Z0-9\-_]+$', code):
        return False

    # RELAXED: Allow codes with only letters OR only numbers (many valid codes are like this)
    # Examples: "WELCOME", "SAVE", "2024", "50OFF" are all valid

    # Avoid codes that are too repetitive (like "AAAA" or "1111")
    if len(set(code)) < 2:  # Reduced from 3 to 2
        return False

    # STRICT: Exclude common non-code words that are frequently misidentified
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
        # Gaming/app words that get misidentified
        'COOKIE', 'KINGDOM', 'GAME', 'PLAY', 'LEVEL', 'COINS', 'GEMS', 'POINTS',
        # Platform words
        'TELEGRAM', 'WHATSAPP', 'INSTAGRAM', 'FACEBOOK', 'YOUTUBE', 'TWITTER',
        # Action words
        'CLICK', 'VISIT', 'CHECK', 'WATCH', 'DOWNLOAD', 'INSTALL', 'REGISTER',
        # Time/date words
        'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST',
        'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'MONDAY', 'TUESDAY', 'WEDNESDAY',
        'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'TODAY', 'TOMORROW', 'YESTERDAY'
    }

    if code.upper() in common_non_codes:
        return False

    # Avoid obvious non-codes with patterns
    non_code_patterns = [
        r'^(SAVE|DEAL|OFFER|CODE|FREE|GET)\d*$',
        r'^\d{4}$',  # Just year (2024, 2025, etc.)
        r'^[A-Z]{1,3}$',  # Too short and only letters
        r'^[A-Z]{10,}$',  # Too long and only letters
        r'^(GET|WIN|SAVE)\d+$',  # GET50, WIN100, SAVE25, etc.
        r'^\d+(OFF|PERCENT)$',  # 50OFF, 25PERCENT, etc.
        r'^\d{1,2}(ST|ND|RD|TH)$',  # Date ordinals like 31ST, 22ND
        r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\d*$',  # Month abbreviations
    ]

    for pattern in non_code_patterns:
        if re.match(pattern, code):
            return False

    # Additional validation: Real coupon codes usually have specific patterns
    # They often mix letters and numbers in meaningful ways
    # Reject codes that are just common words with numbers appended
    common_word_prefixes = ['GET', 'SAVE', 'WIN', 'USE', 'TRY', 'BUY', 'NEW', 'TOP', 'BEST']
    for prefix in common_word_prefixes:
        if code.startswith(prefix) and code[len(prefix):].isdigit():
            return False

    return True

def extract_brand_from_context(context: str, coupon_code: str) -> Optional[str]:
    """
    Extract brand name from the context around a coupon code with improved accuracy
    Only returns brands that are clearly associated with the coupon code
    """
    if not context or not coupon_code:
        return None

    # Use our comprehensive enhanced brand database
    known_brands = {brand.upper() for brand in get_all_brands()}

    # Clean context for better matching
    context_clean = re.sub(r'[^\w\s]', ' ', context)
    context_upper = context_clean.upper()

    # Look for known brands with strict word boundary matching
    for brand in known_brands:
        # Use word boundaries and check proximity to coupon code
        brand_pattern = rf'\b{re.escape(brand)}\b'
        if re.search(brand_pattern, context_upper):
            # Verify the brand is mentioned in reasonable proximity to the coupon code
            brand_matches = list(re.finditer(brand_pattern, context_upper))
            code_matches = list(re.finditer(rf'\b{re.escape(coupon_code.upper())}\b', context_upper))

            if brand_matches and code_matches:
                # Check if brand and code are within reasonable distance (500 characters)
                for brand_match in brand_matches:
                    for code_match in code_matches:
                        distance = abs(brand_match.start() - code_match.start())
                        if distance <= 500:  # Within 500 characters
                            return brand.title()

    # Only try pattern-based extraction if no known brand found and code is valid
    if not is_valid_coupon_code_improved(coupon_code):
        return None

    # Try more flexible pattern-based extraction for simple cases
    brand_patterns = [
        # Brand explicitly mentioned with coupon context
        rf'\b([A-Z][a-zA-Z]{{3,15}})\s+(?:coupon|code|discount|offer|promo)\b.*?{re.escape(coupon_code)}',
        rf'{re.escape(coupon_code)}.*?\b(?:for|at|on)\s+([A-Z][a-zA-Z]{{3,15}})\b',
        # Website patterns
        rf'\b([A-Z][a-zA-Z]{{3,15}})\.(?:com|in|co\.uk|org)\b.*?{re.escape(coupon_code)}',
        rf'{re.escape(coupon_code)}.*?\b([A-Z][a-zA-Z]{{3,15}})\.(?:com|in|co\.uk|org)\b',
        # Simple proximity patterns (for cases like "Amazon with code SAVE50")
        rf'\b([A-Z][a-zA-Z]{{3,15}})\s+.*?\b{re.escape(coupon_code)}\b',
        rf'\b{re.escape(coupon_code)}\b.*?\b([A-Z][a-zA-Z]{{3,15}})\b'
    ]

    for pattern in brand_patterns:
        matches = re.findall(pattern, context, re.IGNORECASE)
        for match in matches:
            potential_brand = match.strip().title()
            if is_valid_brand_name_improved(potential_brand):
                return potential_brand

    # If no brand found, return None instead of guessing
    return None

def is_valid_brand_name_improved(brand: str) -> bool:
    """Validate if extracted text is likely a real brand name with strict filtering"""
    if not brand or len(brand) < 3 or len(brand) > 20:
        return False

    # Must start with capital letter and contain mostly letters
    if not brand[0].isupper() or not re.match(r'^[A-Za-z][A-Za-z\'\&\-\.]*$', brand):
        return False

    # Comprehensive list of common words that are NOT brands
    common_words = {
        # Basic words
        'The', 'And', 'With', 'For', 'Code', 'Deal', 'Offer', 'Sale', 'Discount',
        'Coupon', 'Free', 'Get', 'Save', 'Buy', 'Shop', 'Store', 'Online',
        'Website', 'Link', 'Click', 'Here', 'This', 'That', 'Your', 'New',
        'Best', 'Top', 'Great', 'Amazing', 'Special', 'Limited', 'Exclusive',
        'Today', 'Now', 'Available', 'Working', 'Latest', 'Current',
        # Social media and video terms
        'Video', 'Channel', 'Subscribe', 'Like', 'Share', 'Comment', 'Bell',
        'Description', 'Title', 'Content', 'Guide', 'Tutorial', 'Tips',
        'Watch', 'Follow', 'Notification', 'Update', 'Upload',
        # Action words
        'But', 'Gift', 'Grab', 'Mega', 'Super', 'Ultra', 'Max', 'Plus',
        'Pro', 'Premium', 'Elite', 'Master', 'Expert', 'Advanced',
        # Generic business terms
        'App', 'Site', 'Page', 'Store', 'Shop', 'Brand', 'Company', 'Service',
        'Platform', 'System', 'Network', 'Portal', 'Hub', 'Center',
        # Time and status words
        'Active', 'Valid', 'Expired', 'Working', 'Tested', 'Verified',
        'Confirmed', 'Updated', 'Fresh', 'Recent', 'Live', 'Current',
        # Promotional terms
        'Bonus', 'Extra', 'Maximum', 'Minimum', 'Flat', 'Upto', 'Off',
        'Percent', 'Cash', 'Back', 'Reward', 'Prize', 'Win', 'Lucky',
        # Common misidentified words from the results
        'Couponnxt', 'Discount'  # These appear to be generic coupon site names
    }

    if brand in common_words:
        return False

    # Additional validation: brand should not be all uppercase common words
    if brand.upper() in {word.upper() for word in common_words}:
        return False

    # Must not be too generic or suspicious
    suspicious_patterns = [
        r'^(App|Site|Page|Store|Shop|Brand|Company)$',
        r'^(Get|Save|Win|Buy|Try|Use)\w*$',
        r'^(New|Best|Top|Great|Amazing|Special)\w*$',
        r'^(Working|Active|Valid|Live|Current)\w*$'
    ]

    for pattern in suspicious_patterns:
        if re.match(pattern, brand, re.IGNORECASE):
            return False

    return True

def _has_real_coupon_content(text: str) -> bool:
    """
    Intelligent analysis to determine if text actually contains real coupon content
    Returns False for generic social media content, gaming content, etc.
    """
    if not text:
        return False

    text_lower = text.lower()

    # RED FLAGS: Content that definitely does NOT contain real coupons
    red_flags = [
        # Social media spam indicators
        'subscribe', 'comment', 'like', 'share', 'bell', 'notification',
        'hit the bell', 'don\'t forget to subscribe', 'like and comment',

        # Gaming content indicators
        'cookie run kingdom', 'game codes', 'gaming', 'mobile game',
        'free gems', 'free coins', 'game currency',

        # Generic coupon site spam
        'secret codes', 'hidden codes', 'unlimited codes',
        'working codes', 'latest codes', 'new codes',

        # Vague promotional content without specifics
        'save big', 'huge discounts', 'amazing deals',
        'best offers', 'exclusive deals'
    ]

    # Count red flags
    red_flag_count = sum(1 for flag in red_flags if flag in text_lower)

    # If too many red flags, likely not real coupon content
    if red_flag_count >= 3:
        return False

    # GREEN FLAGS: Indicators of real coupon content
    green_flags = [
        # Specific discount mentions
        r'\d+%\s*off', r'\d+%\s*discount', r'flat\s+\d+%',
        r'save\s+\d+%', r'get\s+\d+%\s*off',

        # Specific brand mentions with context
        r'amazon\s+(?:coupon|discount|offer|code)',
        r'flipkart\s+(?:coupon|discount|offer|code)',
        r'dominos?\s+(?:coupon|discount|offer|code)',
        r'zomato\s+(?:coupon|discount|offer|code)',

        # Specific coupon code patterns
        r'use\s+code\s+[A-Z0-9]{4,}',
        r'apply\s+code\s+[A-Z0-9]{4,}',
        r'enter\s+code\s+[A-Z0-9]{4,}',
        r'promo\s+code\s*:\s*[A-Z0-9]{4,}',

        # Specific monetary amounts
        r'₹\d+\s*off', r'\$\d+\s*off', r'rs\.?\s*\d+\s*off',

        # Expiry date mentions
        r'valid\s+till', r'expires?\s+on', r'limited\s+time',

        # Checkout/purchase context
        r'at\s+checkout', r'during\s+payment', r'on\s+purchase'
    ]

    # Count green flags using regex
    green_flag_count = 0
    for flag_pattern in green_flags:
        if re.search(flag_pattern, text_lower):
            green_flag_count += 1

    # BRAND ANALYSIS: Check if real brands are mentioned
    real_brands_mentioned = _count_real_brands_in_text(text)

    # DECISION LOGIC
    # Need at least 2 green flags OR 1 green flag + real brand mention
    has_sufficient_indicators = (
        green_flag_count >= 2 or
        (green_flag_count >= 1 and real_brands_mentioned >= 1)
    )

    # Additional check: Must not be overwhelmed by red flags
    red_flag_ratio = red_flag_count / max(len(text.split()), 1) * 100
    if red_flag_ratio > 5:  # More than 5% red flag words
        return False

    return has_sufficient_indicators

def _count_real_brands_in_text(text: str) -> int:
    """Count how many real brands are mentioned in the text"""
    real_brands = {
        'amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'meesho',
        'zomato', 'swiggy', 'doordash', 'ubereats',
        'dominos', 'domino\'s', 'kfc', 'mcdonald', 'pizza hut', 'starbucks',
        'uber', 'ola', 'lyft',
        'paytm', 'phonepe', 'googlepay', 'paypal',
        'netflix', 'hotstar', 'spotify', 'prime video', 'disney',
        'samsung', 'apple', 'oneplus', 'xiaomi', 'realme',
        'nike', 'adidas', 'puma', 'zara', 'h&m',
        'booking', 'makemytrip', 'goibibo', 'airbnb', 'oyo',
        'temu', 'ebay', 'walmart', 'target'
    }

    text_lower = text.lower()
    count = 0

    for brand in real_brands:
        if re.search(rf'\b{re.escape(brand)}\b', text_lower):
            count += 1

    return count

def _is_code_in_valid_context(code: str, full_text: str) -> bool:
    """
    Check if a potential coupon code appears in a valid coupon context
    Prevents extraction of random words that happen to match patterns
    """
    if not code or not full_text:
        return False

    text_lower = full_text.lower()
    code_lower = code.lower()

    # Find all occurrences of the code in the text
    code_positions = []
    start = 0
    while True:
        pos = text_lower.find(code_lower, start)
        if pos == -1:
            break
        code_positions.append(pos)
        start = pos + 1

    if not code_positions:
        return False

    # Check context around each occurrence
    for pos in code_positions:
        # Get context around the code (200 characters before and after)
        context_start = max(0, pos - 200)
        context_end = min(len(full_text), pos + len(code) + 200)
        context = full_text[context_start:context_end].lower()

        # Valid context indicators
        valid_indicators = [
            'coupon', 'promo', 'discount', 'offer', 'code',
            'save', 'off', 'deal', 'checkout', 'apply',
            'use', 'enter', 'get', '%', 'percent',
            'flat', 'extra', 'bonus'
        ]

        # Invalid context indicators (social media, gaming, etc.)
        invalid_indicators = [
            'subscribe', 'comment', 'like', 'share', 'bell',
            'notification', 'channel', 'video', 'watch',
            'cookie run', 'kingdom', 'game', 'play',
            'telegram', 'whatsapp', 'instagram'
        ]

        # Count valid and invalid indicators in context
        valid_count = sum(1 for indicator in valid_indicators if indicator in context)
        invalid_count = sum(1 for indicator in invalid_indicators if indicator in context)

        # If this occurrence has valid context, the code is valid
        if valid_count >= 2 and invalid_count <= 1:
            return True

        # Special case: if code appears with specific brand names
        brand_indicators = [
            'amazon', 'flipkart', 'myntra', 'zomato', 'swiggy',
            'dominos', 'kfc', 'uber', 'ola', 'paytm'
        ]

        brand_count = sum(1 for brand in brand_indicators if brand in context)
        if brand_count >= 1 and valid_count >= 1:
            return True

    return False

def extract_coupon_information_improved(text: str) -> List[Dict[str, any]]:
    """
    Main improved extraction function that returns properly linked coupon-brand pairs
    Only extracts when real coupon codes and brands are detected
    """
    if not text:
        return []

    # FIRST: Analyze if the text actually contains real coupon content
    if not _has_real_coupon_content(text):
        return []

    # Extract coupon codes with context
    coupon_findings = extract_coupon_codes_contextual(text)

    if not coupon_findings:
        return []
    
    # Extract other information
    percentages = extract_percentage_discounts_improved(text)
    categories = extract_categories_improved(text)
    expiry_dates = extract_expiry_dates_improved(text)
    
    # Process each coupon finding
    processed_coupons = []
    
    for i, finding in enumerate(coupon_findings):
        code = finding['code']
        context = finding['context']
        
        # Extract brand from the specific context of this code
        brand = extract_brand_from_context(context, code)
        
        # Get associated information
        percentage = percentages[i] if i < len(percentages) else None
        category = categories[i] if i < len(categories) else 'general'
        expiry = expiry_dates[i] if i < len(expiry_dates) else 'N/A'
        
        # Create title based on actual extracted information
        title_parts = []
        if percentage:
            title_parts.append(f"{percentage}% OFF")
        if brand:
            title_parts.append(brand)
        if category and category != 'general':
            title_parts.append(category.replace('_', ' ').title())
        
        title = " ".join(title_parts) if title_parts else f"Discount Code {code}"
        
        coupon_info = {
            'coupon_code': code,
            'brand': brand or 'Unknown',
            'title': title,
            'percentage': percentage,
            'category': category,
            'expiry_date': expiry,
            'description': context.strip(),
            'confidence': finding['confidence'],
            'extraction_method': finding['extraction_method']
        }
        
        processed_coupons.append(coupon_info)
    
    return processed_coupons

def clean_text_advanced(text: str) -> str:
    """Advanced text cleaning for better extraction"""
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', ' ', text)
    
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    
    # Normalize emojis and special characters
    text = re.sub(r'[^\w\s\-\.\,\:\;\!\?\%\$\@\&\(\)\[\]]', ' ', text)
    
    return text.strip()

def extract_percentage_discounts_improved(text: str) -> List[float]:
    """Extract percentage discounts with improved patterns"""
    if not text:
        return []
    
    percentages = []
    patterns = [
        r'(\d{1,2})%\s*(?:off|discount|save)',
        r'(?:save|get|enjoy)\s+(\d{1,2})%',
        r'(?:up\s+to\s+)?(\d{1,2})%\s*(?:discount|off)',
        r'(\d{1,2})\s*percent\s*off'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                percent = float(match)
                if 5 <= percent <= 90:  # Reasonable range
                    percentages.append(percent)
            except (ValueError, TypeError):
                continue
    
    return sorted(list(set(percentages)), reverse=True)

def extract_categories_improved(text: str) -> List[str]:
    """Extract categories with improved accuracy"""
    if not text:
        return []
    
    category_keywords = {
        'electronics': ['electronics', 'phone', 'mobile', 'laptop', 'computer', 'gadget', 'tech'],
        'fashion': ['fashion', 'clothing', 'clothes', 'dress', 'shirt', 'pant', 'wear'],
        'food': ['food', 'restaurant', 'pizza', 'burger', 'meal', 'delivery', 'dining'],
        'health': ['health', 'vitamin', 'supplement', 'medical', 'healthcare', 'fitness'],
        'beauty': ['beauty', 'cosmetics', 'skincare', 'makeup', 'perfume', 'grooming'],
        'home': ['home', 'furniture', 'decor', 'kitchen', 'appliance', 'household']
    }
    
    text_lower = text.lower()
    category_scores = Counter()
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                category_scores[category] += 1
    
    return [category for category, score in category_scores.most_common(2)]

def extract_expiry_dates_improved(text: str) -> List[str]:
    """Extract expiry dates with improved patterns"""
    if not text:
        return []
    
    dates = []
    patterns = [
        r'(?:expires?|valid|until|ends?)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:expires?|valid|until|ends?)\s*:?\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{1,2},?\s*\d{2,4})',
        r'(?:limited|hurry).*?(?:until|till)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match and len(match.strip()) > 5:
                dates.append(match.strip())
    
    return dates[:2]  # Return up to 2 dates