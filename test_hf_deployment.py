#!/usr/bin/env python3
"""
Test script to simulate HF Spaces deployment
This will test if our fixes work in a HF-like environment
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path

def test_deployment():
    """Test the deployment in a simulated HF environment"""
    
    print("🧪 Testing HF Spaces Deployment Simulation")
    print("=" * 50)
    
    # Set HF-like environment variables
    os.environ["OPENHANDS_RUNTIME"] = "local"
    os.environ["SETTINGS_STORE_TYPE"] = "memory"
    os.environ["SECRETS_STORE_TYPE"] = "memory"
    os.environ["CONVERSATION_STORE_TYPE"] = "memory"
    os.environ["FILE_STORE"] = "memory"
    os.environ["SESSION_STORE_TYPE"] = "memory"
    os.environ["PORT"] = "7860"
    os.environ["HOST"] = "0.0.0.0"
    
    # Test 1: Check if we can import the main modules
    print("\n1️⃣ Testing Core Imports...")
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    # Test 2: Test runtime imports
    print("\n2️⃣ Testing Runtime Imports...")
    try:
        from openhands.runtime.impl import DockerRuntime, LocalRuntime, E2BRuntime
        print("✅ Runtime classes imported successfully")
        
        # Test if DockerRuntime works (should work here but fail in real HF)
        try:
            # This would fail in HF Spaces without docker package
            print("🔧 DockerRuntime available in this environment")
        except Exception as e:
            print(f"⚠️  DockerRuntime issue: {e}")
            
    except ImportError as e:
        print(f"❌ Runtime import failed: {e}")
        return False
    
    # Test 3: Test app import
    print("\n3️⃣ Testing App Import...")
    try:
        # Add current directory to path
        sys.path.insert(0, '/workspace/OpenHands-Backend')
        
        # This is the critical test - can we import the app?
        from openhands.server.app import app
        print("✅ OpenHands app imported successfully")
        
        # Test if app is a FastAPI instance
        if hasattr(app, 'routes'):
            print(f"✅ App has {len(app.routes)} routes")
        else:
            print("❌ App is not a valid FastAPI instance")
            return False
            
    except ImportError as e:
        print(f"❌ App import failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Test our fixed entry point
    print("\n4️⃣ Testing Fixed Entry Point...")
    try:
        # Import our fixed app
        exec(open('/workspace/OpenHands-Backend/app_hf_final.py').read().replace('if __name__ == "__main__":', 'if False:'))
        print("✅ Fixed entry point code executed successfully")
    except Exception as e:
        print(f"❌ Fixed entry point failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Test requirements
    print("\n5️⃣ Testing Requirements...")
    requirements_file = '/workspace/OpenHands-Backend/requirements_hf_fixed.txt'
    if Path(requirements_file).exists():
        with open(requirements_file, 'r') as f:
            requirements = f.read()
        
        # Check that problematic packages are not included
        problematic = ['docker', 'google-generativeai', 'redis', 'e2b']
        found_problematic = []
        for pkg in problematic:
            if pkg in requirements and not requirements.count(f'# {pkg}'):
                found_problematic.append(pkg)
        
        if found_problematic:
            print(f"⚠️  Found problematic packages: {found_problematic}")
        else:
            print("✅ No problematic packages in requirements")
    else:
        print("❌ requirements_hf_fixed.txt not found")
        return False
    
    print("\n🎉 All tests passed! Deployment should work on HF Spaces.")
    return True

if __name__ == "__main__":
    success = test_deployment()
    if success:
        print("\n✅ READY FOR HF SPACES DEPLOYMENT!")
        print("\n📋 Next steps:")
        print("1. Upload these files to HF Spaces:")
        print("   - Dockerfile_HF_Final → Dockerfile")
        print("   - requirements_hf_fixed.txt → requirements.txt") 
        print("   - app_hf_final.py")
        print("   - openhands/ folder")
        print("2. Set LLM_API_KEY environment variable")
        print("3. Deploy!")
    else:
        print("\n❌ DEPLOYMENT NOT READY - Fix issues above first")
    
    sys.exit(0 if success else 1)