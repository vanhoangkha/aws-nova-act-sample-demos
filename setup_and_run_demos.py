#!/usr/bin/env python3
"""
Setup and Run Nova Act Demos
============================

This script helps you set up and run the Nova Act demo suite.
"""

import os
import sys
from getpass import getpass

def setup_api_key():
    """Help user set up their Nova Act API key."""
    print("Nova Act API Key Setup")
    print("=" * 40)
    print()
    print("To run the Nova Act demos, you need an API key from:")
    print("https://nova.amazon.com/act")
    print()
    
    # Check if API key is already set
    existing_key = os.getenv('NOVA_ACT_API_KEY')
    if existing_key:
        print(f"API key is already set: {existing_key[:8]}...{existing_key[-8:]}")
        use_existing = input("Use existing API key? (y/n): ").lower().strip()
        if use_existing == 'y':
            return existing_key
    
    print("Please enter your Nova Act API key:")
    print("(It should look like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)")
    
    api_key = getpass("API Key: ").strip()
    
    if not api_key:
        print("No API key provided")
        return None
    
    # Basic validation
    if len(api_key) < 30:
        print("Warning: API key seems too short. Please verify it's correct.")
    
    # Set environment variable for this session
    os.environ['NOVA_ACT_API_KEY'] = api_key
    
    print("API key set for this session")
    print()
    print("To set it permanently, add this to your shell profile:")
    print(f"   export NOVA_ACT_API_KEY='{api_key}'")
    print()
    
    return api_key

def run_enhanced_demos():
    """Run the enhanced demo suite."""
    print("Starting Enhanced Nova Act Demo Suite")
    print("=" * 50)
    
    try:
        # Import and run the enhanced demo suite
        from demo_framework import ConfigManager, Logger
        
        # Show environment info
        config_manager = ConfigManager()
        env_info = config_manager.detect_environment()
        
        print(f"Environment: {env_info.country_code} ({env_info.region})")
        print(f"Platform: {env_info.platform}")
        print(f"Python: {env_info.python_version}")
        print()
        
        # Show optimal sites for user's region
        ecommerce_sites = config_manager.get_optimal_sites("ecommerce")
        print(f"E-commerce sites for your region: {ecommerce_sites}")
        
        news_sites = config_manager.get_optimal_sites("news")
        print(f"News sites for your region: {news_sites}")
        print()
        
        # Run the actual demo suite
        print("Running enhanced demo suite...")
        import subprocess
        result = subprocess.run([sys.executable, "run_all_demos.py"], 
                              capture_output=False, text=True)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running demos: {e}")
        return False

def main():
    """Main function."""
    print("Nova Act Demo Suite Setup & Runner")
    print("=" * 50)
    print()
    
    # Step 1: Set up API key
    api_key = setup_api_key()
    if not api_key:
        print("Cannot run demos without API key")
        print()
        print("To get an API key:")
        print("   1. Visit https://nova.amazon.com/act")
        print("   2. Sign up or log in")
        print("   3. Generate an API key")
        print("   4. Run this script again")
        sys.exit(1)
    
    # Step 2: Run demos
    print("Ready to run demos!")
    proceed = input("Run all demos now? (y/n): ").lower().strip()
    
    if proceed == 'y':
        success = run_enhanced_demos()
        if success:
            print("\nAll demos completed!")
        else:
            print("\nSome demos encountered issues (this is normal)")
            print("The enhanced framework provides detailed error handling and reporting.")
    else:
        print("\nTo run demos later:")
        print("   python run_all_demos.py")
    
    print("\nEnhanced framework features:")
    print("   • Geographic awareness and site selection")
    print("   • Robust error handling with graceful degradation")
    print("   • Comprehensive logging and reporting")
    print("   • Fallback strategies for reliability")
    print("   • Production-ready monitoring")

if __name__ == "__main__":
    main()