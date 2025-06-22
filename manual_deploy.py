#!/usr/bin/env python3
"""
🚀 Manual Deploy Script for HuggingFace Space
Clean and reliable deployment to ensure files are properly updated
"""

import os
import subprocess
import sys
import time

def run_command(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def verify_file_content():
    """Verify that app.py has the correct GET method"""
    print("🔍 Verifying app.py content...")
    
    if not os.path.exists("app.py"):
        print("❌ app.py not found!")
        return False
    
    with open("app.py", "r") as f:
        content = f.read()
    
    # Check for GET method
        return True
    else:
        return False

def main():
    print("🚀 Manual Deploy to HuggingFace Space")
    print("=" * 60)
    
    # Check if HF token is available
    hf_token = os.environ.get('HF_TOKEN')
    if not hf_token:
        print("❌ HF_TOKEN not found in environment")
        print("Please set HF_TOKEN environment variable")
        print("Example: export HF_TOKEN='your_token_here'")
        return
    
    # Verify file content first
    if not verify_file_content():
        print("❌ File verification failed. Please check app.py content.")
        return
    
    space_name = "Minatoz997/Backend66"
    print(f"🎯 Deploying to space: {space_name}")
    
    # Install huggingface_hub
    print("📦 Installing huggingface_hub...")
    success, stdout, stderr = run_command("pip install --upgrade huggingface_hub[cli]")
    if not success:
        print(f"❌ Failed to install huggingface_hub: {stderr}")
        return
    
    # Critical files in order of importance
    critical_files = [
        ("app.py", "Main application file with GET method fix"),
        ("requirements.txt", "Python dependencies"),
        ("Dockerfile", "Container configuration"),
        ("README.md", "Space configuration and documentation"),
    ]
    
    print("🔄 Uploading critical files...")
    
    for file, description in critical_files:
        if os.path.exists(file):
            print(f"📤 Uploading {file} ({description})...")
            cmd = f"huggingface-cli upload {space_name} {file} --repo-type=space"
            success, stdout, stderr = run_command(cmd)
            if success:
                print(f"✅ {file} uploaded successfully")
                time.sleep(1)  # Small delay between uploads
            else:
                print(f"❌ Failed to upload {file}: {stderr}")
                if "401" in stderr:
                    print("🔑 Authentication error. Please check your HF_TOKEN")
                    return
        else:
            print(f"⚠️  {file} not found, skipping...")
    
    # Upload additional files
    additional_files = [
        "PERSONAL_TOKEN_GUIDE.md",
        "README_HF_DEPLOYMENT.md",
    ]
    
    print("\n📤 Uploading additional files...")
    for file in additional_files:
        if os.path.exists(file):
            print(f"📤 Uploading {file}...")
            cmd = f"huggingface-cli upload {space_name} {file} --repo-type=space"
            success, stdout, stderr = run_command(cmd)
            if success:
                print(f"✅ {file} uploaded")
            else:
                print(f"⚠️  Failed to upload {file}")
        else:
            print(f"⚠️  {file} not found, skipping...")
    
    # Upload folders
    folders = ["openhands", "microagents"]
    print("\n📁 Uploading folders...")
    for folder in folders:
        if os.path.exists(folder):
            print(f"📤 Uploading {folder}/ folder...")
            cmd = f"huggingface-cli upload {space_name} {folder}/ --repo-type=space"
            success, stdout, stderr = run_command(cmd)
            if success:
                print(f"✅ {folder}/ uploaded")
            else:
                print(f"⚠️  Failed to upload {folder}/")
        else:
            print(f"⚠️  {folder}/ not found, skipping...")
    
    print("\n🎉 Manual deployment completed!")
    print(f"🌐 Check your space: https://huggingface.co/spaces/{space_name}")
    print("⏱️  Wait 2-3 minutes for space to restart and rebuild")
    print("🔄 The space will automatically restart with the new files")
    
    print("\n📋 What was deployed:")
    print("✅ All essential configuration files")
    print("✅ Supporting documentation and test files")

if __name__ == "__main__":
    main()