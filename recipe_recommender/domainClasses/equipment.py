"""
Equipment domain class
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Equipment:
    """Represents kitchen equipment needed for cooking"""
    name: str
    category: Optional[str] = None
    alternatives: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []
