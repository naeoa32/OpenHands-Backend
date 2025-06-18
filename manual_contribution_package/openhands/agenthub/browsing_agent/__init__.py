# HF Spaces compatible import with fallback
try:
    from openhands.agenthub.browsing_agent.browsing_agent import BrowsingAgent
    from openhands.controller.agent import Agent
    Agent.register('BrowsingAgent', BrowsingAgent)
    BROWSING_AVAILABLE = True
except ImportError:
    # Fallback when browsergym dependencies are not available
    from openhands.controller.agent import Agent
    
    class BrowsingAgent(Agent):
        """Fallback BrowsingAgent for HF Spaces without browsergym dependencies."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
        async def step(self, state):
            """Fallback step method."""
            from openhands.events.action import MessageAction
            return MessageAction(
                content="BrowsingAgent is not available in this environment. Please use CodeActAgent or other available agents."
            )
    
    Agent.register('BrowsingAgent', BrowsingAgent)
    BROWSING_AVAILABLE = False
