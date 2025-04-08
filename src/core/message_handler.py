from typing import Dict, List, Optional, Tuple, Any
from ..agents.agent_config import AgentConfig
from ..utils.llm_utils import create_chat_completion

class MessageHandler:
    """Handles message processing and routing to appropriate agents."""
    
    def __init__(self, agents: List[AgentConfig]):
        self.agents = agents

    def process_message(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]]
    ) -> Tuple[str, Dict[str, Any]]:
        """Process a message and return the appropriate response."""
        
        # First, determine if we need an agent
        agent_decision = self._decide_agent(message, conversation_history)
        
        if agent_decision["needs_agent"]:
            agent = self._get_agent(agent_decision["agent_name"])
            if agent:
                return agent.run_agent(message)
            
        # If no agent is needed or found, return default response
        return self._create_default_response(message), {}

    def _decide_agent(
        self, 
        message: str, 
        history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Decide which agent (if any) should handle the message."""
        
        agents_info = "\n".join([
            f"Agent: {agent.name}\nBackground: {agent.background}"
            for agent in self.agents
        ])
        
        prompt = f"""Given the message and available agents, decide if an agent should handle this request.
Available agents:
{agents_info}

Message: {message}

Respond in JSON format:
{{"needs_agent": boolean, "agent_name": string or null, "reason": string}}"""

        response = create_chat_completion([
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ])
        
        import json
        return json.loads(response)

    def _get_agent(self, agent_name: str) -> Optional[AgentConfig]:
        """Get an agent by name."""
        return next(
            (agent for agent in self.agents if agent.name == agent_name), 
            None
        )

    def _create_default_response(self, message: str) -> str:
        """Create a default response when no agent is needed."""
        return create_chat_completion([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]) 