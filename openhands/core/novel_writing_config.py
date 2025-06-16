"""
Novel Writing Mode Configuration for OpenHands
"""

from dataclasses import dataclass
from typing import Dict, Any
from openhands.core.config.llm_config import LLMConfig

@dataclass
class NovelWritingConfig:
    """Configuration for Novel Writing Mode"""
    
    # Model selection based on budget
    budget_model: str = "openrouter/anthropic/claude-3-haiku-20240307"  # Claude 3.5 Haiku for budget
    premium_model: str = "openrouter/anthropic/claude-3-opus-20240229"  # Claude 3 Opus for premium
    
    # Optimal parameters for creative writing
    temperature: float = 0.8
    max_output_tokens: int = 4000
    top_p: float = 0.9
    
    # OpenRouter specific settings
    openrouter_site_url: str = "https://docs.all-hands.dev/"
    openrouter_app_name: str = "OpenHands-NovelWriting"

def create_novel_writing_llm_config(
    base_config: LLMConfig, 
    is_premium: bool = False,
    api_key: str | None = None
) -> LLMConfig:
    """
    Create an LLM config optimized for novel writing mode.
    
    Args:
        base_config: Base LLM configuration
        is_premium: Whether to use premium model (Claude Opus) or budget model (Claude Haiku)
        api_key: OpenRouter API key
    
    Returns:
        LLMConfig optimized for creative writing
    """
    novel_config = NovelWritingConfig()
    
    # Create a copy of base config
    config_dict = base_config.model_dump()
    
    # Override with novel writing specific settings
    config_dict.update({
        "model": novel_config.premium_model if is_premium else novel_config.budget_model,
        "temperature": novel_config.temperature,
        "max_output_tokens": novel_config.max_output_tokens,
        "top_p": novel_config.top_p,
        "openrouter_site_url": novel_config.openrouter_site_url,
        "openrouter_app_name": novel_config.openrouter_app_name,
    })
    
    # Set API key if provided
    if api_key:
        config_dict["api_key"] = api_key
    
    # Ensure we're using OpenRouter
    if not config_dict.get("base_url"):
        config_dict["base_url"] = "https://openrouter.ai/api/v1"
    
    return LLMConfig(**config_dict)

def get_novel_writing_model_info(is_premium: bool = False) -> Dict[str, Any]:
    """
    Get information about the model being used for novel writing.
    
    Args:
        is_premium: Whether using premium model
        
    Returns:
        Dictionary with model information
    """
    novel_config = NovelWritingConfig()
    
    if is_premium:
        return {
            "model": novel_config.premium_model,
            "name": "Claude 3 Opus",
            "provider": "Anthropic via OpenRouter",
            "tier": "Premium",
            "strengths": ["Highest quality creative writing", "Complex reasoning", "Nuanced character development"],
            "cost": "Higher cost per token",
            "recommended_for": ["Professional writing", "Complex narratives", "Literary fiction"]
        }
    else:
        return {
            "model": novel_config.budget_model,
            "name": "Claude 3.5 Haiku",
            "provider": "Anthropic via OpenRouter", 
            "tier": "Budget",
            "strengths": ["Fast responses", "Good creative writing", "Cost effective"],
            "cost": "Lower cost per token",
            "recommended_for": ["Draft writing", "Brainstorming", "Quick feedback"]
        }

def should_use_premium_model(template_used: str | None = None, content_length: int = 0) -> bool:
    """
    Determine whether to use premium model based on template and content complexity.
    
    Args:
        template_used: The template being used
        content_length: Length of the content being processed
        
    Returns:
        Boolean indicating whether to use premium model
    """
    # Use premium model for complex templates
    premium_templates = ["theme-symbolism", "style-voice", "editing-revision"]
    
    # Use premium model for longer content (more than 1000 characters)
    if content_length > 1000:
        return True
        
    # Use premium model for complex templates
    if template_used in premium_templates:
        return True
        
    return False