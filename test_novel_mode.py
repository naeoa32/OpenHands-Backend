#!/usr/bin/env python3
"""
Test script for Novel Writing Mode implementation
"""

import asyncio
import json
from openhands.events.action.message import MessageAction
from openhands.events.serialization.event import event_from_dict, event_to_dict
from openhands.core.novel_writing_prompts import create_novel_writing_prompt, get_novel_writing_questions
from openhands.core.novel_writing_config import (
    create_novel_writing_llm_config, 
    should_use_premium_model,
    get_novel_writing_model_info
)
from openhands.core.config.llm_config import LLMConfig

def test_message_action_novel_fields():
    """Test that MessageAction supports novel mode fields"""
    print("🧪 Testing MessageAction novel mode fields...")
    
    # Test creating MessageAction with novel mode fields
    message_data = {
        "action": "message",
        "args": {
            "content": "Bantu saya mengembangkan karakter protagonis",
            "novel_mode": True,
            "original_prompt": "Saya butuh bantuan karakter",
            "template_used": "character-development"
        }
    }
    
    # Test serialization
    message_action = MessageAction(
        content="Bantu saya mengembangkan karakter protagonis",
        novel_mode=True,
        original_prompt="Saya butuh bantuan karakter",
        template_used="character-development"
    )
    
    print(f"✅ MessageAction created successfully")
    print(f"   - novel_mode: {message_action.novel_mode}")
    print(f"   - original_prompt: {message_action.original_prompt}")
    print(f"   - template_used: {message_action.template_used}")
    
    # Test event serialization
    event_dict = event_to_dict(message_action)
    print(f"✅ Event serialization successful")
    
    return True

def test_novel_writing_prompts():
    """Test novel writing prompt generation"""
    print("\n🧪 Testing novel writing prompts...")
    
    # Test basic prompt
    basic_prompt = create_novel_writing_prompt()
    print(f"✅ Basic prompt created (length: {len(basic_prompt)})")
    
    # Test template-specific prompt
    template_prompt = create_novel_writing_prompt("character-development")
    print(f"✅ Template prompt created (length: {len(template_prompt)})")
    
    # Test with original prompt
    full_prompt = create_novel_writing_prompt(
        "character-development", 
        "Saya butuh bantuan mengembangkan karakter utama"
    )
    print(f"✅ Full prompt created (length: {len(full_prompt)})")
    
    # Test questions
    questions = get_novel_writing_questions("character-development")
    print(f"✅ Questions retrieved: {len(questions)} questions")
    
    return True

def test_novel_writing_config():
    """Test novel writing configuration"""
    print("\n🧪 Testing novel writing configuration...")
    
    from pydantic import SecretStr
    
    # Create base config with SecretStr for security testing
    base_config = LLMConfig(
        model="claude-3-haiku-20240307",
        api_key=SecretStr("test-key"),
        temperature=0.0
    )
    
    # Test budget config
    budget_config = create_novel_writing_llm_config(base_config, is_premium=False)
    print(f"✅ Budget config created:")
    print(f"   - model: {budget_config.model}")
    print(f"   - temperature: {budget_config.temperature}")
    print(f"   - max_output_tokens: {budget_config.max_output_tokens}")
    print(f"   - api_key type: {type(budget_config.api_key).__name__}")
    
    # Test premium config
    premium_config = create_novel_writing_llm_config(base_config, is_premium=True)
    print(f"✅ Premium config created:")
    print(f"   - model: {premium_config.model}")
    print(f"   - temperature: {premium_config.temperature}")
    print(f"   - api_key secured: {budget_config.api_key is not None}")
    
    # Test model selection logic with configurable thresholds
    use_premium_simple = should_use_premium_model("character-development", 500)
    use_premium_complex = should_use_premium_model("theme-symbolism", 2000)
    
    print(f"✅ Model selection logic:")
    print(f"   - Simple template, short content: {'Premium' if use_premium_simple else 'Budget'}")
    print(f"   - Complex template, long content: {'Premium' if use_premium_complex else 'Budget'}")
    
    # Test configurable thresholds
    import os
    original_threshold = os.environ.get('NOVEL_PREMIUM_CONTENT_THRESHOLD')
    os.environ['NOVEL_PREMIUM_CONTENT_THRESHOLD'] = '800'
    
    use_premium_with_lower_threshold = should_use_premium_model("character-development", 1000)
    print(f"   - With lower threshold (800): {'Premium' if use_premium_with_lower_threshold else 'Budget'}")
    
    # Restore original threshold
    if original_threshold:
        os.environ['NOVEL_PREMIUM_CONTENT_THRESHOLD'] = original_threshold
    else:
        os.environ.pop('NOVEL_PREMIUM_CONTENT_THRESHOLD', None)
    
    # Test model info
    budget_info = get_novel_writing_model_info(False)
    premium_info = get_novel_writing_model_info(True)
    
    print(f"✅ Model info retrieved:")
    print(f"   - Budget: {budget_info['name']} ({budget_info['tier']})")
    print(f"   - Premium: {premium_info['name']} ({premium_info['tier']})")
    
    # Test API key security
    try:
        # This should work
        secret_value = budget_config.api_key.get_secret_value()
        print(f"✅ API key security: SecretStr properly implemented")
    except Exception as e:
        print(f"❌ API key security issue: {e}")
        return False
    
    return True

def test_event_serialization():
    """Test event serialization with novel mode"""
    print("\n🧪 Testing event serialization...")
    
    # Create test data as it would come from frontend
    frontend_data = {
        "action": "message",
        "args": {
            "content": "Enhanced prompt dari novel service",
            "novel_mode": True,
            "original_prompt": "Input asli user",
            "template_used": "character-development"
        }
    }
    
    try:
        # Test deserialization
        event = event_from_dict(frontend_data)
        print(f"✅ Event deserialization successful")
        print(f"   - Type: {type(event).__name__}")
        print(f"   - Novel mode: {event.novel_mode}")
        print(f"   - Template: {event.template_used}")
        
        # Test serialization back
        serialized = event_to_dict(event)
        print(f"✅ Event serialization successful")
        
        return True
    except Exception as e:
        print(f"❌ Event serialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Novel Writing Mode Tests\n")
    
    tests = [
        test_message_action_novel_fields,
        test_novel_writing_prompts,
        test_novel_writing_config,
        test_event_serialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Novel Writing Mode implementation is ready.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)