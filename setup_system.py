#!/usr/bin/env python3
"""
🔧 ULTIMATE COUPON EXTRACTION SYSTEM - SETUP SCRIPT
Automated setup and configuration for the Ultimate Coupon Extraction System
"""

import os
import sys
import subprocess
from datetime import datetime

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = [
        "results",
        "logs", 
        "data",
        "test_results"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    return True

def check_config():
    """Check configuration file"""
    print("⚙️ Checking configuration...")
    
    config_file = "config/application_settings.py"
    
    if os.path.exists(config_file):
        print("   ✅ Configuration file exists")
        
        # Check if API key is set
        try:
            sys.path.append('config')
            from application_settings import YOUTUBE_API_KEY
            
            if YOUTUBE_API_KEY and YOUTUBE_API_KEY != 'YOUR_API_KEY_HERE':
                print("   ✅ YouTube API key is configured")
                return True
            else:
                print("   ⚠️ YouTube API key needs to be configured")
                print("   💡 Edit config/application_settings.py and add your API key")
                return False
                
        except ImportError:
            print("   ❌ Error reading configuration file")
            return False
    else:
        print("   ❌ Configuration file not found")
        return False

def run_system_test():
    """Run a quick system test"""
    print("🧪 Running system test...")
    
    try:
        # Test imports
        sys.path.append('src')
        from src.enhanced_brand_database import get_all_brands
        from src.persistent_data_manager import PersistentDataManager
        
        # Test brand database
        brands = get_all_brands()
        print(f"   ✅ Brand database loaded: {len(brands)} brands")
        
        # Test data manager
        data_manager = PersistentDataManager()
        summary = data_manager.get_existing_coupon_summary()
        print(f"   ✅ Data manager initialized: {summary['unique_codes']} existing codes")
        
        print("   ✅ All system components working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ System test failed: {e}")
        return False

def display_next_steps():
    """Display next steps for the user"""
    print("\n🎯 NEXT STEPS:")
    print("-" * 40)
    print("1. 🔑 Configure your YouTube API key in config/application_settings.py")
    print("2. 🚀 Run the system: python app.py")
    print("3. 🧪 Or test first: python test_ultimate_system.py")
    print("4. 📖 Read README_ULTIMATE.md for detailed documentation")
    print()
    print("🎉 Expected results:")
    print("   • 1000+ unique coupons per comprehensive run")
    print("   • 100+ brands covered per session")
    print("   • Multi-source discovery (YouTube + Web + Cross-platform)")
    print("   • Intelligent duplicate detection and persistent storage")

def main():
    """Main setup function"""
    print("🔧 ULTIMATE COUPON EXTRACTION SYSTEM - SETUP")
    print("=" * 60)
    print(f"📅 Setup started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = True
    
    # Step 1: Install requirements
    if not install_requirements():
        success = False
    
    print()
    
    # Step 2: Create directories
    if not create_directories():
        success = False
    
    print()
    
    # Step 3: Check configuration
    config_ok = check_config()
    if not config_ok:
        print("   ⚠️ Configuration needs attention (see next steps)")
    
    print()
    
    # Step 4: Run system test
    if config_ok and not run_system_test():
        success = False
    
    print()
    
    # Final status
    if success and config_ok:
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("✅ System is ready for ultimate coupon extraction")
    elif success:
        print("⚠️ SETUP MOSTLY COMPLETE")
        print("🔑 Just need to configure the YouTube API key")
    else:
        print("❌ SETUP ENCOUNTERED ISSUES")
        print("💡 Please resolve the errors above and run setup again")
    
    print()
    display_next_steps()
    
    print("\n" + "=" * 60)
    print("🔧 SETUP SCRIPT COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
