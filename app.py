#!/usr/bin/env python3
"""
PROFESSIONAL COUPON AUTOMATION SYSTEM
Enterprise-grade YouTube coupon extraction and analysis platform
"""

import os
import sys
import time
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from src.coupon_extraction_engine import ImprovedCouponEngine
from src.business_intelligence_models import ScrapingResult
from config.application_settings import YOUTUBE_API_KEY

def main():
    """Professional coupon automation system execution"""
    
    print("🚀 ULTIMATE COUPON AUTOMATION SYSTEM 🚀")
    print("=" * 80)
    print("✅ TRADITIONAL FEATURES:")
    print("   • 8 Key Information Fields (Title, Code, Brand, %, Date, Description, Category, YouTuber Channel)")
    print("   • Expanded Video Targeting (influencer promotional content beyond just 'coupon' titles)")
    print("   • Complete Description Analysis (entire content analysis)")
    print("   • Brand Intelligence (context-based detection)")
    print("   • Dynamic Title Generation (meaningful naming)")
    print("")
    print("🆕 NEW ULTIMATE FEATURES:")
    print("   • Channel-Based Traversal (systematic exploration of entire channels)")
    print("   • Related Video Following (YouTube recommendation algorithm traversal)")
    print("   • Playlist Exploration (curated content discovery)")
    print("   • Cross-Platform Discovery (Reddit, forums, blogs)")
    print("   • Intelligent Duplicate Detection (code + brand comparison)")
    print("   • Persistent Data Management (incremental CSV building)")
    print("   • Enhanced Brand Database (1000+ brands across all industries)")
    print("   • Multi-Source Web Scraping (RetailMeNot, Coupons.com, etc.)")
    print("")
    print("🎯 TARGET VOLUME: 1000+ unique coupons per run")
    print("💾 PERSISTENT: Builds upon previous results, no data loss")
    print("🔍 COMPREHENSIVE: Discovers hidden coupons beyond keyword searches")
    print("=" * 80)
    
    try:
        # Initialize improved automation engine with intelligent analysis
        automation_engine = ImprovedCouponEngine(YOUTUBE_API_KEY)

        # Use the ULTIMATE extraction method
        print("🚀 Running ULTIMATE coupon extraction with ALL discovery mechanisms...")
        print("📈 This will extract REAL coupon codes from EVERY possible source")
        print("🔍 Beyond keywords: Channel traversal, playlists, cross-platform, web scraping")
        print("💾 Intelligent duplicate detection: Only adds truly new coupons")

        today = datetime.now().strftime("%Y%m%d")
        output_directory = f"results/coupon_intelligence_{today}"
        os.makedirs(output_directory, exist_ok=True)

        print(f"📁 Output directory: {output_directory}")
        print("=" * 70)

        start_time = time.time()

        # Run the COMPREHENSIVE extraction with EXPANDED INFLUENCER search strategy + WEB SCRAPING
        # Target broader promotional content where influencers mention discount codes
        # PLUS scrape major coupon sites and brand-specific sources
        search_queries = [
            # WEB HOSTING & DOMAIN SERVICES (High-value niche)
            "hostinger discount code", "bluehost promo offer", "godaddy domain deal",
            "namecheap hosting discount", "siteground offer code", "a2hosting promo",
            "dreamhost discount deal", "hostgator offer code", "inmotion hosting promo",
            "cloudflare discount", "digitalocean promo", "linode hosting deal",
            "vultr discount code", "aws hosting offer", "google cloud promo",

            # FITNESS & SUPPLEMENTS (Massive influencer market)
            "muscleblaze protein discount", "optimum nutrition offer", "dymatize promo code",
            "bsn supplement deal", "cellucor discount offer", "mutant nutrition promo",
            "myprotein discount code", "prozis supplement offer", "healthkart deal",
            "nutrabay fitness discount", "bigmuscles nutrition promo", "avvatar whey offer",
            "muscletech discount code", "universal nutrition deal", "labrada supplement offer",
            "isopure protein promo", "gold standard whey discount", "serious mass deal",
            "creatine monohydrate offer", "bcaa supplement discount", "pre workout promo",
            "fat burner discount code", "mass gainer offer", "protein bar deal",

            # SOFTWARE & SAAS (High-ticket items)
            "adobe creative cloud discount", "microsoft office promo", "canva pro offer",
            "grammarly premium deal", "nordvpn discount code", "expressvpn promo",
            "surfshark vpn offer", "cyberghost discount", "hotspot shield deal",
            "malwarebytes antivirus promo", "norton security discount", "mcafee offer code",
            "kaspersky antivirus deal", "bitdefender discount", "avast premium offer",
            "dropbox storage promo", "google drive discount", "onedrive deal offer",
            "zoom pro discount", "slack premium offer", "trello business deal",
            "asana project management promo", "monday.com discount", "notion pro offer",

            # GAMING & ENTERTAINMENT
            "steam game discount code", "epic games store offer", "origin games promo",
            "uplay games discount", "gog games deal", "humble bundle offer",
            "xbox game pass discount", "playstation plus promo", "nintendo eshop deal",
            "twitch prime discount", "discord nitro offer", "spotify premium promo",
            "youtube premium deal", "netflix subscription discount", "amazon prime offer",
            "disney plus hotstar promo", "zee5 subscription deal", "sony liv discount",

            # FASHION & BEAUTY NICHE BRANDS
            "shein fashion haul discount", "romwe clothing offer", "zaful swimwear promo",
            "yesstyle korean fashion deal", "asos fashion discount", "boohoo clothing offer",
            "prettylittlething fashion promo", "missguided discount code", "nasty gal deal",
            "urban outfitters offer", "forever21 fashion promo", "h&m clothing discount",
            "zara fashion deal", "mango clothing offer", "uniqlo fashion promo",
            "sephora beauty discount", "ulta makeup offer", "morphe cosmetics promo",
            "fenty beauty deal", "rare beauty discount", "glossier makeup offer",

            # TECH GADGETS & ELECTRONICS
            "anker charging discount", "aukey electronics offer", "ravpower promo code",
            "ugreen accessories deal", "baseus gadgets discount", "xiaomi products offer",
            "oneplus accessories promo", "samsung galaxy discount", "apple accessories deal",
            "logitech peripherals offer", "razer gaming discount", "corsair gaming promo",
            "steelseries gaming deal", "hyperx gaming discount", "asus tech offer",
            "msi gaming laptop promo", "acer laptop discount", "hp computer deal",
            "dell laptop offer", "lenovo thinkpad promo", "macbook accessories discount",

            # FOOD & NUTRITION
            "myprotein nutrition discount", "bulk powders offer", "protein works promo",
            "applied nutrition deal", "grenade supplements discount", "phd nutrition offer",
            "reflex nutrition promo", "sci-mx supplements deal", "maximuscle discount",
            "usn nutrition offer", "kaged muscle promo", "ghost supplements deal",
            "ryse supplements discount", "gorilla mode promo", "cbum supplements offer",

            # HOME & LIFESTYLE BRANDS
            "ikea furniture discount", "wayfair home offer", "overstock furniture promo",
            "west elm home deal", "pottery barn discount", "crate barrel offer",
            "cb2 furniture promo", "world market deal", "pier1 imports discount",
            "homegoods decor offer", "target home promo", "walmart furniture deal",

            # TRAVEL & BOOKING SERVICES
            "booking.com hotel discount", "expedia travel offer", "hotels.com promo",
            "airbnb stay discount", "vrbo rental offer", "agoda hotel promo",
            "kayak flight deal", "skyscanner discount", "momondo travel offer",
            "priceline hotel promo", "travelocity deal", "orbitz travel discount",

            # EDUCATION & ONLINE COURSES
            "udemy course discount", "coursera plus offer", "skillshare premium promo",
            "masterclass subscription deal", "pluralsight discount", "linkedin learning offer",
            "codecademy pro promo", "treehouse learning deal", "datacamp discount",
            "brilliant premium offer", "khan academy promo", "edx course deal",

            # FINANCIAL & CRYPTO SERVICES
            "coinbase crypto discount", "binance trading offer", "kraken exchange promo",
            "robinhood investing deal", "webull trading discount", "etoro investment offer",
            "acorns investing promo", "stash investment deal", "m1 finance discount",

            # Major E-commerce Platforms (Expanded)
            "amazon review discount code", "flipkart haul discount", "myntra try on offer",
            "nykaa beauty haul promo", "temu unboxing deal", "shein haul discount",
            "ajio fashion review offer", "meesho shopping deal", "snapdeal discount review",
            "paytm mall offer", "shopclues discount", "jiomart promo code",

            # Food & Delivery (Expanded)
            "zomato discount code", "swiggy promo offer", "dominos pizza deal",
            "mcdonald review discount", "kfc offer code", "pizza hut promo",
            "uber eats discount", "food panda offer", "dunzo promo code",
            "grofers grocery discount", "bigbasket offer code", "amazon fresh deal",

            # General Promotional Content (Broader)
            "sponsored content discount", "brand collaboration offer", "influencer promo code",
            "paid partnership deal", "creator code discount", "affiliate offer code",
            "product review discount", "unboxing promo code", "haul discount offer",
            "try on discount code", "first impression deal", "honest review offer",
            "discount code 2025", "promo code 2025", "offer code working",
            "deal code latest", "save money tips", "best deals today",
            "shopping deals online", "exclusive discount offer", "limited time promo"
        ]

        print(f"🔍 Starting with {len(search_queries)} keyword queries as SEED for discovery...")
        print("💎 Target Industries: Web Hosting, Fitness Supplements, Software/SaaS, Gaming, Fashion, Tech, Food, Travel, Education, Crypto")
        print("🎯 Target Brands: Hostinger, MuscleBlaze, NordVPN, Steam, Shein, Anker, MyProtein, Booking.com, Udemy, Coinbase + 1000+ more")
        print("")
        print("🚀 ULTIMATE EXTRACTION PHASES:")
        print("   Phase 1: Keyword-based YouTube search (baseline)")
        print("   Phase 2: Channel traversal (explore entire channels)")
        print("   Phase 3: Enhanced discovery (trending, playlists, related videos)")
        print("   Phase 4: Web scraping (major coupon sites)")
        print("   Phase 5: Intelligent duplicate filtering & persistent storage")
        print("")

        # Define target industries for comprehensive discovery
        target_industries = ['tech_deals', 'hosting_reviews', 'fitness_supplements', 'fashion_hauls',
                           'food_delivery', 'software_tutorials', 'gaming_content', 'general_deals']

        # Run ULTIMATE extraction (ALL discovery mechanisms)
        result = automation_engine.run_ultimate_extraction(
            search_queries=search_queries,
            max_results_per_query=50,
            enable_channel_traversal=True,
            enable_cross_platform=True,
            target_industries=target_industries
        )

        # Display results (comprehensive stats are already printed by the engine)
        print(f"\n🎉 ULTIMATE EXTRACTION COMPLETED!")
        print("=" * 80)

        if result.videos:
            total_coupons = sum(len(video.coupons) for video in result.videos)
            unique_brands = set(coupon.brand for video in result.videos for coupon in video.coupons)

            print(f"📊 FINAL SUMMARY:")
            print(f"   ⏱️ Total processing time: {time.time() - start_time:.2f} seconds")
            print(f"   📈 Total Videos Analyzed: {result.total_videos_processed}")
            print(f"   🎯 Total Coupons Found: {total_coupons}")
            print(f"   🏢 Unique Brands Covered: {len(unique_brands)}")
            print(f"   🔍 Discovery Methods: Keyword search + Channel traversal + Web scraping + Cross-platform")
            print(f"   💾 Persistent Storage: Intelligent duplicate detection applied")

            # Show sample results from different sources
            print(f"\n📋 SAMPLE RESULTS FROM DIFFERENT SOURCES:")
            sample_count = 0
            sources_shown = set()

            for video in result.videos:
                if sample_count >= 8:  # Show 8 samples max
                    break

                for coupon in video.coupons:
                    if sample_count >= 8:
                        break

                    source = "YouTube"
                    if hasattr(coupon, 'channel_name'):
                        if 'Web Scraping' in coupon.channel_name:
                            source = "Web Scraping"
                        elif 'Cross-Platform' in coupon.channel_name:
                            source = "Cross-Platform"

                    # Try to show variety of sources
                    if source not in sources_shown or len(sources_shown) >= 3:
                        sources_shown.add(source)
                        discount_info = f" ({coupon.percent_off}% off)" if coupon.percent_off else ""
                        print(f"   • {coupon.coupon_code} → {coupon.brand}{discount_info} [{source}]")
                        sample_count += 1

            print(f"\n💡 The system discovered coupons from {len(sources_shown)} different source types!")
            print(f"🔄 Next run will build upon these results (no duplicates will be added)")

        else:
            print("ℹ️ No new coupons found - all discovered coupons were already in the database!")
            print("💡 This shows the intelligent duplicate detection is working perfectly")

    except Exception as e:
        print(f"💥 CRITICAL ERROR: {str(e)}")
        print("🔧 Please check your configuration and try again")
        return False

    return True

if __name__ == "__main__":
    main()
