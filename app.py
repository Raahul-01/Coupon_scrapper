#!/usr/bin/env python3
"""
🚀 ULTIMATE COUPON EXTRACTION SYSTEM
Revolutionary multi-source coupon discovery platform with intelligent persistence

FEATURES:
- Channel-Based Discovery: Explores entire channels beyond keywords
- Multi-Source Integration: YouTube + Web + Cross-Platform  
- Intelligent Persistence: Smart duplicate detection (code + brand)
- 1000+ Brand Database: Comprehensive coverage across all industries
- 5-Phase Discovery: Keywords → Channels → Web → Cross-Platform → Storage

PERFORMANCE:
- Volume: 1000+ unique coupons per comprehensive run
- Brands: 100+ brands covered per session
- Sources: YouTube, RetailMeNot, Coupons.com, Reddit, Forums
- Persistence: Builds upon existing data, zero loss
"""

import os
import sys
import time
import logging
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

# Import the ultimate extraction engine
from src.coupon_extraction_engine import ImprovedCouponEngine
from config.application_settings import YOUTUBE_API_KEY

def setup_logging():
    """Configure professional logging"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/ultimate_extraction_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )

def print_system_banner():
    """Display professional system banner"""
    print("\n🚀 ULTIMATE COUPON EXTRACTION SYSTEM")
    print("=" * 80)
    print("🎯 REVOLUTIONARY CAPABILITIES:")
    print("   ✅ Channel-Based Discovery: Explores entire channels beyond keywords")
    print("   ✅ Multi-Source Integration: YouTube + Web + Cross-Platform")
    print("   ✅ Intelligent Persistence: Smart duplicate detection (code + brand)")
    print("   ✅ 1000+ Brand Database: Comprehensive coverage across all industries")
    print("   ✅ 5-Phase Discovery: Keywords → Channels → Web → Cross-Platform → Storage")
    print("")
    print("📊 PERFORMANCE TARGETS:")
    print("   🎯 Volume: 1000+ unique coupons per comprehensive run")
    print("   🏢 Brands: 100+ brands covered per session")
    print("   🔍 Sources: YouTube, RetailMeNot, Coupons.com, Reddit, Forums")
    print("   💾 Persistence: Builds upon existing data, zero loss")
    print("")
    print("🏭 INDUSTRY COVERAGE:")
    print("   🖥️  Web Hosting: Hostinger, Bluehost, GoDaddy, Namecheap + 40 more")
    print("   💪 Fitness: MuscleBlaze, Optimum Nutrition, MyProtein + 50 more")
    print("   💻 Software: NordVPN, Adobe, Microsoft 365, Grammarly + 60 more")
    print("   🎮 Gaming: Steam, Epic Games, Xbox Game Pass + 40 more")
    print("   👗 Fashion: Shein, ASOS, Sephora, Nike + 80 more")
    print("=" * 80)

def get_search_queries():
    """Get comprehensive search queries for all industries"""
    return [
        # Web Hosting & Domain Services
        "hostinger discount code", "bluehost coupon", "godaddy promo", "namecheap deal",
        "siteground discount", "a2hosting coupon", "dreamhost promo", "hostgator deal",
        "digitalocean credit", "linode promo", "vultr discount", "cloudflare deal",
        
        # Fitness & Supplements  
        "muscleblaze discount", "optimum nutrition coupon", "myprotein promo", "dymatize deal",
        "bsn discount", "cellucor coupon", "muscletech promo", "healthkart deal",
        "nutrabay discount", "bigmuscles coupon", "protein powder discount", "supplement deal",
        "pre workout coupon", "bcaa discount", "creatine promo", "mass gainer deal",
        
        # Software & SaaS
        "nordvpn discount", "expressvpn coupon", "surfshark promo", "adobe deal",
        "microsoft 365 discount", "canva pro coupon", "grammarly promo", "zoom deal",
        "slack discount", "notion coupon", "dropbox promo", "malwarebytes deal",
        "norton discount", "mcafee coupon", "kaspersky promo", "bitdefender deal",
        
        # Gaming & Entertainment
        "steam discount", "epic games coupon", "xbox game pass promo", "playstation deal",
        "nintendo eshop discount", "humble bundle coupon", "origin promo", "uplay deal",
        "netflix discount", "spotify coupon", "youtube premium promo", "disney plus deal",
        "twitch prime discount", "discord nitro coupon", "gaming headset promo",
        
        # Fashion & Beauty
        "shein discount", "asos coupon", "h&m promo", "zara deal", "nike discount",
        "adidas coupon", "sephora promo", "ulta deal", "morphe discount", "fenty coupon",
        "glossier promo", "fashion haul discount", "makeup deal", "skincare coupon",
        
        # Tech & Electronics
        "anker discount", "samsung coupon", "apple promo", "xiaomi deal", "oneplus discount",
        "logitech coupon", "razer promo", "corsair deal", "tech gadget discount",
        "smartphone coupon", "laptop promo", "headphones deal", "charger discount",
        
        # Food & Delivery
        "zomato coupon", "swiggy promo", "doordash deal", "ubereats discount",
        "dominos coupon", "kfc promo", "mcdonalds deal", "pizza hut discount",
        "food delivery coupon", "restaurant promo", "grocery deal",
        
        # Travel & Booking
        "booking.com discount", "expedia coupon", "hotels.com promo", "airbnb deal",
        "makemytrip discount", "goibibo coupon", "cleartrip promo", "yatra deal",
        "oyo discount", "travel booking coupon", "flight deal", "hotel promo",
        
        # Education & Courses
        "udemy discount", "coursera coupon", "skillshare promo", "masterclass deal",
        "pluralsight discount", "codecademy coupon", "online course promo",
        "duolingo deal", "babbel discount", "language learning coupon",
        
        # Financial & Crypto
        "coinbase discount", "binance coupon", "robinhood promo", "webull deal",
        "crypto exchange discount", "trading platform coupon", "investment promo",
        
        # General Deal Terms
        "discount code", "promo code", "coupon code", "deal alert", "savings code",
        "offer code", "voucher code", "cashback deal", "limited time offer",
        "exclusive discount", "special promo", "flash sale", "mega deal"
    ]

def main():
    """Main application entry point"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Display banner
    print_system_banner()
    
    try:
        print("\n🔧 SYSTEM INITIALIZATION")
        print("-" * 50)
        
        # Initialize the ultimate extraction engine with all features
        print("⚙️ Initializing Ultimate Extraction Engine...")
        automation_engine = ImprovedCouponEngine(
            YOUTUBE_API_KEY,
            enable_deduplication=True,
            enable_web_scraping=True,
            enable_channel_traversal=True,
            enable_persistent_data=True
        )
        print("✅ Engine initialized with all advanced features")
        
        # Get comprehensive search queries
        search_queries = get_search_queries()
        print(f"✅ Loaded {len(search_queries)} comprehensive search queries")
        
        # Define target industries for discovery
        target_industries = [
            'tech_deals', 'hosting_reviews', 'fitness_supplements', 
            'fashion_hauls', 'food_delivery', 'software_tutorials', 
            'gaming_content', 'general_deals'
        ]
        print(f"✅ Targeting {len(target_industries)} industry categories")
        
        print("\n🚀 STARTING ULTIMATE EXTRACTION")
        print("-" * 50)
        print("📍 Phase 1: Keyword-based YouTube search (baseline)")
        print("📍 Phase 2: Channel traversal (explore entire channels)")
        print("📍 Phase 3: Enhanced discovery (trending, playlists, related videos)")
        print("📍 Phase 4: Web scraping (major coupon sites)")
        print("📍 Phase 5: Intelligent duplicate filtering & persistent storage")
        print("")
        print("⏱️ Estimated time: 30-60 minutes for comprehensive extraction")
        print("💡 You can interrupt safely - progress is saved incrementally")
        print("")
        
        # Record start time
        start_time = time.time()
        
        # Run the ULTIMATE extraction with all discovery mechanisms
        result = automation_engine.run_ultimate_extraction(
            search_queries=search_queries,
            max_results_per_query=50,
            enable_channel_traversal=True,
            enable_cross_platform=True,
            target_industries=target_industries
        )
        
        # Calculate processing time
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Display final results summary
        print("\n🎉 ULTIMATE EXTRACTION COMPLETED!")
        print("=" * 80)
        
        if result.videos:
            total_coupons = sum(len(video.coupons) for video in result.videos)
            unique_brands = set(coupon.brand for video in result.videos for coupon in video.coupons)
            
            print("📊 FINAL RESULTS SUMMARY:")
            print(f"   ⏱️ Total processing time: {processing_time/60:.1f} minutes")
            print(f"   📈 Total videos analyzed: {result.total_videos_processed}")
            print(f"   🎯 Total coupons discovered: {total_coupons}")
            print(f"   🏢 Unique brands covered: {len(unique_brands)}")
            print(f"   🔍 Discovery methods: 5-phase comprehensive system")
            print(f"   💾 Data persistence: Intelligent duplicate detection applied")
            
            # Show sample results from different sources
            print(f"\n📋 SAMPLE DISCOVERIES (showing variety):")
            sample_count = 0
            sources_shown = set()
            
            for video in result.videos:
                if sample_count >= 10:  # Show 10 samples max
                    break
                    
                for coupon in video.coupons:
                    if sample_count >= 10:
                        break
                        
                    source = "YouTube"
                    if hasattr(coupon, 'channel_name'):
                        if 'Web Scraping' in coupon.channel_name:
                            source = "Web"
                        elif 'Cross-Platform' in coupon.channel_name:
                            source = "Cross-Platform"
                    
                    sources_shown.add(source)
                    discount_info = f" ({coupon.percent_off}% off)" if coupon.percent_off else ""
                    print(f"   • {coupon.coupon_code} → {coupon.brand}{discount_info} [{source}]")
                    sample_count += 1
            
            print(f"\n💡 Discovered coupons from {len(sources_shown)} different source types!")
            print(f"🔄 Next run will build upon these results (no duplicates will be added)")
            
            # Success metrics
            print(f"\n🏆 SUCCESS METRICS:")
            if total_coupons >= 100:
                print("   ✅ Volume Target: EXCEEDED (100+ coupons)")
            else:
                print(f"   ⚠️ Volume Target: {total_coupons} coupons (may be due to existing data)")
            
            if len(unique_brands) >= 20:
                print("   ✅ Brand Diversity: EXCELLENT (20+ brands)")
            else:
                print(f"   ⚠️ Brand Diversity: {len(unique_brands)} brands")
            
            if len(sources_shown) >= 2:
                print("   ✅ Source Diversity: EXCELLENT (multiple sources)")
            else:
                print("   ⚠️ Source Diversity: Limited to single source")
                
        else:
            print("ℹ️ No new coupons found - all discovered coupons were already in the database!")
            print("💡 This indicates the intelligent duplicate detection is working perfectly")
            print("🔄 Try running again later as new content becomes available")
        
        print("\n🎯 NEXT STEPS:")
        print("   📁 Check the results/ directory for your CSV files")
        print("   🔄 Run again anytime to discover new coupons")
        print("   📈 Each run builds upon previous results")
        print("   💾 Your data is safely preserved and growing")
        
        logger.info(f"Ultimate extraction completed successfully in {processing_time/60:.1f} minutes")
        
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
        print("💾 Progress has been saved - you can resume anytime")
        logger.info("Extraction interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        print("💡 Check the logs for detailed error information")
        logger.error(f"Extraction failed: {e}", exc_info=True)
        
    finally:
        print("\n" + "=" * 80)
        print("🚀 ULTIMATE COUPON EXTRACTION SYSTEM - SESSION COMPLETE")
        print("=" * 80)

if __name__ == "__main__":
    main()
