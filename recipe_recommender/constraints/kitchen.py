"""
Kitchen model for recipe recommendation system
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Kitchen:
    """Represents a kitchen with available equipment and resources"""
    
    available_equipment: List[str] = field(default_factory=list)
    available_utensils: List[str] = field(default_factory=list)
    storage_items: List[str] = field(default_factory=list)
    space_size: str = "medium"
    
    def __post_init__(self):
        basic_utensils = ['knife', 'cutting board', 'bowl', 'spoon', 'measuring cups']
        for utensil in basic_utensils:
            if utensil not in self.available_utensils:
                self.available_utensils.append(utensil)
    
    def can_prepare(self, recipe) -> bool:
        if not hasattr(recipe, 'equipment'):
            return True
        
        required_equipment = recipe.equipment
        if not required_equipment:
            return True
        
        for equipment in required_equipment:
            equipment_name = equipment.name if hasattr(equipment, 'name') else str(equipment)
            is_essential = equipment.is_essential if hasattr(equipment, 'is_essential') else True
            
            if is_essential and not self.has_equipment(equipment_name):
                if hasattr(equipment, 'alternatives') and equipment.alternatives:
                    has_alternative = any(self.has_equipment(alt) for alt in equipment.alternatives)
                    if not has_alternative:
                        return False
                else:
                    return False
        
        return True
    
    def has_equipment(self, equipment_name: str) -> bool:
        equipment_lower = equipment_name.lower()
        
        for equip in self.available_equipment:
            if equip.lower() in equipment_lower or equipment_lower in equip.lower():
                return True
        
        for utensil in self.available_utensils:
            if utensil.lower() in equipment_lower or equipment_lower in utensil.lower():
                return True
        
        return False
    
    def has_utensil(self, utensil_name: str) -> bool:
        utensil_lower = utensil_name.lower()
        return any(u.lower() in utensil_lower or utensil_lower in u.lower() 
                  for u in self.available_utensils)
    
    def add_equipment(self, equipment_name: str):
        if equipment_name not in self.available_equipment:
            self.available_equipment.append(equipment_name)
    
    def add_utensil(self, utensil_name: str):
        if utensil_name not in self.available_utensils:
            self.available_utensils.append(utensil_name)
