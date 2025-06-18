#!/usr/bin/env python3
"""
Test script to verify the fixes for HF Spaces deployment
"""
import os
import sys
import requests
import time
import subprocess
import signal
from threading import Thread

def setup_test_environment():
    """Setup test environment variables"""
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    os.environ.setdefault("SERVE_FRONTEND", "false")
    os.environ.setdefault("DISABLE_SECURITY", "true")
    os.environ.setdefault("OPENHANDS_DISABLE_AUTH", "true")
    os.environ.setdefault("SETTINGS_STORE_TYPE", "memory")
    os.environ.setdefault("SECRETS_STORE_TYPE", "memory")
    os.environ.setdefault("FILE_STORE_PATH", "/tmp/openhands")
    os.environ.setdefault("WORKSPACE_BASE", "/tmp/workspace")
    os.environ.setdefault("CACHE_DIR", "/tmp/cache")
    
    # Create directories
    os.makedirs("/tmp/openhands", exist_ok=True)
    os.makedirs("/tmp/workspace", exist_ok=True)
    os.makedirs("/tmp/cache", exist_ok=True)

def test_endpoints():
    """Test various endpoints"""
    base_url = "http://localhost:7860"
    
    endpoints_to_test = [
        "/",
        "/health", 
        "/api/options/config",
        "/api/hf/status",
        "/api/hf/ready",
        "/api/hf/environment",
        "/api/hf/debug",
        "/api/hf/logs-container",
        "/api/hf/logs",
        "/api/simple/health",
        "/api/simple/test",
        "/docs",
        "/openapi.json"
    ]
    
    print("🧪 Testing endpoints...")
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200 and endpoint == "/":
                data = response.json()
                print(f"   Root response: {data.get('name', 'Unknown')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    # Test a non-existent endpoint to verify 404 handling
    try:
        response = requests.get(f"{base_url}/nonexistent", timeout=10)
        print(f"🔍 404 Test - Status: {response.status_code}")
        if response.status_code == 404:
            data = response.json()
            print(f"   404 Response: {data.get('message', 'No message')}")
    except Exception as e:
        print(f"❌ 404 Test failed: {e}")
    
    # Test POST endpoints
    print("\n🧪 Testing POST endpoints...")
    
    # Test HF test conversation endpoint
    try:
        response = requests.post(f"{base_url}/api/hf/test-conversation", timeout=10)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} POST /api/hf/test-conversation - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Test conversation ID: {data.get('conversation_id', 'None')}")
    except Exception as e:
        print(f"❌ POST /api/hf/test-conversation failed: {e}")
    
    # Test simple conversation endpoint
    try:
        test_data = {
            "message": "Hello, this is a test message"
        }
        response = requests.post(f"{base_url}/api/simple/conversation", json=test_data, timeout=10)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} POST /api/simple/conversation - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Conversation ID: {data.get('conversation_id', 'None')}")
            print(f"   Response: {data.get('response', 'None')}")
    except Exception as e:
        print(f"❌ POST /api/simple/conversation failed: {e}")
    
    # Test public conversations endpoint with minimal data
    try:
        test_data = {
            "initial_user_msg": "Hello, this is a test message",
            "repository": None,
            "selected_branch": None,
            "image_urls": [],
            "replay_json": None,
            "suggested_task": None,
            "git_provider": None,
            "conversation_instructions": None
        }
        response = requests.post(f"{base_url}/api/conversations", json=test_data, timeout=10)
        status = "✅" if response.status_code in [200, 400, 401] else "❌"  # Accept auth errors as expected
        print(f"{status} POST /api/conversations - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Conversation ID: {data.get('conversation_id', 'None')}")
        elif response.status_code in [400, 401]:
            data = response.json()
            print(f"   Expected error: {data.get('error_type', 'unknown')}")
    except Exception as e:
        print(f"❌ POST /api/conversations failed: {e}")

def run_server():
    """Run the server in a subprocess"""
    print("🚀 Starting server...")
    return subprocess.Popen([
        sys.executable, "app_hf.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def main():
    """Main test function"""
    print("🔧 Setting up test environment...")
    setup_test_environment()
    
    # Start server
    server_process = run_server()
    
    try:
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(10)
        
        # Test endpoints
        test_endpoints()
        
    finally:
        # Clean up
        print("🧹 Cleaning up...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()
        
        print("✅ Test completed!")

if __name__ == "__main__":
    main()