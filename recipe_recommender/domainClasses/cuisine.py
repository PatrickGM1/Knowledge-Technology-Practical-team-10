"""
Cuisine Domain Class
Represents a type of cooking tradition or regional style
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Cuisine:
    """Represents a cuisine type"""
    
    name: str
    region: str = ""
    description: str = ""
    
    common_ingredients: List[str] = field(default_factory=list)
    common_techniques: List[str] = field(default_factory=list)
    flavor_profile: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return self.name
    
    def is_similar_to(self, other_cuisine: str) -> bool:
        similar_groups = {
            'italian': ['mediterranean', 'greek'],
            'french': ['mediterranean', 'european'],
            'chinese': ['asian', 'thai', 'vietnamese'],
            'japanese': ['asian', 'korean'],
            'mexican': ['latin american', 'tex-mex'],
            'indian': ['south asian', 'pakistani']
        }
        
        cuisine_lower = self.name.lower()
        other_lower = other_cuisine.lower()
        
        if cuisine_lower in similar_groups:
            return other_lower in similar_groups[cuisine_lower]
        
        return False


COMMON_CUISINES = [
    "French",
    "Italian",
    "Asian",
    "Mediterranean"
]
