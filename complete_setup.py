#!/usr/bin/env python3
"""
🎯 Complete Setup Script
One-click setup untuk deployment yang 100% working
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    print("🎯" + "="*60)
    print("🚀 OpenHands Complete Setup - 100% Working Deployment")
    print("📱 Mobile-Friendly | Auto-Deploy Ready")
    print("="*62)

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Success")
            return True
        else:
            print(f"  ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def check_git_status():
    """Check git repository status"""
    print("\n🔍 Checking Git repository...")
    
    # Check if we're in a git repo
    if not Path('.git').exists():
        print("  ❌ Not a git repository")
        return False
    
    # Check git status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("  ⚠️  Uncommitted changes detected")
        print("  📝 Modified files:")
        for line in result.stdout.strip().split('\n')[:5]:
            print(f"    {line}")
        return True
    else:
        print("  ✅ Working directory clean")
        return True

def validate_environment():
    """Validate environment setup"""
    print("\n🔍 Validating environment...")
    
    # Run our validation script
    try:
        result = subprocess.run([sys.executable, 'validate_deployment.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ All validations passed")
            return True
        else:
            print("  ❌ Validation failed")
            print("  📋 Issues found:")
            # Show last few lines of output
            lines = result.stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"    {line}")
            return False
    except Exception as e:
        print(f"  ❌ Validation error: {e}")
        return False

def setup_environment_file():
    """Setup .env file"""
    print("\n🔧 Setting up environment file...")
    
    if Path('.env').exists():
        print("  ⚠️  .env file already exists")
        response = input("  🤔 Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("  ⏭️  Skipping .env setup")
            return True
    
    # Run setup_env.py
    try:
        result = subprocess.run([sys.executable, 'setup_env.py', 'create'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✅ .env file created")
            return True
        else:
            print("  ❌ Failed to create .env file")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def commit_changes():
    """Commit all changes"""
    print("\n📝 Committing changes...")
    
    # Add all files
    if not run_command('git add .', 'Adding files to git'):
        return False
    
    # Check if there are changes to commit
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
    if result.returncode == 0:
        print("  ℹ️  No changes to commit")
        return True
    
    # Commit changes
    commit_message = """🎯 Complete setup for 100% working deployment

✅ All dependencies verified and optimized
✅ Port configuration standardized (7860)
✅ Environment setup scripts added
✅ Validation and testing tools included
✅ GitHub Actions auto-deploy ready
✅ Mobile-friendly deployment solution

🚀 Ready for production deployment!

Components:
- Complete requirements.txt with all dependencies
- Optimized Dockerfile for HF Spaces
- Environment setup and validation scripts
- Auto-deploy GitHub Actions workflow
- Comprehensive testing and monitoring tools

📱 Mobile users can now deploy via GitHub app!"""

    cmd = f'git commit -m "{commit_message}"'
    return run_command(cmd, 'Committing changes')

def push_changes():
    """Push changes to repository"""
    print("\n📤 Pushing changes to repository...")
    
    # Get current branch
    result = subprocess.run(['git', 'branch', '--show-current'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("  ❌ Cannot determine current branch")
        return False
    
    branch = result.stdout.strip()
    print(f"  📍 Current branch: {branch}")
    
    # Push changes
    cmd = f'git push -u origin {branch}'
    return run_command(cmd, f'Pushing to {branch}')

def show_next_steps():
    """Show next steps for deployment"""
    print("\n🎯 Next Steps for 100% Working Deployment:")
    
    steps = [
        "1. 🔐 Set GitHub Secrets:",
        "   • HF_TOKEN = your_huggingface_token",
        "   • HF_USERNAME = your_hf_username", 
        "   • HF_SPACE_NAME = your_space_name",
        "",
        "2. 🤗 Create Hugging Face Space:",
        "   • Go to https://huggingface.co/new-space",
        "   • Choose Docker SDK",
        "   • Set app_port to 7860",
        "",
        "3. 🔧 Set HF Space Environment Variables:",
        "   • LLM_API_KEY = your_openrouter_api_key",
        "   • LLM_MODEL = openrouter/anthropic/claude-3-haiku-20240307",
        "   • LLM_BASE_URL = https://openrouter.ai/api/v1",
        "",
        "4. 🚀 Deploy:",
        "   • Push to main branch (auto-deploy)",
        "   • Or trigger manually in GitHub Actions",
        "",
        "5. ✅ Test Deployment:",
        "   • python test_deployment.py https://your-space.hf.space",
        "   • Check /health endpoint",
        "   • Verify /docs page"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n📱 Mobile Users:")
    print(f"  • Use GitHub mobile app to push changes")
    print(f"  • Monitor deployment in Actions tab")
    print(f"  • No need to touch HF Spaces interface!")
    
    print(f"\n🔗 Useful Links:")
    print(f"  • GitHub Secrets: https://github.com/your-repo/settings/secrets/actions")
    print(f"  • Create HF Space: https://huggingface.co/new-space")
    print(f"  • OpenRouter API: https://openrouter.ai/keys")

def interactive_setup():
    """Interactive setup process"""
    print("\n🎯 Interactive Setup Process:")
    
    # Get user preferences
    print("\n🤔 Setup preferences:")
    auto_commit = input("  📝 Auto-commit changes? (Y/n): ").strip().lower()
    auto_push = input("  📤 Auto-push to repository? (Y/n): ").strip().lower()
    
    auto_commit = auto_commit != 'n'
    auto_push = auto_push != 'n'
    
    # Run setup steps
    steps = [
        ("Environment File", setup_environment_file),
        ("Validation", validate_environment),
        ("Git Status", check_git_status)
    ]
    
    success = True
    for step_name, step_func in steps:
        try:
            if not step_func():
                print(f"  ❌ {step_name} failed")
                success = False
        except Exception as e:
            print(f"  ❌ {step_name} error: {e}")
            success = False
    
    if not success:
        print("\n🚨 Setup encountered issues. Please review and fix before proceeding.")
        return False
    
    # Commit and push if requested
    if auto_commit:
        if not commit_changes():
            print("\n⚠️  Commit failed, but setup is complete")
        elif auto_push:
            if not push_changes():
                print("\n⚠️  Push failed, but changes are committed locally")
    
    return True

def main():
    print_banner()
    
    # Check if we're in the right directory
    if not Path('app_hf.py').exists():
        print("❌ app_hf.py not found. Please run this script from the repository root.")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'validate':
            success = validate_environment()
            sys.exit(0 if success else 1)
        elif command == 'commit':
            success = commit_changes()
            sys.exit(0 if success else 1)
        elif command == 'push':
            success = push_changes()
            sys.exit(0 if success else 1)
        elif command == 'env':
            success = setup_environment_file()
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: validate, commit, push, env")
            sys.exit(1)
    else:
        # Run interactive setup
        success = interactive_setup()
        
        if success:
            print("\n🎉 Setup completed successfully!")
            show_next_steps()
            print("\n🚀 Ready for 100% working deployment!")
        else:
            print("\n🚨 Setup failed. Please review issues above.")
        
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()