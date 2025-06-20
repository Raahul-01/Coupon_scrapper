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

from src.coupon_extraction_engine import ProfessionalCouponEngine
from src.business_intelligence_models import ScrapingResult

def main():
    """Professional coupon automation system execution"""
    
    print("🚀 PROFESSIONAL COUPON AUTOMATION SYSTEM")
    print("=" * 70)
    print("✅ 7 Key Information Fields (Title, Code, Brand, %, Date, Description, Category)")
    print("✅ Complete Description Analysis (entire content analysis)")
    print("✅ Smart Duplicate Prevention (intelligent tracking)")
    print("✅ Clean Content Processing (no repeated sentences)")
    print("✅ Brand Intelligence (context-based detection)")
    print("✅ Dynamic Title Generation (meaningful naming)")
    print("✅ Single File Consolidation (unified output)")
    print("✅ Broad Market Coverage (comprehensive keywords)")
    print("✅ High Volume Processing (10K+ target capability)")
    print("✅ Enterprise Organization (professional structure)")
    print("=" * 70)
    
    try:
        # Initialize professional automation engine
        automation_engine = ProfessionalCouponEngine(enable_smart_features=True)
        
        # Get comprehensive market keywords
        market_keywords = automation_engine.get_comprehensive_market_keywords()
        print(f"🎯 Processing {len(market_keywords)} comprehensive market areas...")
        print(f"📈 TESTING MODE: Target 500 coupons for testing purposes")
        
        today = datetime.now().strftime("%Y%m%d")
        output_directory = f"results/coupon_intelligence_{today}"
        os.makedirs(output_directory, exist_ok=True)
        
        print(f"📁 Output directory: {output_directory}")
        print("=" * 70)
        
        start_time = time.time()
        all_results = []
        total_coupons = 0
        total_videos = 0
        
        # Process market coverage - LIMITED TO 500 COUPONS FOR TESTING
        for i, keyword in enumerate(market_keywords, 1):
            print(f"\n🔍 [{i}/{len(market_keywords)}] Market analysis: '{keyword}'")

            # STOP when we reach 500 coupons for testing
            if total_coupons >= 500:
                print(f"\n🎯 TESTING LIMIT REACHED: {total_coupons} coupons found!")
                break
            
            try:
                # Use intelligence to get fresh content only
                fresh_content_ids = automation_engine.get_fresh_content(keyword, max_results=30)
                
                if not fresh_content_ids:
                    print(f"   ℹ️ No new content found for '{keyword}'")
                    continue
                
                # Process with complete intelligence analysis
                processing_result = automation_engine.process_content_batch(fresh_content_ids)
                
                if processing_result.total_coupons_found > 0:
                    # Apply intelligence filtering
                    filtered_result = automation_engine.apply_intelligence_filtering(processing_result)
                    
                    if filtered_result.total_coupons_found > 0:
                        all_results.append(filtered_result)
                        total_coupons += filtered_result.total_coupons_found
                        total_videos += len(filtered_result.videos)
                        
                        print(f"   ✅ NEW: {filtered_result.total_coupons_found} coupons from {len(filtered_result.videos)} videos")
                        print(f"   📊 Running total: {total_coupons:,} NEW coupons")
                    else:
                        print(f"   🔄 All content was duplicate")
                else:
                    print(f"   ℹ️ No coupons found in new content")
                
                # Efficient processing for broad coverage
                time.sleep(0.2)
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        # Generate professional output with intelligence
        if all_results:
            # Consolidate all results
            consolidated_result = ScrapingResult()
            for result in all_results:
                consolidated_result.total_videos_processed += result.total_videos_processed
                consolidated_result.total_coupons_found += result.total_coupons_found
                consolidated_result.videos.extend(result.videos)
            
            # Export to professional format with 7 key fields
            output_filename = f"{output_directory}/COUPON_INTELLIGENCE_7_FIELDS_{today}.csv"
            automation_engine.export_professional_intelligence(consolidated_result, output_filename)
            
            # Save intelligence history for future processing
            automation_engine.save_intelligence_history()
            
            # Generate comprehensive business intelligence report
            create_business_intelligence_report(consolidated_result, total_coupons, total_videos, output_directory, today)
            
            # Professional success metrics
            duration = (time.time() - start_time) / 60
            print(f"\n🎉 PROFESSIONAL AUTOMATION SUCCESS!")
            print(f"📊 BUSINESS INTELLIGENCE METRICS:")
            print(f"   🎫 Total NEW coupons: {total_coupons:,}")
            print(f"   🎬 Total NEW videos: {total_videos:,}")
            print(f"   ⏱️ Processing duration: {duration:.1f} minutes")
            print(f"   📈 Processing rate: {total_coupons/duration:.0f} coupons/minute")
            print(f"   📁 Professional output: {output_filename}")
            print(f"   🎯 Contains ALL 7 key fields with complete intelligence!")
            print(f"   🧠 Intelligence history saved for future automation")
        else:
            print("\n⚠️ No new content found - all available content was already processed")
        
    except KeyboardInterrupt:
        print("\n⚠️ Automation stopped by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")

