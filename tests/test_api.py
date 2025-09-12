"""
Test script for the Periodic Table API - Day 2 Database Version
Run this after starting the server to verify everything works with the database
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing Periodic Table API...")
    print("=" * 50)
    
    try:
        # Test root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test health check
        print("2. Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Test get all elements
        print("3. Testing get all elements...")
        response = requests.get(f"{BASE_URL}/elements")
        print(f"   Status: {response.status_code}")
        elements = response.json()
        print(f"   Found {len(elements)} elements")
        for element in elements:
            print(f"   - {element['symbol']}: {element['name']}")
        print()
        
        # Test get specific elements
        test_symbols = ["H", "He", "INVALID"]
        
        for symbol in test_symbols:
            print(f"4. Testing get element '{symbol}'...")
            response = requests.get(f"{BASE_URL}/elements/{symbol}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                element = response.json()
                print(f"   Found: {element['name']} ({element['symbol']})")
                print(f"   Atomic Number: {element['number']}")
                print(f"   Info: {element['info'][:50]}...")
            else:
                print(f"   Error: {response.json()}")
            print()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
