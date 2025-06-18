# HF Spaces compatible import with fallback
try:
    from openhands.agenthub.visualbrowsing_agent.visualbrowsing_agent import (
        VisualBrowsingAgent,
    )
    from openhands.controller.agent import Agent
    Agent.register('VisualBrowsingAgent', VisualBrowsingAgent)
    VISUAL_BROWSING_AVAILABLE = True
except ImportError:
    # Fallback when browsergym dependencies are not available
    from openhands.controller.agent import Agent
    
    class VisualBrowsingAgent(Agent):
        """Fallback VisualBrowsingAgent for HF Spaces without browsergym dependencies."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        async def step(self, state):
            """Fallback step method."""
            from openhands.events.action import MessageAction
            return MessageAction(
                content="VisualBrowsingAgent is not available in this environment. Please use CodeActAgent or other available agents."
            )
    
    Agent.register('VisualBrowsingAgent', VisualBrowsingAgent)
    VISUAL_BROWSING_AVAILABLE = False
