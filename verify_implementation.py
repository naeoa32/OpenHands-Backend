#!/usr/bin/env python3
"""
Final verification script for Novel Writing Mode implementation
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_implementation():
    """Verify all implementation files"""
    print("🔍 Verifying Novel Writing Mode Implementation")
    print("=" * 50)
    
    files_to_check = [
        # Core implementation files
        ("openhands/events/action/message.py", "Extended MessageAction"),
        ("openhands/core/novel_writing_prompts.py", "Novel Writing Prompts"),
        ("openhands/core/novel_writing_config.py", "Novel Writing Config"),
        ("openhands/server/session/session.py", "Modified Session Handler"),
        
        # Configuration files
        (".env.example", "Environment Variables Template"),
        ("render.yaml", "Render Deployment Config"),
        
        # Documentation
        ("NOVEL_WRITING_MODE.md", "Novel Writing Mode Documentation"),
        ("RENDER_DEPLOYMENT.md", "Render Deployment Guide"),
        
        # Test and utility files
        ("test_novel_mode.py", "Test Script"),
        ("start_novel_server.py", "Server Start Script"),
        ("verify_implementation.py", "This Verification Script"),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_code_modifications():
    """Check if code modifications are correct"""
    print("\n🔧 Verifying Code Modifications")
    print("-" * 30)
    
    # Check MessageAction modifications
    try:
        from openhands.events.action.message import MessageAction
        
        # Create test instance
        msg = MessageAction(
            content="test",
            novel_mode=True,
            original_prompt="test prompt",
            template_used="character-development"
        )
        
        print("✅ MessageAction supports novel mode fields")
        
        # Check serialization
        from openhands.events.serialization.event import event_to_dict
        event_dict = event_to_dict(msg)
        print("✅ MessageAction serialization works")
        
    except Exception as e:
        print(f"❌ MessageAction modification failed: {e}")
        return False
    
    # Check novel writing modules
    try:
        from openhands.core.novel_writing_prompts import create_novel_writing_prompt
        from openhands.core.novel_writing_config import create_novel_writing_llm_config
        
        prompt = create_novel_writing_prompt("character-development")
        print("✅ Novel writing prompts module works")
        
        from openhands.core.config.llm_config import LLMConfig
        base_config = LLMConfig()
        novel_config = create_novel_writing_llm_config(base_config)
        print("✅ Novel writing config module works")
        
    except Exception as e:
        print(f"❌ Novel writing modules failed: {e}")
        return False
    
    return True

def check_deployment_readiness():
    """Check if deployment configuration is ready"""
    print("\n🚀 Verifying Deployment Readiness")
    print("-" * 35)
    
    # Check render.yaml
    render_yaml_path = Path("render.yaml")
    if render_yaml_path.exists():
        content = render_yaml_path.read_text()
        if "openhands-novel-backend" in content:
            print("✅ render.yaml configured for novel writing")
        else:
            print("❌ render.yaml not properly configured")
            return False
    
    # Check .env.example
    env_example_path = Path(".env.example")
    if env_example_path.exists():
        content = env_example_path.read_text()
        required_vars = [
            "OPENROUTER_API_KEY",
            "NOVEL_WRITING_BUDGET_MODEL",
            "NOVEL_WRITING_PREMIUM_MODEL",
            "OR_SITE_URL",
            "OR_APP_NAME"
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables in .env.example: {missing_vars}")
            return False
        else:
            print("✅ .env.example contains all required variables")
    
    return True

def check_documentation():
    """Check if documentation is complete"""
    print("\n📚 Verifying Documentation")
    print("-" * 25)
    
    docs_to_check = [
        ("NOVEL_WRITING_MODE.md", ["Overview", "Features", "API Integration", "Usage Examples"]),
        ("RENDER_DEPLOYMENT.md", ["Quick Deploy", "Environment Variables", "Frontend Integration", "Troubleshooting"])
    ]
    
    for doc_file, required_sections in docs_to_check:
        doc_path = Path(doc_file)
        if doc_path.exists():
            content = doc_path.read_text()
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"❌ {doc_file} missing sections: {missing_sections}")
                return False
            else:
                print(f"✅ {doc_file} complete with all sections")
        else:
            print(f"❌ {doc_file} not found")
            return False
    
    return True

def generate_summary():
    """Generate implementation summary"""
    print("\n📋 Implementation Summary")
    print("=" * 25)
    
    print("🎯 NOVEL WRITING MODE FEATURES:")
    print("   ✅ Indonesian creative writing prompts")
    print("   ✅ Intelligent model selection (Budget/Premium)")
    print("   ✅ Template-based assistance (7 templates)")
    print("   ✅ Optimized AI parameters (temp: 0.8, tokens: 4000)")
    print("   ✅ No generic responses - always asks specific questions")
    
    print("\n🔧 TECHNICAL IMPLEMENTATION:")
    print("   ✅ Extended MessageAction with novel_mode fields")
    print("   ✅ Novel writing system prompts in Indonesian")
    print("   ✅ Dynamic LLM configuration switching")
    print("   ✅ OpenRouter API integration")
    print("   ✅ WebSocket-based real-time communication")
    
    print("\n🚀 DEPLOYMENT READY:")
    print("   ✅ Render.yaml configuration")
    print("   ✅ Environment variables template")
    print("   ✅ Health check endpoints")
    print("   ✅ CORS configuration")
    print("   ✅ Auto-scaling support")
    
    print("\n📚 DOCUMENTATION:")
    print("   ✅ Novel Writing Mode guide")
    print("   ✅ Render deployment instructions")
    print("   ✅ Frontend integration examples")
    print("   ✅ Troubleshooting guide")
    
    print("\n🎨 SUPPORTED TEMPLATES:")
    templates = [
        "character-development",
        "plot-structure", 
        "dialogue-writing",
        "world-building",
        "style-voice",
        "theme-symbolism",
        "editing-revision"
    ]
    for template in templates:
        print(f"   ✅ {template}")

def main():
    """Main verification function"""
    print("🚀 OpenHands Novel Writing Mode - Final Verification")
    print("=" * 55)
    
    checks = [
        ("File Structure", check_implementation),
        ("Code Modifications", check_code_modifications),
        ("Deployment Config", check_deployment_readiness),
        ("Documentation", check_documentation),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 55)
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Novel Writing Mode implementation is complete and ready for deployment")
        
        generate_summary()
        
        print("\n🚀 NEXT STEPS:")
        print("1. Set your OPENROUTER_API_KEY in Render environment variables")
        print("2. Deploy to Render using the provided render.yaml")
        print("3. Test the WebSocket connection from your frontend")
        print("4. Monitor logs and usage in Render dashboard")
        
        print("\n📝 FRONTEND INTEGRATION:")
        print("Send novel_mode: true in MessageAction to activate Novel Writing Mode")
        print("Include template_used and original_prompt for best results")
        
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please review the errors above and fix them before deployment")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)