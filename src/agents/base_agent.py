from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple
from ..tools.tool_config import ToolConfig

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, background: str, tools: List[ToolConfig]):
        self.name = name
        self.background = background
        self.tools = tools

    @abstractmethod
    def process_instruction(self, instruction: str) -> Tuple[str, Dict[str, Any]]:
        """Process an instruction and return result with context."""
        pass

    @abstractmethod
    def can_handle(self, instruction: str) -> bool:
        """Determine if this agent can handle the given instruction."""
        pass

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get information about available tools."""
        return [tool.get_tool_info() for tool in self.tools] 