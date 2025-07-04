#!/usr/bin/env python3
"""
ENHANCED BRAND DATABASE
Comprehensive database of brands across all industries with focus on niche markets
"""

# HOSTING & DOMAIN SERVICES (Comprehensive List)
HOSTING_BRANDS = [
    # Major Hosting Providers
    'Hostinger', 'Bluehost', 'GoDaddy', 'Namecheap', 'SiteGround', 'A2Hosting',
    'DreamHost', 'HostGator', 'InMotion', 'Cloudflare', 'DigitalOcean', 'Linode',
    'Vultr', 'AWS', 'Google Cloud', 'Microsoft Azure', 'Heroku', 'Netlify', 'Vercel',
    
    # Specialized Hosting
    'WP Engine', 'Kinsta', 'Flywheel', 'Pressable', 'Pagely', 'WPX Hosting',
    'Rocket.net', 'Cloudways', 'GridPane', 'SpinupWP', 'RunCloud', 'Ploi',
    
    # VPS & Cloud Providers
    'OVHcloud', 'Hetzner', 'Contabo', 'Time4VPS', 'InterServer', 'Hostwinds',
    'LiquidWeb', 'Media Temple', 'Rackspace', 'IBM Cloud', 'Oracle Cloud',
    
    # Domain Registrars
    'Porkbun', 'Dynadot', 'Gandi', 'Hover', 'Name.com', 'Domain.com',
    'Epik', 'Tucows', 'Enom', 'Network Solutions', 'Register.com',
    
    # CDN & Security
    'MaxCDN', 'KeyCDN', 'BunnyCDN', 'Fastly', 'Amazon CloudFront',
    'Sucuri', 'Wordfence', 'SiteLock', 'Malcare', 'Jetpack',
    
    # Email Hosting
    'ProtonMail', 'Tutanota', 'FastMail', 'Zoho Mail', 'Titan Email',
    'Microsoft 365', 'Google Workspace', 'ImprovMX', 'ForwardEmail'
]

# FITNESS & SUPPLEMENT BRANDS (Massive Expansion)
FITNESS_BRANDS = [
    # Protein & Supplements
    'MuscleBlaze', 'Optimum Nutrition', 'Dymatize', 'BSN', 'Cellucor', 'MuscleTech',
    'Universal Nutrition', 'Labrada', 'Isopure', 'Gold Standard', 'Serious Mass',
    'MyProtein', 'Prozis', 'Bulk Powders', 'Protein Works', 'Applied Nutrition',
    'Grenade', 'PhD Nutrition', 'Reflex Nutrition', 'Sci-MX', 'Maximuscle',
    'USN Nutrition', 'Kaged Muscle', 'Ghost Supplements', 'Ryse Supplements',
    'Gorilla Mode', 'CBUM', 'Raw Nutrition', 'Axe & Sledge', 'Bucked Up',
    
    # Indian Fitness Brands
    'Avvatar Whey', 'Bigmuscles Nutrition', 'AS-IT-IS Nutrition', 'Proburst',
    'Nutrabay', 'HealthKart', 'MuscleXP', 'Steadfast Nutrition', 'Absolute Nutrition',
    'Ultimate Nutrition', 'Muscle Asylum', 'Dextro Energy', 'Fast&Up',
    
    # Pre-Workout & Energy
    'C4 Energy', 'Bang Energy', 'Reign', 'Monster Energy', 'Red Bull',
    'Celsius', 'Alani Nu', 'Psychotic', 'Mr. Hyde', 'NO-Xplode',
    'Jack3d', 'Mesomorph', 'Total War', 'Woke AF', 'Crack',
    
    # Fat Burners & Weight Loss
    'Hydroxycut', 'Leanmode', 'CLA', 'L-Carnitine', 'Green Tea Extract',
    'Forskolin', 'Garcinia Cambogia', 'Raspberry Ketones', 'Yohimbine',
    
    # Fitness Equipment Brands
    'Bowflex', 'NordicTrack', 'Peloton', 'Schwinn', 'ProForm', 'Sole Fitness',
    'Life Fitness', 'Precor', 'Matrix', 'Cybex', 'Hammer Strength',
    'PowerBlock', 'Adjustable Dumbbells', 'Resistance Bands', 'TRX',
    
    # Fitness Apparel
    'Gymshark', 'Alphalete', 'YoungLA', 'NVGTN', 'Echt', 'Ryderwear',
    'Born Primitive', 'Noble', 'Ten Thousand', 'Lululemon', 'Under Armour',
    'Nike Training', 'Adidas Performance', 'Puma Training'
]

