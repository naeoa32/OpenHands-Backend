#!/usr/bin/env python3
"""
Simple HF Spaces deployment script for Human-Like Writing Assistant
"""

import os
import sys
import argparse
from huggingface_hub import HfApi, create_repo
from pathlib import Path

def deploy_to_hf_spaces(space_name: str, hf_token: str = None):
    """Deploy to HF Spaces with essential files only"""
    
    # Get HF token
    if not hf_token:
        hf_token = os.getenv('HF_TOKEN')
    
    if not hf_token:
        print("❌ Error: HF_TOKEN not found in environment variables")
        sys.exit(1)
    
    print(f"🚀 Deploying to HF Spaces: {space_name}")
    
    # Initialize HF API
    api = HfApi(token=hf_token)
    
    # Essential files to deploy
    essential_files = [
        'app.py',
        'requirements.txt', 
        'Dockerfile',
        'README.md',
        'start.sh'
    ]
    
    try:
        # Create or get the space
        try:
            api.create_repo(
                repo_id=space_name,
                repo_type="space",
                space_sdk="docker",
                exist_ok=True
            )
            print(f"✅ Space {space_name} ready")
        except Exception as e:
            print(f"⚠️  Space creation warning: {e}")
    
        # Upload essential files
        for file_path in essential_files:
            if os.path.exists(file_path):
                print(f"📤 Uploading {file_path}...")
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_path,
                    repo_id=space_name,
                    repo_type="space"
                )
                print(f"✅ {file_path} uploaded")
            else:
                print(f"⚠️  {file_path} not found, skipping")
        
        print(f"\n🎉 Deployment successful!")
        print(f"🌐 Space URL: https://huggingface.co/spaces/{space_name}")
        print(f"📊 Logs: https://huggingface.co/spaces/{space_name}?logs=container")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Deploy to HF Spaces')
    parser.add_argument('--space-name', required=True, help='HF Space name (e.g., username/space-name)')
    parser.add_argument('--token', help='HF Token (optional, uses HF_TOKEN env var)')
    
    args = parser.parse_args()
    
    success = deploy_to_hf_spaces(args.space_name, args.token)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()