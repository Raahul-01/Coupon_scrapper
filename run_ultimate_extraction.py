#!/usr/bin/env python3
"""
🚀 ULTIMATE COUPON EXTRACTION - QUICK RUN SCRIPT
Professional launcher for the Ultimate Coupon Extraction System
"""

import os
import sys
import subprocess
from datetime import datetime

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import pandas
        import requests
        import beautifulsoup4
        from googleapiclient.discovery import build
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if YouTube API key is configured"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
        from config.application_settings import YOUTUBE_API_KEY
        
        if YOUTUBE_API_KEY and YOUTUBE_API_KEY != 'YOUR_API_KEY_HERE':
            print("✅ YouTube API key is configured")
            return True
        else:
            print("❌ YouTube API key not configured")
            print("💡 Edit config/application_settings.py and add your API key")
            return False
    except ImportError:
        print("❌ Configuration file not found")
        print("💡 Make sure config/application_settings.py exists")
        return False

def main():
    """Main launcher"""
    print("🚀 ULTIMATE COUPON EXTRACTION SYSTEM - LAUNCHER")
    print("=" * 60)
    print(f"📅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Pre-flight checks
    print("🔍 PRE-FLIGHT CHECKS:")
    print("-" * 30)
    
    if not check_requirements():
        return
    
    if not check_api_key():
        return
    
    print("✅ All checks passed - ready for extraction!")
    print()
    
    # Launch the main application
    print("🚀 LAUNCHING ULTIMATE EXTRACTION SYSTEM...")
    print("=" * 60)
    
    try:
        # Run the main application
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n⚠️ Extraction interrupted by user")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Extraction failed with error code: {e.returncode}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    finally:
        print("\n" + "=" * 60)
        print("🏁 LAUNCHER SESSION COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    main()
