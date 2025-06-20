#!/usr/bin/env python3
"""
Test script untuk Fizzo automation endpoint
"""

import asyncio
import json
import sys
from datetime import datetime

async def test_fizzo_endpoint():
    """Test Fizzo automation endpoint dengan dummy data"""
    
    print("🧪 Testing Fizzo Automation Endpoint")
    print("=" * 50)
    
    # Import modules
    try:
        import httpx
        print("✅ httpx available")
    except ImportError:
        print("❌ httpx not available, installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "httpx"])
        import httpx
        print("✅ httpx installed and imported")
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "password": "test_password",
        "chapter_title": f"Test Chapter - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "chapter_content": "Ini adalah test chapter untuk automation fizzo.org. " * 50 + 
                          "Chapter ini berisi minimal 1000 karakter untuk memenuhi requirement fizzo.org. " * 10 +
                          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20
    }
    
    print(f"📝 Test Data:")
    print(f"   Email: {test_data['email']}")
    print(f"   Chapter Title: {test_data['chapter_title']}")
    print(f"   Content Length: {len(test_data['chapter_content'])} characters")
    print()
    
    # Test endpoint
    base_url = "http://localhost:7860"
    endpoint = f"{base_url}/api/fizzo-auto-update"
    
    print(f"🎯 Testing endpoint: {endpoint}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print("🚀 Sending POST request...")
            
            response = await client.post(
                endpoint,
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"📊 Response Status: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            try:
                result = response.json()
                print(f"📊 Response Body:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                
                if response.status_code == 200:
                    if result.get("success"):
                        print("✅ Test PASSED: Endpoint responded successfully")
                    else:
                        print("⚠️  Test WARNING: Endpoint responded but automation failed")
                        print(f"   Error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"❌ Test FAILED: HTTP {response.status_code}")
                    
            except json.JSONDecodeError:
                print(f"❌ Test FAILED: Invalid JSON response")
                print(f"   Raw response: {response.text}")
                
    except httpx.ConnectError:
        print("❌ Test FAILED: Cannot connect to server")
        print("   Make sure the server is running on localhost:7860")
        print("   Run: python app.py")
        
    except Exception as e:
        print(f"❌ Test FAILED: Unexpected error")
        print(f"   Error: {e}")
    
    print()
    print("🏁 Test completed")

def test_validation():
    """Test input validation"""
    print("\n🧪 Testing Input Validation")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        {
            "name": "Empty email",
            "data": {"email": "", "password": "test", "chapter_title": "Test", "chapter_content": "x" * 1000},
            "should_fail": True
        },
        {
            "name": "Empty password", 
            "data": {"email": "test@test.com", "password": "", "chapter_title": "Test", "chapter_content": "x" * 1000},
            "should_fail": True
        },
        {
            "name": "Short content",
            "data": {"email": "test@test.com", "password": "test", "chapter_title": "Test", "chapter_content": "short"},
            "should_fail": True
        },
        {
            "name": "Valid data",
            "data": {"email": "test@test.com", "password": "test", "chapter_title": "Test", "chapter_content": "x" * 1000},
            "should_fail": False
        }
    ]
    
    for case in test_cases:
        print(f"📝 {case['name']}: ", end="")
        
        # Basic validation logic (mimic the endpoint validation)
        data = case['data']
        
        if not data.get('email') or not data.get('password'):
            result = "FAIL - Missing credentials"
        elif not data.get('chapter_title') or not data.get('chapter_content'):
            result = "FAIL - Missing chapter data"
        elif len(data.get('chapter_content', '')) < 1000:
            result = "FAIL - Content too short"
        elif len(data.get('chapter_content', '')) > 60000:
            result = "FAIL - Content too long"
        else:
            result = "PASS - Valid data"
            
        expected = "FAIL" if case['should_fail'] else "PASS"
        actual = result.split(" - ")[0]
        
        if expected == actual:
            print(f"✅ {result}")
        else:
            print(f"❌ Expected {expected}, got {actual}")

if __name__ == "__main__":
    print("🚀 Fizzo Automation Test Suite")
    print("=" * 50)
    
    # Test validation first
    test_validation()
    
    # Test endpoint (requires server running)
    print("\n" + "=" * 50)
    print("⚠️  Note: The following test requires the server to be running")
    print("   Start server with: python app.py")
    print("   Then run this test in another terminal")
    print("=" * 50)
    
    try:
        asyncio.run(test_fizzo_endpoint())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")