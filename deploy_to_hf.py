#!/usr/bin/env python3
"""
🚀 Deploy to Hugging Face Spaces - Helper Script
Memudahkan deployment dan testing untuk mobile users
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path

def print_banner():
    print("🤗" + "="*50)
    print("🚀 OpenHands → Hugging Face Spaces Deployer")
    print("📱 Mobile-Friendly Deployment Helper")
    print("="*52)

def check_environment():
    """Check if all required environment variables are set"""
    print("\n🔍 Checking environment...")
    
    required_vars = {
        'HF_TOKEN': 'Hugging Face API Token',
        'HF_USERNAME': 'Hugging Face Username', 
        'HF_SPACE_NAME': 'Hugging Face Space Name'
    }
    
    missing = []
    for var, desc in required_vars.items():
        if not os.getenv(var):
            missing.append(f"  ❌ {var} - {desc}")
        else:
            print(f"  ✅ {var} - Set")
    
    if missing:
        print("\n🚨 Missing environment variables:")
        for var in missing:
            print(var)
        print("\n💡 Set them in GitHub Secrets or local environment")
        return False
    
    return True

def test_hf_connection():
    """Test connection to Hugging Face API"""
    print("\n🔗 Testing Hugging Face connection...")
    
    token = os.getenv('HF_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get('https://huggingface.co/api/whoami', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"  ✅ Connected as: {user_info.get('name', 'Unknown')}")
            return True
        else:
            print(f"  ❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Connection error: {e}")
        return False

def check_space_exists():
    """Check if the target space exists"""
    print("\n🏠 Checking target space...")
    
    username = os.getenv('HF_USERNAME')
    space_name = os.getenv('HF_SPACE_NAME')
    token = os.getenv('HF_TOKEN')
    
    space_url = f"https://huggingface.co/api/spaces/{username}/{space_name}"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(space_url, headers=headers)
        if response.status_code == 200:
            print(f"  ✅ Space exists: {username}/{space_name}")
            return True
        elif response.status_code == 404:
            print(f"  ⚠️  Space not found: {username}/{space_name}")
            print(f"  💡 Create it at: https://huggingface.co/new-space")
            return False
        else:
            print(f"  ❌ Error checking space: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def validate_files():
    """Validate that all required files exist"""
    print("\n📁 Validating deployment files...")
    
    required_files = [
        'Dockerfile',
        'requirements.txt', 
        'app_hf.py',
        'space_config.yml'
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            missing.append(file)
            print(f"  ❌ {file}")
    
    if missing:
        print(f"\n🚨 Missing files: {', '.join(missing)}")
        return False
    
    return True

def check_port_config():
    """Check if port configuration is consistent"""
    print("\n🔌 Checking port configuration...")
    
    # Check space_config.yml
    try:
        with open('space_config.yml', 'r') as f:
            content = f.read()
            if 'app_port: 7860' in content:
                print("  ✅ space_config.yml - Port 7860")
            else:
                print("  ⚠️  space_config.yml - Port not 7860")
    except Exception as e:
        print(f"  ❌ space_config.yml error: {e}")
    
    # Check app_hf.py
    try:
        with open('app_hf.py', 'r') as f:
            content = f.read()
            if 'PORT", 7860' in content:
                print("  ✅ app_hf.py - Default port 7860")
            else:
                print("  ⚠️  app_hf.py - Default port not 7860")
    except Exception as e:
        print(f"  ❌ app_hf.py error: {e}")

def test_local_build():
    """Test if Docker build works locally"""
    print("\n🐳 Testing Docker build...")
    
    try:
        # Check if Docker is available
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("  ⚠️  Docker not available - skipping build test")
            return True
        
        print("  🔨 Building Docker image...")
        result = subprocess.run(['docker', 'build', '-t', 'openhands-test', '.'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Docker build successful")
            return True
        else:
            print("  ❌ Docker build failed:")
            print(f"     {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ⚠️  Docker test skipped: {e}")
        return True

def generate_deployment_summary():
    """Generate deployment summary"""
    print("\n📋 Deployment Summary:")
    
    username = os.getenv('HF_USERNAME', 'your-username')
    space_name = os.getenv('HF_SPACE_NAME', 'your-space')
    
    print(f"  🎯 Target: {username}/{space_name}")
    print(f"  🔗 URL: https://{username}-{space_name}.hf.space")
    print(f"  📚 Docs: https://{username}-{space_name}.hf.space/docs")
    print(f"  ❤️  Health: https://{username}-{space_name}.hf.space/health")

def show_next_steps():
    """Show next steps for deployment"""
    print("\n🎯 Next Steps:")
    print("  1. 📤 Push changes to GitHub main branch")
    print("  2. 🤖 GitHub Actions will auto-deploy to HF Spaces")
    print("  3. 📱 Monitor deployment in GitHub Actions tab")
    print("  4. ✅ Test endpoints once deployment completes")
    print("\n📱 Mobile Users:")
    print("  • Use GitHub mobile app to push changes")
    print("  • Monitor deployment in Actions tab")
    print("  • No need to touch HF Spaces interface!")

def main():
    print_banner()
    
    # Run all checks
    checks = [
        ("Environment Variables", check_environment),
        ("HF Connection", test_hf_connection), 
        ("Target Space", check_space_exists),
        ("Required Files", validate_files),
        ("Port Configuration", check_port_config),
        ("Docker Build", test_local_build)
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"  ❌ {name} check failed: {e}")
            all_passed = False
    
    # Generate summary
    generate_deployment_summary()
    
    if all_passed:
        print("\n🎉 All checks passed! Ready to deploy!")
        show_next_steps()
        return 0
    else:
        print("\n🚨 Some checks failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())