def create_business_intelligence_report(result, total_coupons, total_videos, output_directory, today):
    """Generate comprehensive business intelligence report"""
    
    report_file = f"{output_directory}/BUSINESS_INTELLIGENCE_REPORT_{today}.txt"
    
    # Analyze business metrics
    categories = {}
    brands = {}
    
    for video in result.videos:
        for coupon in video.coupons:
            # Category intelligence
            category = coupon.category or 'general'
            categories[category] = categories.get(category, 0) + 1
            
            # Brand intelligence
            brand = coupon.brand or 'unknown'
            brands[brand] = brands.get(brand, 0) + 1
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"PROFESSIONAL COUPON AUTOMATION SYSTEM - BUSINESS INTELLIGENCE REPORT\n")
        f.write(f"Generated: {today}\n")
        f.write("=" * 90 + "\n\n")
        
        f.write(f"🚀 PROFESSIONAL FEATURES IMPLEMENTED:\n")
        f.write(f"✅ 7 Key Information Fields\n")
        f.write(f"✅ Single File Consolidation\n")
        f.write(f"✅ Broad Market Coverage\n")
        f.write(f"✅ Smart Duplicate Prevention\n")
        f.write(f"✅ Complete Content Analysis\n")
        f.write(f"✅ Clean Content Processing\n")
        f.write(f"✅ Brand Intelligence\n")
        f.write(f"✅ Dynamic Title Generation\n")
        f.write(f"✅ High Volume Processing\n")
        f.write(f"✅ Enterprise Organization\n\n")
        
        f.write(f"📊 BUSINESS INTELLIGENCE OVERVIEW:\n")
        f.write(f"Total NEW Coupons: {total_coupons:,}\n")
        f.write(f"Total NEW Videos: {total_videos:,}\n")
        f.write(f"Total Market Categories: {len(categories)}\n")
        f.write(f"Total Brand Partners: {len(brands)}\n\n")
        
        f.write(f"📂 MARKET CATEGORY INTELLIGENCE:\n")
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{category.title()}: {count:,} coupons\n")
        
        f.write(f"\n🏷️ BRAND PARTNER INTELLIGENCE:\n")
        for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True)[:30]:
            f.write(f"{brand}: {count:,} coupons\n")
        
        f.write(f"\n🎯 7 KEY FIELDS IN PROFESSIONAL OUTPUT:\n")
        f.write(f"1. Coupon Title (dynamic generation from intelligence)\n")
        f.write(f"2. Coupon Code (pattern-based extraction)\n")
        f.write(f"3. Brand (context-based intelligence)\n")
        f.write(f"4. Discount Percent (percentage intelligence)\n")
        f.write(f"5. Expiry Date (date pattern intelligence)\n")
        f.write(f"6. Discount Description (clean processing)\n")
        f.write(f"7. Category (market intelligence)\n")
    
    print(f"📄 Business intelligence report: {report_file}")

if __name__ == "__main__":
    main()
