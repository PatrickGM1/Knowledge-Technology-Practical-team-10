"""
Cooking method model for recipe recommendation system.
Represents different cooking techniques and their properties.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class CookingMethod:
    """Represents a cooking method or technique"""
    
    name: str
    category: str = "dry-heat"
    required_equipment: List[str] = field(default_factory=list)
    skill_level: str = "beginner"
    temperature_range: Optional[tuple] = None  # (min, max) in Celsius
    typical_duration: Optional[int] = None  # in minutes
    alternatives: Dict[str, str] = field(default_factory=dict)  # {method_name: notes}
    health_impact: str = "moderate"
    description: str = ""
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"{self.name} ({self.category})"
    
    def requires_equipment(self, equipment: str) -> bool:
        """Check if method requires specific equipment."""
        return equipment.lower() in [e.lower() for e in self.required_equipment]
    
    def has_alternative(self, method_name: str) -> bool:
        """Check if a specific alternative method exists."""
        return method_name.lower() in [m.lower() for m in self.alternatives.keys()]
    
    def get_alternatives(self) -> List[str]:
        """Get list of alternative cooking methods."""
        return list(self.alternatives.keys())
    
    def is_suitable_for_skill(self, user_skill: str) -> bool:
        """Check if method is suitable for user's skill level."""
        skill_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        method_level = skill_levels.get(self.skill_level.lower(), 1)
        user_level = skill_levels.get(user_skill.lower(), 1)
        return user_level >= method_level


# Common cooking method categories
COOKING_METHOD_CATEGORIES = {
    'dry-heat': ['baking', 'roasting', 'grilling', 'broiling', 'sautéing', 'pan-frying', 'deep-frying', 'stir-frying'],
    'moist-heat': ['boiling', 'simmering', 'poaching', 'steaming', 'braising', 'stewing'],
    'combination': ['braising', 'stewing', 'pot-roasting'],
    'other': ['microwaving', 'sous-vide', 'smoking', 'fermenting', 'pickling']
}

# Predefined common cooking methods
COMMON_COOKING_METHODS = {
    'baking': CookingMethod(
        name='baking',
        category='dry-heat',
        required_equipment=['oven', 'baking sheet'],
        skill_level='beginner',
        temperature_range=(150, 230),
        typical_duration=30,
        alternatives={'roasting': 'Similar but typically at higher temperature'},
        health_impact='healthy',
        description='Cooking food in an oven using dry heat'
    ),
    'sautéing': CookingMethod(
        name='sautéing',
        category='dry-heat',
        required_equipment=['pan', 'stove'],
        skill_level='beginner',
        temperature_range=(120, 180),
        typical_duration=10,
        alternatives={'stir-frying': 'Higher heat, constant stirring', 'pan-frying': 'More oil, less movement'},
        health_impact='healthy',
        description='Cooking quickly in a small amount of fat over high heat'
    ),
    'boiling': CookingMethod(
        name='boiling',
        category='moist-heat',
        required_equipment=['pot', 'stove'],
        skill_level='beginner',
        temperature_range=(100, 100),
        typical_duration=15,
        alternatives={'simmering': 'Lower temperature, gentler cooking', 'steaming': 'Healthier, preserves nutrients'},
        health_impact='healthy',
        description='Cooking in boiling water at 100°C'
    ),
    'grilling': CookingMethod(
        name='grilling',
        category='dry-heat',
        required_equipment=['grill'],
        skill_level='intermediate',
        temperature_range=(200, 260),
        typical_duration=20,
        alternatives={'broiling': 'Indoor alternative, heat from above', 'pan-grilling': 'Using a grill pan on stove'},
        health_impact='healthy',
        description='Cooking over direct heat source'
    ),
    'roasting': CookingMethod(
        name='roasting',
        category='dry-heat',
        required_equipment=['oven', 'roasting pan'],
        skill_level='beginner',
        temperature_range=(175, 260),
        typical_duration=60,
        alternatives={'baking': 'Similar, often used for specific foods'},
        health_impact='healthy',
        description='Cooking with dry heat in an oven, typically for larger items'
    ),
    'steaming': CookingMethod(
        name='steaming',
        category='moist-heat',
        required_equipment=['steamer', 'pot'],
        skill_level='beginner',
        temperature_range=(100, 100),
        typical_duration=15,
        alternatives={'boiling': 'Less healthy, nutrients lost in water', 'microwaving': 'Faster but different texture'},
        health_impact='healthy',
        description='Cooking with steam from boiling water'
    ),
    'braising': CookingMethod(
        name='braising',
        category='combination',
        required_equipment=['dutch oven', 'oven'],
        skill_level='intermediate',
        temperature_range=(150, 180),
        typical_duration=120,
        alternatives={'slow cooking': 'Lower temperature, longer time', 'pressure cooking': 'Faster cooking time'},
        health_impact='moderate',
        description='Searing then slow cooking in liquid'
    ),
    'stir-frying': CookingMethod(
        name='stir-frying',
        category='dry-heat',
        required_equipment=['wok', 'stove'],
        skill_level='intermediate',
        temperature_range=(200, 230),
        typical_duration=8,
        alternatives={'sautéing': 'Lower heat, less stirring'},
        health_impact='healthy',
        description='Quick cooking over very high heat with constant stirring'
    )
}
