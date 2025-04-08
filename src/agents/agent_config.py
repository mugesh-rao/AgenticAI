from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from ..tools.tool_config import ToolConfig
import openai

@dataclass
class AgentConfig:
    name: str
    background: str
    tools: List[ToolConfig]
    expected_output: str
    model: str = "gpt-3.5-turbo"  # Default model

    def get_agent_info(self) -> Dict[str, Any]:
        """Format agent information into a JSON-readable format."""
        return {
            "name": self.name,
            "background": self.background,
            "tools": [tool.get_tool_info() for tool in self.tools],
            "expected_output": self.expected_output
        }

    def run_agent(self, instruction: str) -> tuple[str, Dict[str, Any]]:
        """Execute the agent with the given instruction."""
        # Construct the prompt for the agent
        system_prompt = self._build_system_prompt()
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": instruction}
                ]
            )
            
            # Parse the response and determine action
            result = self._parse_agent_response(response.choices[0].message.content)
            return result
        except Exception as e:
            return f"Error executing agent {self.name}: {str(e)}", {}

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent."""
        tools_info = "\n".join([
            f"Tool: {tool.name}\nDescription: {tool.description}\n"
            for tool in self.tools
        ])
        
        return f"""You are an AI agent named {self.name} with the following background:
{self.background}

Available tools:
{tools_info}

Expected output format:
{self.expected_output}

Respond in JSON format with either:
1. {{"action": "use_tool", "tool": "tool_name", "parameters": {{...}}}}
2. {{"action": "final_result", "result": "your result"}}
3. {{"action": "error", "message": "error message"}}"""

    def _parse_agent_response(self, response: str) -> tuple[str, Dict[str, Any]]:
        """Parse the agent's response and execute appropriate action."""
        try:
            import json
            parsed = json.loads(response)
            
            if parsed["action"] == "use_tool":
                tool_name = parsed["tool"]
                tool = next((t for t in self.tools if t.name == tool_name), None)
                if not tool:
                    return f"Error: Tool {tool_name} not found", {}
                
                result = tool.run_tool(parsed["parameters"])
                return str(result), {"tool_used": tool_name, "result": result}
                
            elif parsed["action"] == "final_result":
                return parsed["result"], {"final_result": parsed["result"]}
                
            else:  # error
                return parsed["message"], {"error": parsed["message"]}
                
        except Exception as e:
            return f"Error parsing agent response: {str(e)}", {"error": str(e)} 