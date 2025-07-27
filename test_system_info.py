#!/usr/bin/env python3
"""
Test script for Jarvis system information features
This script tests all the new system monitoring capabilities
"""

import os
import sys
import time

# Add the parent directory to the path so we can import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Import the functions we want to test from main.py
    from main import (
        get_system_info,
        get_battery_status,
        get_network_info,
        get_location_info,
        get_disk_space,
        get_weather_info
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you've installed all required packages with: pip install psutil requests")
    sys.exit(1)

def test_feature(name, function, *args):
    """Test a feature function and print the result"""
    print(f"\n{'=' * 50}")
    print(f"Testing: {name}")
    print(f"{'-' * 50}")
    
    try:
        result = function(*args)
        print(result)
        print(f"\n✅ {name} test completed successfully")
        return True
    except Exception as e:
        print(f"❌ Error in {name}: {e}")
        return False

def main():
    """Main function to test all system information features"""
    print("\n🧪 JARVIS SYSTEM INFORMATION TEST 🧪")
    print("=" * 50)
    
    # List of tests to run
    tests = [
        ("System Information", get_system_info),
        ("Battery Status", get_battery_status),
        ("Network Information", get_network_info),
        ("Location Information", get_location_info),
        ("Disk Space", get_disk_space),
        ("Weather (Default Location)", get_weather_info)
    ]
    
    # Run all tests
    results = {}
    for name, function in tests:
        results[name] = test_feature(name, function)
    
    # Extra test with custom location
    if results.get("Weather (Default Location)", False):
        test_feature("Weather (Custom Location)", get_weather_info, "Tokyo")
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("-" * 50)
    
    success_count = sum(1 for success in results.values() if success)
    print(f"✅ {success_count}/{len(tests)} tests passed")
    
    # Print any failures
    failures = [name for name, success in results.items() if not success]
    if failures:
        print(f"❌ Failed tests: {', '.join(failures)}")
    else:
        print("🎉 All tests passed successfully!")

if __name__ == "__main__":
    main()
