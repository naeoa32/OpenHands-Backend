#!/usr/bin/env python3
"""
🚀 AUTO DEPLOY TO HUGGING FACE SPACES
Script untuk menghapus semua file lama dan upload file baru yang bersih

Usage:
python deploy_to_hf.py --space-name your-space-name --hf-token your-token
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
import tempfile
import time

# Files yang akan di-upload ke HF Spaces
ESSENTIAL_FILES = [
    'app.py',
    'requirements.txt', 
    'Dockerfile',
    'README.md',
    'PERSONAL_TOKEN_GUIDE.md',
    'README_HF_DEPLOYMENT.md',
    '.env.example',
    '.gitignore'
]

ESSENTIAL_FOLDERS = [
    'openhands/',
    'microagents/'
]

def run_command(cmd, cwd=None):
    """Run shell command and return result"""
    print(f"🔧 Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False, result.stderr
        print(f"✅ Success: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    # Check git
    success, _ = run_command("git --version")
    if not success:
        print("❌ Git not found. Please install git first.")
        return False
    
    # Check huggingface_hub
    try:
        import huggingface_hub
        print("✅ huggingface_hub found")
    except ImportError:
        print("❌ huggingface_hub not found. Installing...")
        success, _ = run_command("pip install huggingface_hub")
        if not success:
            return False
    
    return True

def clone_hf_space(space_name, hf_token, temp_dir):
    """Clone HF Space repository"""
    print(f"📥 Cloning HF Space: {space_name}")
    
    space_url = f"https://huggingface.co/spaces/{space_name}"
    clone_url = f"https://oauth:{hf_token}@huggingface.co/spaces/{space_name}"
    
    success, _ = run_command(f"git clone {clone_url} hf_space", cwd=temp_dir)
    if not success:
        print(f"❌ Failed to clone {space_url}")
        print("💡 Make sure:")
        print("   - Space exists and you have access")
        print("   - HF token has write permissions")
        print("   - Space name format: username/space-name")
        return False
    
    return True

def clean_hf_space(hf_space_dir):
    """Remove all files except .git"""
    print("🧹 Cleaning HF Space (removing all files except .git)...")
    
    for item in os.listdir(hf_space_dir):
        if item == '.git':
            continue
        
        item_path = os.path.join(hf_space_dir, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"🗑️  Removed directory: {item}")
            else:
                os.remove(item_path)
                print(f"🗑️  Removed file: {item}")
        except Exception as e:
            print(f"⚠️  Could not remove {item}: {e}")

def copy_essential_files(source_dir, hf_space_dir):
    """Copy essential files to HF Space"""
    print("📋 Copying essential files...")
    
    # Copy files
    for file_name in ESSENTIAL_FILES:
        source_file = os.path.join(source_dir, file_name)
        if os.path.exists(source_file):
            dest_file = os.path.join(hf_space_dir, file_name)
            shutil.copy2(source_file, dest_file)
            print(f"✅ Copied: {file_name}")
        else:
            print(f"⚠️  File not found: {file_name}")
    
    # Copy folders
    for folder_name in ESSENTIAL_FOLDERS:
        source_folder = os.path.join(source_dir, folder_name.rstrip('/'))
        if os.path.exists(source_folder):
            dest_folder = os.path.join(hf_space_dir, folder_name.rstrip('/'))
            if os.path.exists(dest_folder):
                shutil.rmtree(dest_folder)
            shutil.copytree(source_folder, dest_folder)
            print(f"✅ Copied folder: {folder_name}")
        else:
            print(f"⚠️  Folder not found: {folder_name}")

def create_hf_space_config(hf_space_dir):
    """Create HF Spaces configuration"""
    print("⚙️  Creating HF Spaces configuration...")
    
    # Create README.md header for HF Spaces
    readme_path = os.path.join(hf_space_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add HF Spaces header if not present
        if not content.startswith('---'):
            hf_header = """---
title: Personal OpenHands Backend
emoji: 💕
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

"""
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(hf_header + content)
            print("✅ Added HF Spaces header to README.md")

def commit_and_push(hf_space_dir, space_name):
    """Commit and push changes to HF Space"""
    print("📤 Committing and pushing changes...")
    
    # Configure git
    run_command("git config user.name 'OpenHands Deploy Bot'", cwd=hf_space_dir)
    run_command("git config user.email 'deploy@openhands.dev'", cwd=hf_space_dir)
    
    # Add all files
    success, _ = run_command("git add -A", cwd=hf_space_dir)
    if not success:
        return False
    
    # Check if there are changes
    success, output = run_command("git status --porcelain", cwd=hf_space_dir)
    if not output.strip():
        print("ℹ️  No changes to commit")
        return True
    
    # Commit
    commit_msg = "🚀 CLEAN DEPLOY: Remove duplicates, deploy essential files only\n\n✅ Files deployed:\n- app.py (all-in-one backend)\n- requirements.txt (minimal deps)\n- Dockerfile (HF optimized)\n- Complete documentation\n- openhands/ (agents)\n- microagents/ (templates)\n\n🗑️ Removed all duplicate files\n💕 Ready for personal use!"
    
    success, _ = run_command(f'git commit -m "{commit_msg}"', cwd=hf_space_dir)
    if not success:
        return False
    
    # Push
    success, _ = run_command("git push origin main", cwd=hf_space_dir)
    if not success:
        print("❌ Failed to push to HF Space")
        return False
    
    print(f"✅ Successfully deployed to: https://huggingface.co/spaces/{space_name}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Deploy clean OpenHands backend to HF Spaces")
    parser.add_argument("--space-name", required=True, help="HF Space name (username/space-name)")
    parser.add_argument("--hf-token", help="HF token (or set HF_TOKEN env var)")
    parser.add_argument("--source-dir", default=".", help="Source directory (default: current)")
    
    args = parser.parse_args()
    
    # Get HF token
    hf_token = args.hf_token or os.getenv("HF_TOKEN")
    if not hf_token:
        print("❌ HF token required. Use --hf-token or set HF_TOKEN env var")
        print("💡 Get token from: https://huggingface.co/settings/tokens")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Get absolute paths
    source_dir = os.path.abspath(args.source_dir)
    if not os.path.exists(source_dir):
        print(f"❌ Source directory not found: {source_dir}")
        return 1
    
    print("🚀 Starting HF Spaces deployment...")
    print(f"📁 Source: {source_dir}")
    print(f"🌐 Target: {args.space_name}")
    print("=" * 60)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📂 Using temp directory: {temp_dir}")
        
        # Clone HF Space
        if not clone_hf_space(args.space_name, hf_token, temp_dir):
            return 1
        
        hf_space_dir = os.path.join(temp_dir, "hf_space")
        
        # Clean HF Space
        clean_hf_space(hf_space_dir)
        
        # Copy essential files
        copy_essential_files(source_dir, hf_space_dir)
        
        # Create HF configuration
        create_hf_space_config(hf_space_dir)
        
        # Commit and push
        if not commit_and_push(hf_space_dir, args.space_name):
            return 1
    
    print("=" * 60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print(f"🌐 Your space: https://huggingface.co/spaces/{args.space_name}")
    print("⏱️  Build will start automatically (5-10 minutes)")
    print("🔧 Don't forget to set environment variables:")
    print("   - LLM_API_KEY=your_openrouter_key")
    print("   - PERSONAL_ACCESS_TOKEN=your_password")
    print("💕 Enjoy your personal AI backend!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())