from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class Parameter:
    name: str
    description: str
    required: bool
    type: str

@dataclass
class ToolConfig:
    name: str
    description: str
    parameters: List[Parameter]
    expected_response_format: str
    callable_function: Callable

    def get_tool_info(self) -> Dict[str, Any]:
        """Format tool information into a JSON-readable format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [
                {
                    "name": param.name,
                    "description": param.description,
                    "required": param.required,
                    "type": param.type
                }
                for param in self.parameters
            ],
            "expected_response_format": self.expected_response_format
        }

    def run_tool(self, params: Dict[str, Any]) -> Any:
        """Execute the tool with given parameters."""
        # Validate required parameters
        for param in self.parameters:
            if param.required and param.name not in params:
                raise ValueError(f"Missing required parameter: {param.name}")
        
        return self.callable_function(**params) 