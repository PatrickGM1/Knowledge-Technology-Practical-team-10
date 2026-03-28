"""
Rule model for inference engine
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Rule:
    """Represents a single inference rule"""
    
    id: str
    name: str
    description: str = ""
    priority: int = 0
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    action: Dict[str, Any] = field(default_factory=dict)
    category: str = "general"
    fired_count: int = 0
    
    def __repr__(self):
        return f"Rule(id='{self.id}', name='{self.name}', priority={self.priority})"