# SOFTWARE & SAAS BRANDS (Comprehensive)
SOFTWARE_BRANDS = [
    # Creative Software
    'Adobe Creative Cloud', 'Adobe Photoshop', 'Adobe Illustrator', 'Adobe Premiere',
    'Adobe After Effects', 'Adobe InDesign', 'Adobe Lightroom', 'Adobe XD',
    'Canva Pro', 'Figma', 'Sketch', 'InVision', 'Framer', 'Principle',
    'Affinity Designer', 'Affinity Photo', 'Affinity Publisher', 'CorelDRAW',
    'PaintShop Pro', 'Luminar', 'Capture One', 'DxO PhotoLab',
    
    # Productivity & Office
    'Microsoft 365', 'Google Workspace', 'Notion', 'Obsidian', 'Roam Research',
    'Evernote', 'OneNote', 'Bear', 'Ulysses', 'Scrivener', 'Grammarly',
    'ProWritingAid', 'Hemingway Editor', 'Todoist', 'Any.do', 'TickTick',
    'Asana', 'Monday.com', 'Trello', 'ClickUp', 'Basecamp', 'Wrike',
    
    # VPN & Security
    'NordVPN', 'ExpressVPN', 'Surfshark', 'CyberGhost', 'Private Internet Access',
    'IPVanish', 'Hotspot Shield', 'TunnelBear', 'ProtonVPN', 'Windscribe',
    'Malwarebytes', 'Norton', 'McAfee', 'Kaspersky', 'Bitdefender', 'Avast',
    'AVG', 'ESET', 'Trend Micro', 'F-Secure', 'Sophos',
    
    # Cloud Storage
    'Dropbox', 'Google Drive', 'OneDrive', 'iCloud', 'Box', 'pCloud',
    'MEGA', 'Sync.com', 'Tresorit', 'SpiderOak', 'Backblaze', 'Carbonite',
    
    # Communication
    'Zoom', 'Microsoft Teams', 'Slack', 'Discord', 'Telegram', 'WhatsApp Business',
    'Skype', 'Google Meet', 'GoToMeeting', 'WebEx', 'BlueJeans',
    
    # Development Tools
    'GitHub', 'GitLab', 'Bitbucket', 'Visual Studio Code', 'JetBrains',
    'Sublime Text', 'Atom', 'Brackets', 'CodePen', 'JSFiddle', 'Replit',
    'Heroku', 'Netlify', 'Vercel', 'Railway', 'PlanetScale', 'Supabase'
]

# GAMING & ENTERTAINMENT BRANDS
GAMING_BRANDS = [
    # Gaming Platforms
    'Steam', 'Epic Games Store', 'Origin', 'Uplay', 'GOG', 'Humble Bundle',
    'Xbox Game Pass', 'PlayStation Plus', 'Nintendo eShop', 'Battle.net',
    'Rockstar Games Launcher', 'Bethesda Launcher', 'Twitch Prime Gaming',
    
    # Gaming Hardware
    'Razer', 'Corsair', 'Logitech G', 'SteelSeries', 'HyperX', 'ASUS ROG',
    'MSI Gaming', 'Alienware', 'NZXT', 'Cooler Master', 'Thermaltake',
    'Roccat', 'Turtle Beach', 'Astro Gaming', 'Audio-Technica Gaming',
    
    # Streaming Services
    'Netflix', 'Amazon Prime Video', 'Disney+', 'Hulu', 'HBO Max', 'Apple TV+',
    'Paramount+', 'Peacock', 'Discovery+', 'ESPN+', 'Showtime', 'Starz',
    'Crunchyroll', 'Funimation', 'VRV', 'Tubi', 'Pluto TV',
    
    # Music Streaming
    'Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 'Tidal',
    'Deezer', 'Pandora', 'SoundCloud', 'Bandcamp', 'Qobuz'
]

# FASHION & BEAUTY BRANDS (Niche Focus)
FASHION_BRANDS = [
    # Fast Fashion & Online
    'Shein', 'Romwe', 'Zaful', 'YesStyle', 'AliExpress Fashion', 'Wish Fashion',
    'Temu Fashion', 'Boohoo', 'PrettyLittleThing', 'Missguided', 'Nasty Gal',
    'ASOS', 'Urban Outfitters', 'Forever 21', 'H&M', 'Zara', 'Mango',
    
    # Beauty & Cosmetics
    'Sephora', 'Ulta Beauty', 'Morphe', 'Fenty Beauty', 'Rare Beauty',
    'Glossier', 'Kylie Cosmetics', 'Jeffree Star Cosmetics', 'Tarte',
    'Too Faced', 'Urban Decay', 'NARS', 'MAC Cosmetics', 'Maybelline',
    'L\'Oreal', 'Revlon', 'CoverGirl', 'NYX Professional Makeup',
    
    # Skincare
    'The Ordinary', 'CeraVe', 'Neutrogena', 'Olay', 'Clinique', 'Estee Lauder',
    'Drunk Elephant', 'Paula\'s Choice', 'Kiehl\'s', 'Origins', 'Fresh',
    'Tatcha', 'Glow Recipe', 'Youth to the People', 'Herbivore Botanicals'
]

