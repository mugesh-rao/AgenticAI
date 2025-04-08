from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """Execute the tool's main functionality."""
        pass

    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate the input parameters."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool's name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool's description."""
        pass 