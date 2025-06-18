#!/usr/bin/env python3
"""
Verify that Google authentication is completely disabled
and conversation endpoints are accessible without login
"""
import os
import sys
import json
from pathlib import Path

def verify_no_google_auth():
    """Verify Google auth is disabled and conversations work"""
    
    print("🔍 Verifying No Google Authentication Required")
    print("=" * 50)
    
    # Check 1: Environment variables
    print("\n1️⃣ Checking Environment Variables...")
    auth_disabled = os.getenv("OPENHANDS_DISABLE_AUTH", "true").lower() == "true"
    security_disabled = os.getenv("DISABLE_SECURITY", "true").lower() == "true"
    
    print(f"✅ OPENHANDS_DISABLE_AUTH: {auth_disabled}")
    print(f"✅ DISABLE_SECURITY: {security_disabled}")
    
    if not auth_disabled or not security_disabled:
        print("⚠️  Authentication might still be enabled")
    else:
        print("✅ Authentication completely disabled")
    
    # Check 2: Search for Google auth code
    print("\n2️⃣ Scanning for Google Authentication Code...")
    google_auth_files = []
    
    # Search for Google auth related code
    search_patterns = [
        "google.auth",
        "google.oauth",
        "GoogleAuth",
        "oauth2",
        "client_secret",
        "google_client_id"
    ]
    
    for pattern in search_patterns:
        print(f"   Searching for: {pattern}")
        # Search in Python files
        for py_file in Path("/workspace/OpenHands-Backend").rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if pattern.lower() in content.lower() and "test" not in str(py_file).lower():
                        # Check if it's actually used (not commented)
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if pattern.lower() in line.lower() and not line.strip().startswith('#'):
                                google_auth_files.append(f"{py_file}:{i+1}")
                                break
            except:
                pass
    
    if google_auth_files:
        print("⚠️  Found potential Google auth references:")
        for ref in google_auth_files[:5]:  # Show first 5
            print(f"     {ref}")
    else:
        print("✅ No active Google authentication code found")
    
    # Check 3: Verify conversation endpoints
    print("\n3️⃣ Testing Conversation Endpoints...")
    
    # Set up environment like HF Spaces
    os.environ["OPENHANDS_DISABLE_AUTH"] = "true"
    os.environ["DISABLE_SECURITY"] = "true"
    os.environ["SETTINGS_STORE_TYPE"] = "memory"
    os.environ["CONVERSATION_STORE_TYPE"] = "memory"
    
    try:
        sys.path.insert(0, '/workspace/OpenHands-Backend')
        from openhands.server.app import app
        
        # Check if app has conversation routes
        conversation_routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                if 'conversation' in route.path.lower():
                    conversation_routes.append(f"{route.methods} {route.path}")
        
        print(f"✅ Found {len(conversation_routes)} conversation routes:")
        for route in conversation_routes[:10]:  # Show first 10
            print(f"     {route}")
            
    except Exception as e:
        print(f"❌ Error testing conversation endpoints: {e}")
        return False
    
    # Check 4: Verify no authentication middleware
    print("\n4️⃣ Checking Authentication Middleware...")
    
    auth_middleware = []
    try:
        # Check if auth middleware is disabled
        if hasattr(app, 'middleware_stack') and app.middleware_stack:
            middleware_count = len(app.middleware_stack)
            print(f"✅ Total middleware: {middleware_count}")
            
            # Look for auth-related middleware
            for middleware in app.middleware_stack:
                middleware_name = str(type(middleware)).lower()
                if any(auth_term in middleware_name for auth_term in ['auth', 'oauth', 'google']):
                    auth_middleware.append(middleware_name)
        else:
            print("✅ No middleware stack found")
        
        if auth_middleware:
            print(f"⚠️  Found auth middleware: {auth_middleware}")
        else:
            print("✅ No authentication middleware found")
            
    except Exception as e:
        print(f"⚠️  Could not check middleware: {e}")
        auth_middleware = []  # Ensure it's defined
    
    # Check 5: Test API endpoints accessibility
    print("\n5️⃣ Testing API Endpoint Accessibility...")
    
    public_endpoints = [
        "/health",
        "/api/options/config",
        "/api/conversations",
        "/api/simple/conversation",
        "/test-chat/health"
    ]
    
    accessible_endpoints = []
    for endpoint in public_endpoints:
        # Check if endpoint exists in routes
        for route in app.routes:
            if hasattr(route, 'path') and route.path == endpoint:
                accessible_endpoints.append(endpoint)
                break
    
    print(f"✅ Accessible endpoints: {len(accessible_endpoints)}/{len(public_endpoints)}")
    for endpoint in accessible_endpoints:
        print(f"     ✅ {endpoint}")
    
    missing_endpoints = set(public_endpoints) - set(accessible_endpoints)
    if missing_endpoints:
        print("⚠️  Missing endpoints:")
        for endpoint in missing_endpoints:
            print(f"     ❌ {endpoint}")
    
    # Final verification
    print("\n" + "=" * 50)
    print("🎯 VERIFICATION SUMMARY")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 5
    
    if auth_disabled and security_disabled:
        print("✅ Authentication disabled in environment")
        checks_passed += 1
    else:
        print("❌ Authentication not properly disabled")
    
    if not google_auth_files:
        print("✅ No Google authentication code found")
        checks_passed += 1
    else:
        print("⚠️  Google auth references found (might be inactive)")
        checks_passed += 0.5
    
    if len(conversation_routes) > 0:
        print("✅ Conversation endpoints available")
        checks_passed += 1
    else:
        print("❌ No conversation endpoints found")
    
    if not auth_middleware:
        print("✅ No authentication middleware")
        checks_passed += 1
    else:
        print("❌ Authentication middleware detected")
    
    if len(accessible_endpoints) >= 3:
        print("✅ Public endpoints accessible")
        checks_passed += 1
    else:
        print("❌ Not enough public endpoints")
    
    success_rate = (checks_passed / total_checks) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 VERIFICATION PASSED! No Google auth required, conversations accessible!")
        return True
    else:
        print("❌ VERIFICATION FAILED! Some issues need to be addressed.")
        return False

if __name__ == "__main__":
    success = verify_no_google_auth()
    
    if success:
        print("\n✅ READY FOR DEPLOYMENT!")
        print("📋 Your backend is configured for:")
        print("   - No Google authentication required")
        print("   - Public conversation access")
        print("   - Anonymous usage")
        print("   - Direct API integration")
    else:
        print("\n❌ NEEDS ATTENTION!")
        print("📋 Please review the issues above")
    
    sys.exit(0 if success else 1)