# TECH GADGETS & ELECTRONICS
TECH_BRANDS = [
    # Accessories & Chargers
    'Anker', 'Aukey', 'RAVPower', 'UGREEN', 'Baseus', 'Belkin', 'Spigen',
    'OtterBox', 'UAG', 'Peak Design', 'Moment', 'DJI', 'GoPro', 'Insta360',
    
    # Audio
    'Sony WH-1000XM4', 'Bose QuietComfort', 'AirPods Pro', 'Sennheiser',
    'Audio-Technica', 'Beyerdynamic', 'Focal', 'Grado', 'Audeze', 'Hifiman',
    'JBL', 'Harman Kardon', 'Bang & Olufsen', 'Marshall', 'Beats',
    
    # Smart Home
    'Philips Hue', 'LIFX', 'Nest', 'Ecobee', 'Ring', 'Arlo', 'Wyze',
    'TP-Link Kasa', 'Amazon Echo', 'Google Nest', 'Apple HomePod'
]

# FOOD & NUTRITION BRANDS
FOOD_BRANDS = [
    # Meal Delivery
    'HelloFresh', 'Blue Apron', 'Home Chef', 'Sunbasket', 'Green Chef',
    'Purple Carrot', 'Factor', 'Freshly', 'Gobble', 'EveryPlate',
    
    # Health Foods
    'Thrive Market', 'Vitacost', 'iHerb', 'Swanson', 'NOW Foods',
    'Jarrow Formulas', 'Solgar', 'Nature Made', 'Garden of Life',
    'Rainbow Light', 'New Chapter', 'MegaFood', 'Country Life'
]

# TRAVEL & BOOKING SERVICES
TRAVEL_BRANDS = [
    # Booking Platforms
    'Booking.com', 'Expedia', 'Hotels.com', 'Priceline', 'Kayak', 'Skyscanner',
    'Momondo', 'Trivago', 'Agoda', 'Orbitz', 'Travelocity', 'CheapTickets',
    
    # Indian Travel
    'MakeMyTrip', 'Goibibo', 'Cleartrip', 'Yatra', 'ixigo', 'EaseMyTrip',
    'Paytm Travel', 'Ola Travel', 'Redbus', 'AbhiBus',
    
    # Accommodation
    'Airbnb', 'Vrbo', 'HomeAway', 'Vacasa', 'RedAwning', 'FlipKey',
    'OYO', 'Treebo', 'FabHotels', 'Zostel', 'Backpacker Panda'
]

# EDUCATION & ONLINE COURSES
EDUCATION_BRANDS = [
    # Online Learning
    'Udemy', 'Coursera', 'Skillshare', 'MasterClass', 'Pluralsight',
    'LinkedIn Learning', 'Codecademy', 'Treehouse', 'DataCamp', 'Brilliant',
    'Khan Academy', 'edX', 'Udacity', 'FutureLearn', 'Domestika',
    
    # Language Learning
    'Duolingo', 'Babbel', 'Rosetta Stone', 'Busuu', 'Memrise', 'italki',
    'Preply', 'Cambly', 'HelloTalk', 'Tandem', 'FluentU'
]

# FINANCIAL & CRYPTO SERVICES
FINANCIAL_BRANDS = [
    # Crypto Exchanges
    'Coinbase', 'Binance', 'Kraken', 'Gemini', 'KuCoin', 'Huobi', 'OKX',
    'Crypto.com', 'FTX', 'Bitfinex', 'Bitstamp', 'Coinmama', 'Changelly',
    
    # Investment Platforms
    'Robinhood', 'Webull', 'E*TRADE', 'TD Ameritrade', 'Fidelity', 'Schwab',
    'Interactive Brokers', 'M1 Finance', 'Acorns', 'Stash', 'Betterment',
    
    # Indian Fintech
    'Zerodha', 'Upstox', 'Angel Broking', 'Groww', 'Paytm Money', 'ETMONEY',
    'Kuvera', 'Coin by Zerodha', 'INDmoney', 'Scripbox'
]

# COMPREHENSIVE BRAND MAPPING
ALL_BRANDS = {
    'hosting': HOSTING_BRANDS,
    'fitness': FITNESS_BRANDS,
    'software': SOFTWARE_BRANDS,
    'gaming': GAMING_BRANDS,
    'fashion': FASHION_BRANDS,
    'tech': TECH_BRANDS,
    'food': FOOD_BRANDS,
    'travel': TRAVEL_BRANDS,
    'education': EDUCATION_BRANDS,
    'financial': FINANCIAL_BRANDS
}

# Flatten all brands for general use
ALL_BRANDS_FLAT = []
for category_brands in ALL_BRANDS.values():
    ALL_BRANDS_FLAT.extend(category_brands)

# Remove duplicates and sort
ALL_BRANDS_FLAT = sorted(list(set(ALL_BRANDS_FLAT)))

def get_brands_by_category(category: str) -> list:
    """Get brands for a specific category"""
    return ALL_BRANDS.get(category.lower(), [])

def get_all_brands() -> list:
    """Get all brands across all categories"""
    return ALL_BRANDS_FLAT

def is_known_brand(brand_name: str) -> bool:
    """Check if a brand is in our database"""
    return brand_name.title() in ALL_BRANDS_FLAT

def get_brand_category(brand_name: str) -> str:
    """Get the category of a brand"""
    brand_title = brand_name.title()
    for category, brands in ALL_BRANDS.items():
        if brand_title in brands:
            return category
    return 'general'
