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