#!/usr/bin/env python3
"""
🚨 EMERGENCY FIX for HF Space
Quick fix untuk configuration error
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚨 EMERGENCY FIX for HF Space Configuration Error")
    print("=" * 60)
    
    # Check if HF token is available
    hf_token = os.environ.get('HF_TOKEN')
    if not hf_token:
        print("❌ HF_TOKEN not found in environment")
        print("Please set HF_TOKEN environment variable")
        return
    
    space_name = "Minatoz997/Backend66"
    
    print(f"🎯 Fixing space: {space_name}")
    
    # Install huggingface_hub
    print("📦 Installing huggingface_hub...")
    success, stdout, stderr = run_command("pip install --upgrade huggingface_hub[cli]")
    if not success:
        print(f"❌ Failed to install huggingface_hub: {stderr}")
        return
    
    # Upload only essential files in correct order
    essential_files = [
        "README.md",           # First - contains configuration
        "requirements.txt",    # Second - dependencies
        "Dockerfile",          # Third - container config
        "app.py",             # Last - main application
    ]
    
    print("🔄 Uploading essential files in correct order...")
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"📤 Uploading {file}...")
            cmd = f"huggingface-cli upload {space_name} {file} --repo-type=space"
            success, stdout, stderr = run_command(cmd)
            if success:
                print(f"✅ {file} uploaded successfully")
            else:
                print(f"❌ Failed to upload {file}: {stderr}")
        else:
            print(f"⚠️  {file} not found, skipping...")
    
    print("\n🎉 Emergency fix completed!")
    print(f"🌐 Check your space: https://huggingface.co/spaces/{space_name}")
    print("⏱️  Wait 2-3 minutes for rebuild to complete")

if __name__ == "__main__":
    main()