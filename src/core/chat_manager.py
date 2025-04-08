from typing import Dict, List, Optional
from ..agents.agent_config import AgentConfig
from openai import OpenAI
import json

class ChatManager:
    def __init__(self, agents: List[AgentConfig], openai_api_key: str):
        self.agents = agents
        self.message_history = []
        self.client = OpenAI(api_key=openai_api_key)  # NEW client-based SDK

    def handle_input(self, user_message: str) -> str:
        """Handle user input and return a response."""
        self.message_history.append({"role": "user", "content": user_message})
        
        result, context = self.agentic_action(self.message_history)
        response = self._generate_response(result, context)
        self.message_history.append({"role": "assistant", "content": response})
        
        return response

    def agentic_action(self, message_history: List[Dict[str, str]]) -> tuple[str, Dict]:
        """Determine if an agent should be invoked and handle the action."""

        agents_info = "\n".join([
            f"Agent: {agent.name}\nBackground: {agent.background}\n"
            for agent in self.agents
        ])
        
        decision_prompt = f"""Given the following conversation history and available agents, 
determine if any agent should be invoked or if the chatbot should handle the response directly.

Available Agents:
{agents_info}

Respond in JSON format with:
{{"action": "none"}} or
{{"action": "request_info", "message": "..."}} or
{{"action": "delegate", "agent": "agent_name", "instruction": "..."}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": decision_prompt},
                    *message_history
                ]
            )
            decision_text = response.choices[0].message.content
            decision = json.loads(decision_text)

            if decision["action"] == "none":
                return "", {}

            elif decision["action"] == "request_info":
                return decision["message"], {}

            elif decision["action"] == "delegate":
                agent = next((a for a in self.agents if a.name == decision["agent"]), None)
                if not agent:
                    return f"Error: Agent {decision['agent']} not found", {}
                return agent.run_agent(decision["instruction"])

        except Exception as e:
            return f"Error in agentic action: {str(e)}", {"error": str(e)}

    def _generate_response(self, result: str, context: Dict) -> str:
        """Generate a natural language response using the result and context."""
        prompt = f"""As a friendly and informal chatbot assisting the user, generate a response 
considering the following result and context from our AI agents:

Result: {result}
Context: {context}

Respond in a natural, conversational way while incorporating the information provided."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    *self.message_history
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
