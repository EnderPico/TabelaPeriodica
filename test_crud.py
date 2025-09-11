"""
Comprehensive CRUD Testing Script for Periodic Table API
Tests all Create, Read, Update, Delete operations

Run this script to verify all CRUD endpoints work correctly
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_crud_operations():
    """Test all CRUD operations for elements"""
    print("🧪 Testing Periodic Table API - CRUD Operations")
    print("=" * 60)
    
    try:
        # Test 1: Get all elements (initial state)
        print("\n1. 📋 Testing GET /elements (initial state)")
        response = requests.get(f"{BASE_URL}/elements")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            elements = response.json()
            print(f"   Found {len(elements)} elements initially")
            for element in elements:
                print(f"   - {element['symbol']}: {element['name']}")
        print()
        
        # Test 2: Create new element
        print("2. ➕ Testing POST /elements (create Oxygen)")
        new_element = {
            "symbol": "O",
            "name": "Oxygen",
            "number": 8,
            "info": "Essential for respiration and combustion. Makes up about 21% of Earth's atmosphere."
        }
        
        response = requests.post(
            f"{BASE_URL}/elements",
            json=new_element,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Created: {result['message']}")
            print(f"   Element ID: {result['element']['id']}")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 3: Get specific element
        print("3. 🔍 Testing GET /elements/O (get Oxygen)")
        response = requests.get(f"{BASE_URL}/elements/O")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            element = response.json()
            print(f"   ✅ Found: {element['name']} ({element['symbol']})")
            print(f"   Atomic Number: {element['number']}")
            print(f"   Info: {element['info'][:50]}...")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 4: Update element
        print("4. ✏️  Testing PUT /elements/O (update Oxygen info)")
        update_data = {
            "info": "Updated description: Essential for life and combustion processes. Critical for cellular respiration."
        }
        
        response = requests.put(
            f"{BASE_URL}/elements/O",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Updated: {result['message']}")
            print(f"   New info: {result['element']['info'][:50]}...")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 5: Verify update
        print("5. 🔍 Testing GET /elements/O (verify update)")
        response = requests.get(f"{BASE_URL}/elements/O")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            element = response.json()
            print(f"   ✅ Verified: {element['name']}")
            print(f"   Updated info: {element['info'][:50]}...")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 6: Test case-insensitive search
        print("6. 🔍 Testing GET /elements/o (case-insensitive)")
        response = requests.get(f"{BASE_URL}/elements/o")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            element = response.json()
            print(f"   ✅ Found with lowercase: {element['name']} ({element['symbol']})")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 7: Create another element
        print("7. ➕ Testing POST /elements (create Nitrogen)")
        new_element2 = {
            "symbol": "N",
            "name": "Nitrogen",
            "number": 7,
            "info": "Makes up 78% of Earth's atmosphere. Essential for proteins and DNA."
        }
        
        response = requests.post(
            f"{BASE_URL}/elements",
            json=new_element2,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Created: {result['message']}")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 8: Get all elements (after additions)
        print("8. 📋 Testing GET /elements (after additions)")
        response = requests.get(f"{BASE_URL}/elements")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            elements = response.json()
            print(f"   Found {len(elements)} elements now")
            for element in elements:
                print(f"   - {element['symbol']}: {element['name']}")
        print()
        
        # Test 9: Try to create duplicate element
        print("9. ❌ Testing POST /elements (duplicate - should fail)")
        duplicate_element = {
            "symbol": "H",
            "name": "Hydrogen",
            "number": 1,
            "info": "This should fail - already exists"
        }
        
        response = requests.post(
            f"{BASE_URL}/elements",
            json=duplicate_element,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            error = response.json()
            print(f"   ✅ Correctly rejected: {error['detail']}")
        else:
            print(f"   ❌ Unexpected success: {response.json()}")
        print()
        
        # Test 10: Delete element
        print("10. 🗑️  Testing DELETE /elements/N (delete Nitrogen)")
        response = requests.delete(f"{BASE_URL}/elements/N")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Deleted: {result['message']}")
        else:
            print(f"   ❌ Error: {response.json()}")
        print()
        
        # Test 11: Verify deletion
        print("11. 🔍 Testing GET /elements/N (should be deleted)")
        response = requests.get(f"{BASE_URL}/elements/N")
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            error = response.json()
            print(f"   ✅ Correctly not found: {error['detail']}")
        else:
            print(f"   ❌ Unexpected: {response.json()}")
        print()
        
        # Test 12: Final state
        print("12. 📋 Testing GET /elements (final state)")
        response = requests.get(f"{BASE_URL}/elements")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            elements = response.json()
            print(f"   Found {len(elements)} elements in final state")
            for element in elements:
                print(f"   - {element['symbol']}: {element['name']}")
        print()
        
        print("🎉 All CRUD tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_crud_operations()
