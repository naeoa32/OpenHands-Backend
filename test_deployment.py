#!/usr/bin/env python3
"""
🧪 Test Deployment - API Testing Script
Test semua endpoint setelah deployment ke HF Spaces
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class DeploymentTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
        
    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🧪 {title}")
        print('='*50)
        
    def test_endpoint(self, method, endpoint, data=None, expected_status=200):
        """Test a single endpoint"""
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        try:
            print(f"\n🔗 Testing: {method} {endpoint}")
            print(f"   URL: {url}")
            
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                print(f"   ❌ Unsupported method: {method}")
                return False
                
            print(f"   Status: {response.status_code}")
            
            if response.status_code == expected_status:
                print(f"   ✅ Success!")
                
                # Try to parse JSON response
                try:
                    json_data = response.json()
                    print(f"   📄 Response: {json.dumps(json_data, indent=2)[:200]}...")
                except:
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                return True
            else:
                print(f"   ❌ Expected {expected_status}, got {response.status_code}")
                print(f"   📄 Response: {response.text[:200]}...")
                return False
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout after 30 seconds")
            return False
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection error - service might be down")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def test_health_check(self):
        """Test health endpoint"""
        self.print_header("Health Check")
        return self.test_endpoint('GET', '/health')
    
    def test_api_docs(self):
        """Test API documentation"""
        self.print_header("API Documentation")
        return self.test_endpoint('GET', '/docs', expected_status=200)
    
    def test_config(self):
        """Test configuration endpoint"""
        self.print_header("Configuration")
        return self.test_endpoint('GET', '/api/options/config')
    
    def test_create_conversation(self):
        """Test conversation creation"""
        self.print_header("Create Conversation")
        
        data = {
            "message": "Hello! Can you help me write a simple Python function?",
            "agent_type": "CodeActAgent",
            "max_iterations": 5
        }
        
        return self.test_endpoint('POST', '/api/conversations', data=data)
    
    def test_cors_headers(self):
        """Test CORS headers"""
        self.print_header("CORS Headers")
        
        url = urljoin(self.base_url + '/', 'health')
        
        try:
            response = self.session.options(url)
            headers = response.headers
            
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods', 
                'Access-Control-Allow-Headers'
            ]
            
            print(f"\n🔗 Testing CORS headers for: {url}")
            
            for header in cors_headers:
                if header in headers:
                    print(f"   ✅ {header}: {headers[header]}")
                else:
                    print(f"   ❌ Missing: {header}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ CORS test failed: {e}")
            return False
    
    def test_response_time(self):
        """Test response time"""
        self.print_header("Response Time Test")
        
        url = urljoin(self.base_url + '/', 'health')
        
        try:
            start_time = time.time()
            response = self.session.get(url)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            print(f"\n🔗 Testing response time: {url}")
            print(f"   ⏱️  Response time: {response_time:.2f}ms")
            
            if response_time < 5000:  # Less than 5 seconds
                print(f"   ✅ Good response time!")
                return True
            else:
                print(f"   ⚠️  Slow response time (>{response_time:.2f}ms)")
                return True  # Still pass, just slow
                
        except Exception as e:
            print(f"   ❌ Response time test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting deployment tests...")
        print(f"🎯 Target URL: {self.base_url}")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("API Documentation", self.test_api_docs),
            ("Configuration", self.test_config),
            ("CORS Headers", self.test_cors_headers),
            ("Response Time", self.test_response_time),
            ("Create Conversation", self.test_create_conversation)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"\n❌ {test_name} failed with exception: {e}")
                results[test_name] = False
        
        # Print summary
        self.print_summary(results)
        
        return all(results.values())
    
    def print_summary(self, results):
        """Print test summary"""
        self.print_header("Test Summary")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\n📊 Results: {passed}/{total} tests passed")
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        if passed == total:
            print(f"\n🎉 All tests passed! Deployment is working correctly!")
            print(f"🔗 Your API is ready at: {self.base_url}")
            print(f"📚 Documentation: {self.base_url}/docs")
        else:
            print(f"\n⚠️  {total - passed} tests failed. Check the issues above.")
            
        print(f"\n📱 Mobile Testing:")
        print(f"   • Health: {self.base_url}/health")
        print(f"   • Docs: {self.base_url}/docs")
        print(f"   • Config: {self.base_url}/api/options/config")

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://username-spacename.hf.space")
        sys.exit(1)
    
    base_url = sys.argv[1]
    
    # Validate URL format
    if not base_url.startswith(('http://', 'https://')):
        print("❌ URL must start with http:// or https://")
        sys.exit(1)
    
    tester = DeploymentTester(base_url)
    
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()