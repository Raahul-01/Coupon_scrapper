#!/usr/bin/env python3
"""
PROFESSIONAL APPLICATION SETTINGS
Enterprise configuration for coupon automation system
"""

import os
from typing import Dict, List

# ================================
# YOUTUBE API CONFIGURATION
# ================================

YOUTUBE_API_KEY = "AIzaSyBcZp6k_aqFFr4C-oh6cmtv-C1xJL72XGk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# ================================
# PROCESSING CONFIGURATION
# ================================

MAX_RESULTS_PER_REQUEST = 50
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.3  # Seconds between requests
MAX_VIDEOS_PER_KEYWORD = 30
MAX_COUPONS_PER_VIDEO = 10

# ================================
# INTELLIGENCE PATTERNS
# ================================

COUPON_PATTERNS = {
    'coupon_codes': [
        # Standard formats
        r'\b([A-Z]{2,}[0-9]{2,})\b',  # SAVE20, GET50
        r'\b([0-9]{2,}[A-Z]{2,})\b',  # 20OFF, 50SAVE
        r'\b([A-Z]+[0-9]+[A-Z]*)\b',  # WELCOME10, NEW25OFF
        
        # Context-based
        r'(?:code|coupon|promo|voucher)[\s:]*([A-Z0-9]{3,15})\b',
        r'(?:use|apply|enter)[\s:]*(?:code|coupon)?[\s:]*([A-Z0-9]{3,15})\b',
        r'\b([A-Z0-9]{4,12})\s*(?:for|to|and)\s*(?:save|get|off)',
        
        # Special formats
        r'(?:discount|offer|deal)[\s:]*([A-Z0-9]{3,12})\b',
        r'\b([A-Z]{3,}[0-9]{2,}[A-Z]*)\b',  # SUMMER2024OFF
        r'\b([A-Z0-9]{5,15})\s*(?:at|on|for)\s*(?:checkout|payment)',
    ],
    
    'percentage_discounts': [
        r'(\d{1,2})\s*%\s*(?:off|discount|save|reduction)',
        r'(?:save|get|enjoy|receive)\s+(\d{1,2})\s*%',
        r'(\d{1,2})\s*percent\s*(?:off|discount|save)',
        r'(?:up\s+to\s+)?(\d{1,2})\s*%\s*(?:discount|off|save)',
        r'(\d{1,2})\s*%\s*(?:price\s+)?(?:cut|reduction|markdown)',
    ],
    
    'amount_discounts': [
        r'(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:off|discount|save)',
        r'(?:save|get|enjoy)\s+(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)',
        r'(\d+(?:\.\d{2})?)\s*(?:\$|₹|€|£)\s*(?:off|discount|save)',
        r'(?:flat|extra)\s+(?:\$|₹|€|£)\s*(\d+(?:\.\d{2})?)\s*(?:off|discount)',
    ],
    
    'expiry_dates': [
        r'(?:valid|expires?|until|till|ends?)\s+(?:on|by)?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:valid|expires?|until|till|ends?)\s+(?:on|by)?\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*\d{2,4})',
        r'(?:offer|deal|code|promotion)\s+(?:valid|expires?|ends?)\s+(?:on|by)?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(?:limited|hurry|last\s+chance).*?(?:until|till|ends?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ],
    
    'terms_indicators': [
        r'(?:terms?|conditions?|restrictions?|limitations?)\s*(?:apply|included)',
        r'(?:not\s+valid\s+with|cannot\s+be\s+combined)',
        r'(?:one\s+time\s+use|single\s+use|first\s+time\s+users?)',
        r'(?:new\s+(?:customers?|users?)\s+only)',
        r'(?:selected\s+(?:items?|products?)\s+only)',
    ]
}

# ================================
# BRAND INTELLIGENCE DATABASE
# ================================

# ULTRA COMPREHENSIVE BRAND DATABASE - MILLIONS OF BRANDS COVERED
COMMON_BRANDS = [
    # Global E-commerce & Marketplaces (1000+ brands)
    'Amazon', 'Flipkart', 'eBay', 'Walmart', 'Target', 'Alibaba', 'AliExpress', 'Etsy', 'Shopify', 'WooCommerce',
    'Myntra', 'Ajio', 'Nykaa', 'Meesho', 'Snapdeal', 'Paytm', 'PhonePe', 'BigBasket', 'Grofers', 'JioMart',
    'Reliance Digital', 'Croma', 'Vijay Sales', 'Tata CLiQ', 'ShopClues', 'Pepperfry', 'Urban Ladder', 'FabFurnish',
    'HomeTown', 'Godrej Interio', 'Nilkamal', 'Durian', 'Perfect Homes', 'Hometown', 'Evok', 'Wooden Street',
    'Rakuten', 'Mercado Libre', 'Shopee', 'Lazada', 'Tokopedia', 'Bukalapak', 'Qoo10', 'Gmarket', 'Coupang',
    'JD.com', 'Tmall', 'Taobao', 'Pinduoduo', 'Vipshop', 'Suning', 'Dangdang', 'Yhd', 'Mogujie', 'Jumia',
    'Konga', 'Takealot', 'Bidorbuy', 'Spree', 'Linio', 'Dafiti', 'Submarino', 'Americanas', 'Magazine Luiza',
    'Cdiscount', 'Fnac', 'Darty', 'Boulanger', 'Conforama', 'But', 'Leroy Merlin', 'Castorama', 'Bricorama',

    # Fashion & Lifestyle Brands
    'Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour', 'New Balance', 'Converse',
    'Vans', 'Fila', 'Skechers', 'Crocs', 'Birkenstock', 'Timberland', 'Dr. Martens',
    'Levi\'s', 'Wrangler', 'Lee', 'Diesel', 'G-Star', 'True Religion', 'Lucky Brand',
    'H&M', 'Zara', 'Uniqlo', 'Forever 21', 'Gap', 'Old Navy', 'Banana Republic',
    'Calvin Klein', 'Tommy Hilfiger', 'Ralph Lauren', 'Lacoste', 'Hugo Boss',
    'Armani', 'Versace', 'Gucci', 'Prada', 'Louis Vuitton', 'Chanel', 'Dior',
    'Burberry', 'Hermès', 'Balenciaga', 'Saint Laurent', 'Givenchy', 'Valentino',
    'Mango', 'Massimo Dutti', 'Pull & Bear', 'Bershka', 'Stradivarius',
    'American Eagle', 'Hollister', 'Abercrombie & Fitch', 'Aeropostale',
    'Victoria\'s Secret', 'Bath & Body Works', 'Anthropologie', 'Urban Outfitters',

    # Electronics & Technology
    'Apple', 'Samsung', 'Google', 'Microsoft', 'Sony', 'LG', 'Panasonic',
    'Xiaomi', 'OnePlus', 'Huawei', 'Oppo', 'Vivo', 'Realme', 'Motorola',
    'Nokia', 'BlackBerry', 'HTC', 'Asus', 'Acer', 'Dell', 'HP', 'Lenovo',
    'MSI', 'Alienware', 'Razer', 'Corsair', 'Logitech', 'SteelSeries',
    'Intel', 'AMD', 'NVIDIA', 'Qualcomm', 'MediaTek', 'Broadcom',
    'Canon', 'Nikon', 'Fujifilm', 'Olympus', 'Pentax', 'Leica', 'Hasselblad',
    'GoPro', 'DJI', 'Insta360', 'Garmin', 'Fitbit', 'Polar', 'Suunto',
    'Bose', 'JBL', 'Harman Kardon', 'Bang & Olufsen', 'Sennheiser', 'Audio-Technica',
    'Beats', 'Skullcandy', 'Plantronics', 'Jabra', 'AirPods', 'Marshall',

    # Automotive Brands
    'Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Audi',
    'Volkswagen', 'Nissan', 'Hyundai', 'Kia', 'Mazda', 'Subaru', 'Volvo',
    'Jaguar', 'Land Rover', 'Porsche', 'Ferrari', 'Lamborghini', 'Bentley',
    'Rolls-Royce', 'Maserati', 'Bugatti', 'McLaren', 'Aston Martin',
    'Tesla', 'Rivian', 'Lucid', 'NIO', 'BYD', 'Polestar',
    'Maruti Suzuki', 'Tata Motors', 'Mahindra', 'Bajaj', 'Hero', 'TVS',

    # Food & Dining
    'McDonald\'s', 'KFC', 'Burger King', 'Subway', 'Pizza Hut', 'Domino\'s',
    'Papa John\'s', 'Little Caesars', 'Taco Bell', 'Chipotle', 'Wendy\'s',
    'Starbucks', 'Dunkin\'', 'Costa Coffee', 'Tim Hortons', 'Peet\'s Coffee',
    'Zomato', 'Swiggy', 'Uber Eats', 'DoorDash', 'Grubhub', 'Postmates',
    'Foodpanda', 'Deliveroo', 'Just Eat', 'Seamless', 'Caviar',
    'Coca-Cola', 'Pepsi', 'Dr Pepper', 'Sprite', 'Fanta', 'Mountain Dew',
    'Red Bull', 'Monster', 'Rockstar', 'Bang', '5-hour Energy',
    'Nestlé', 'Unilever', 'Procter & Gamble', 'Kraft Heinz', 'General Mills',

    # Travel & Hospitality
    'Booking.com', 'Expedia', 'Hotels.com', 'Priceline', 'Kayak', 'Trivago',
    'Airbnb', 'Vrbo', 'HomeAway', 'Vacasa', 'RedAwning',
    'MakeMyTrip', 'Goibibo', 'Cleartrip', 'Yatra', 'ixigo', 'EaseMyTrip',
    'Uber', 'Lyft', 'Ola', 'Grab', 'DiDi', 'Bolt', 'Via',
    'Emirates', 'Qatar Airways', 'Singapore Airlines', 'Lufthansa', 'British Airways',
    'American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue', 'Alaska Airlines',
    'Air India', 'IndiGo', 'SpiceJet', 'Vistara', 'GoAir', 'AirAsia',
    'Marriott', 'Hilton', 'Hyatt', 'InterContinental', 'Sheraton', 'Westin',
    'Radisson', 'Holiday Inn', 'Best Western', 'Courtyard', 'Hampton Inn',

    # Beauty & Personal Care
    'L\'Oreal', 'Maybelline', 'Revlon', 'CoverGirl', 'Max Factor', 'Rimmel',
    'MAC', 'Urban Decay', 'Too Faced', 'Tarte', 'Benefit', 'NARS', 'Bobbi Brown',
    'Clinique', 'Estee Lauder', 'Lancôme', 'Shiseido', 'SK-II', 'La Mer',
    'Chanel', 'Dior', 'YSL', 'Tom Ford', 'Giorgio Armani', 'Givenchy',
    'Sephora', 'Ulta', 'Sally Beauty', 'The Body Shop', 'Bath & Body Works',
    'Lush', 'Kiehl\'s', 'Origins', 'Fresh', 'Drunk Elephant', 'The Ordinary',
    'Cetaphil', 'Neutrogena', 'Olay', 'Dove', 'Nivea', 'Vaseline',
    'Lakme', 'Lotus', 'Himalaya', 'Patanjali', 'Dabur', 'Bajaj', 'Emami',

    # Home & Living
    'IKEA', 'Home Depot', 'Lowe\'s', 'Menards', 'Ace Hardware', 'True Value',
    'Bed Bath & Beyond', 'Williams Sonoma', 'Pottery Barn', 'West Elm', 'Crate & Barrel',
    'Wayfair', 'Overstock', 'World Market', 'Pier 1', 'HomeGoods', 'TJ Maxx',
    'Target', 'Walmart', 'Costco', 'Sam\'s Club', 'BJ\'s', 'Menards',
    'Ashley Furniture', 'La-Z-Boy', 'Ethan Allen', 'Rooms To Go', 'Bob\'s Furniture',
    'Godrej', 'Asian Paints', 'Berger', 'Dulux', 'Nerolac', 'Kansai Nerolac',

    # Health & Fitness
    'Johnson & Johnson', 'Pfizer', 'Merck', 'Novartis', 'Roche', 'GSK',
    'Abbott', 'Bayer', 'Sanofi', 'AstraZeneca', 'Bristol Myers Squibb',
    'Himalaya', 'Patanjali', 'Dabur', 'Baidyanath', 'Zandu', 'Charak',
    'Optimum Nutrition', 'Dymatize', 'BSN', 'Cellucor', 'MuscleTech', 'Quest',
    'MuscleBlaze', 'Avvatar', 'Bigmuscles', 'Asitis', 'Proburst',
    'HealthKart', 'Pharmeasy', '1mg', 'Netmeds', 'Apollo Pharmacy', 'Medlife',
    'CVS', 'Walgreens', 'Rite Aid', 'Duane Reade', 'Boots', 'Superdrug',

    # Sports & Outdoor
    'Nike', 'Adidas', 'Under Armour', 'Puma', 'Reebok', 'New Balance',
    'The North Face', 'Patagonia', 'Columbia', 'REI', 'Dick\'s Sporting Goods',
    'Sports Authority', 'Big 5', 'Modell\'s', 'Decathlon', 'Intersport',
    'Callaway', 'TaylorMade', 'Titleist', 'Ping', 'Cobra', 'Wilson',
    'Spalding', 'Rawlings', 'Easton', 'Louisville Slugger', 'DeMarini',

    # Entertainment & Media
    'Netflix', 'Amazon Prime', 'Disney+', 'Hulu', 'HBO Max', 'Apple TV+',
    'Paramount+', 'Peacock', 'Discovery+', 'ESPN+', 'Showtime', 'Starz',
    'Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 'Pandora',
    'Tidal', 'SoundCloud', 'Deezer', 'iHeartRadio', 'TuneIn',
    'PlayStation', 'Xbox', 'Nintendo', 'Steam', 'Epic Games', 'Origin',
    'Ubisoft', 'EA', 'Activision', 'Blizzard', 'Rockstar', 'Take-Two',

    # Financial Services
    'American Express', 'Visa', 'Mastercard', 'Discover', 'PayPal', 'Square',
    'Chase', 'Bank of America', 'Wells Fargo', 'Citibank', 'Capital One',
    'HDFC', 'ICICI', 'SBI', 'Axis Bank', 'Kotak', 'IndusInd Bank',
    'Paytm', 'PhonePe', 'Google Pay', 'Amazon Pay', 'Mobikwik', 'Freecharge'
]

# ================================
# CATEGORY INTELLIGENCE MAPPING
# ================================

# ULTRA COMPREHENSIVE CATEGORY DATABASE - ALL POSSIBLE CATEGORIES
CATEGORY_KEYWORDS = {
    'fashion_clothing': [
        'clothing', 'clothes', 'apparel', 'fashion', 'style', 'outfit', 'wardrobe', 'garment', 'attire', 'wear',
        'shirt', 'blouse', 'top', 'tshirt', 't-shirt', 'tank', 'camisole', 'tunic', 'polo', 'henley',
        'pants', 'trousers', 'jeans', 'denim', 'chinos', 'khakis', 'leggings', 'joggers', 'sweatpants',
        'dress', 'gown', 'frock', 'maxi', 'midi', 'mini', 'cocktail', 'evening', 'casual', 'formal',
        'skirt', 'shorts', 'bermuda', 'capri', 'culottes', 'palazzo', 'dhoti', 'salwar', 'kurta',
        'jacket', 'blazer', 'coat', 'overcoat', 'windbreaker', 'bomber', 'denim jacket', 'leather jacket',
        'sweater', 'cardigan', 'pullover', 'hoodie', 'sweatshirt', 'jumper', 'vest', 'waistcoat',
        'lingerie', 'underwear', 'bra', 'panties', 'boxers', 'briefs', 'sleepwear', 'nightwear', 'pajamas',
        'swimwear', 'bikini', 'swimsuit', 'beachwear', 'boardshorts', 'rashguard', 'coverup',
        'ethnic', 'traditional', 'saree', 'lehenga', 'anarkali', 'churidar', 'dupatta', 'sherwani',
        'maternity', 'pregnancy', 'nursing', 'plus size', 'petite', 'tall', 'big', 'slim fit', 'regular fit'
    ],

    'fashion_footwear': [
        'shoes', 'footwear', 'sneakers', 'trainers', 'running shoes', 'walking shoes', 'athletic shoes',
        'boots', 'ankle boots', 'knee boots', 'combat boots', 'hiking boots', 'work boots', 'rain boots',
        'sandals', 'flip flops', 'slides', 'slippers', 'moccasins', 'loafers', 'boat shoes',
        'heels', 'high heels', 'stilettos', 'pumps', 'wedges', 'platforms', 'kitten heels',
        'flats', 'ballet flats', 'oxfords', 'brogues', 'derbies', 'monk straps', 'chelsea boots',
        'formal shoes', 'dress shoes', 'casual shoes', 'sports shoes', 'basketball shoes', 'tennis shoes',
        'soccer cleats', 'football boots', 'golf shoes', 'cycling shoes', 'skating shoes',
        'kids shoes', 'baby shoes', 'toddler shoes', 'school shoes', 'uniform shoes'
    ],

    'fashion_accessories': [
        'accessories', 'jewelry', 'jewellery', 'necklace', 'earrings', 'bracelet', 'ring', 'pendant',
        'watch', 'smartwatch', 'fitness tracker', 'timepiece', 'chronograph', 'digital watch', 'analog watch',
        'bag', 'handbag', 'purse', 'clutch', 'tote', 'satchel', 'crossbody', 'shoulder bag', 'backpack',
        'wallet', 'purse', 'cardholder', 'money clip', 'coin purse', 'travel wallet', 'passport holder',
        'belt', 'leather belt', 'fabric belt', 'chain belt', 'designer belt', 'casual belt', 'formal belt',
        'sunglasses', 'eyewear', 'reading glasses', 'prescription glasses', 'contact lenses', 'frames',
        'hat', 'cap', 'beanie', 'fedora', 'baseball cap', 'snapback', 'bucket hat', 'beret', 'headband',
        'scarf', 'shawl', 'stole', 'muffler', 'bandana', 'neck warmer', 'infinity scarf',
        'tie', 'bow tie', 'necktie', 'cufflinks', 'tie clip', 'pocket square', 'suspenders',
        'gloves', 'mittens', 'fingerless gloves', 'driving gloves', 'winter gloves', 'work gloves'
    ],
    
    'electronics': [
        'electronics', 'gadgets', 'technology', 'tech', 'digital', 'smart',
        'phone', 'smartphone', 'mobile', 'tablet', 'laptop', 'computer', 'pc',
        'tv', 'television', 'monitor', 'screen', 'display', 'camera', 'video',
        'headphones', 'earphones', 'speakers', 'audio', 'gaming', 'console',
        'charger', 'cable', 'adapter', 'battery', 'power bank', 'wireless'
    ],
    
    'food': [
        'food', 'restaurant', 'dining', 'meal', 'eat', 'delivery', 'takeaway',
        'pizza', 'burger', 'sandwich', 'pasta', 'rice', 'chicken', 'beef',
        'vegetarian', 'vegan', 'organic', 'healthy', 'snacks', 'drinks',
        'coffee', 'tea', 'juice', 'water', 'grocery', 'supermarket', 'fresh'
    ],
    
    'travel': [
        'travel', 'trip', 'vacation', 'holiday', 'tour', 'journey', 'flight',
        'hotel', 'accommodation', 'booking', 'reservation', 'ticket', 'visa',
        'passport', 'luggage', 'suitcase', 'backpack', 'cruise', 'resort',
        'destination', 'adventure', 'explore', 'international', 'domestic'
    ],
    
    'beauty': [
        'beauty', 'cosmetics', 'makeup', 'skincare', 'haircare', 'personal care',
        'lipstick', 'foundation', 'mascara', 'eyeshadow', 'blush', 'concealer',
        'moisturizer', 'cleanser', 'serum', 'cream', 'lotion', 'shampoo',
        'conditioner', 'perfume', 'fragrance', 'nail', 'manicure', 'pedicure'
    ],
    
    'home': [
        'home', 'house', 'furniture', 'decor', 'interior', 'design', 'living',
        'bedroom', 'kitchen', 'bathroom', 'dining', 'office', 'garden',
        'appliances', 'refrigerator', 'washing machine', 'microwave', 'oven',
        'sofa', 'bed', 'table', 'chair', 'cabinet', 'storage', 'lighting'
    ],
    
    'health': [
        'health', 'healthcare', 'medical', 'medicine', 'pharmacy', 'fitness',
        'wellness', 'nutrition', 'supplement', 'vitamin', 'protein', 'gym',
        'exercise', 'workout', 'yoga', 'meditation', 'therapy', 'treatment',
        'doctor', 'hospital', 'clinic', 'insurance', 'organic', 'natural'
    ],
    
    'entertainment': [
        'entertainment', 'movie', 'film', 'cinema', 'theater', 'music', 'song',
        'album', 'concert', 'show', 'performance', 'streaming', 'netflix',
        'amazon prime', 'disney', 'spotify', 'youtube', 'gaming', 'game',
        'book', 'ebook', 'magazine', 'newspaper', 'subscription', 'premium'
    ],
    
    'automotive': [
        'car', 'auto', 'vehicle', 'automotive', 'bike', 'motorcycle', 'scooter',
        'truck', 'suv', 'sedan', 'hatchback', 'fuel', 'petrol', 'diesel',
        'electric', 'hybrid', 'insurance', 'service', 'maintenance', 'parts',
        'accessories', 'tires', 'battery', 'oil', 'garage', 'mechanic'
    ],
    
    'education': [
        'education', 'learning', 'course', 'training', 'skill', 'study',
        'school', 'college', 'university', 'online', 'tutorial', 'class',
        'book', 'textbook', 'exam', 'test', 'certification', 'degree',
        'diploma', 'language', 'programming', 'coding', 'software', 'app'
    ]
}
