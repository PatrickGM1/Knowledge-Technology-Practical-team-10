"""
Kitchen domain class for recipe recommendation system.
Represents a user's kitchen environment and available resources.
"""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Kitchen:
    """Represents a kitchen with available equipment and resources"""
    
    available_equipment: List[str] = field(default_factory=list)
    available_utensils: List[str] = field(default_factory=list)
    storage_items: List[str] = field(default_factory=list)
    space_size: str = "medium"  # small, medium, large
    
    def __post_init__(self):
        """Add basic utensils to every kitchen"""
        basic_utensils = ['knife', 'cutting board', 'bowl', 'spoon', 'measuring cups']
        for utensil in basic_utensils:
            if utensil not in self.available_utensils:
                self.available_utensils.append(utensil)
    
    def can_prepare(self, recipe) -> bool:
        """
        Check if kitchen has necessary equipment to prepare recipe.
        
        Args:
            recipe: Recipe object with equipment requirements
            
        Returns:
            True if kitchen can handle the recipe, False otherwise
        """
        if not hasattr(recipe, 'equipment'):
            return True  # If no equipment requirements, assume we can prepare
        
        required_equipment = recipe.equipment
        if not required_equipment:
            return True
        
        # Check each required equipment item
        for equipment in required_equipment:
            equipment_name = equipment.name if hasattr(equipment, 'name') else str(equipment)
            
            # Check if equipment is essential
            is_essential = equipment.is_essential if hasattr(equipment, 'is_essential') else True
            
            if is_essential and not self.has_equipment(equipment_name):
                # Check if there's an acceptable alternative
                if hasattr(equipment, 'alternatives') and equipment.alternatives:
                    has_alternative = any(self.has_equipment(alt) for alt in equipment.alternatives)
                    if not has_alternative:
                        return False
                else:
                    return False
        
        return True
    
    def has_equipment(self, equipment_name: str) -> bool:
        """
        Check if specific equipment is available in kitchen.
        
        Args:
            equipment_name: Name of equipment to check
            
        Returns:
            True if equipment is available, False otherwise
        """
        equipment_lower = equipment_name.lower()
        
        # Check in available_equipment
        for equip in self.available_equipment:
            if equip.lower() in equipment_lower or equipment_lower in equip.lower():
                return True
        
        # Check in available_utensils
        for utensil in self.available_utensils:
            if utensil.lower() in equipment_lower or equipment_lower in utensil.lower():
                return True
        
        return False
    
    def has_utensil(self, utensil_name: str) -> bool:
        """Check if specific utensil is available"""
        utensil_lower = utensil_name.lower()
        return any(u.lower() in utensil_lower or utensil_lower in u.lower() 
                  for u in self.available_utensils)
    
    def add_equipment(self, equipment_name: str):
        """Add equipment to kitchen"""
        if equipment_name not in self.available_equipment:
            self.available_equipment.append(equipment_name)
    
    def add_utensil(self, utensil_name: str):
        """Add utensil to kitchen"""
        if utensil_name not in self.available_utensils:
            self.available_utensils.append(utensil_name)
    
    def get_missing_equipment(self, recipe) -> List[str]:
        """Get list of equipment required by recipe but not available in kitchen"""
        if not hasattr(recipe, 'equipment'):
            return []
        
        missing = []
        for equipment in recipe.equipment:
            equipment_name = equipment.name if hasattr(equipment, 'name') else str(equipment)
            is_essential = equipment.is_essential if hasattr(equipment, 'is_essential') else True
            
            if is_essential and not self.has_equipment(equipment_name):
                missing.append(equipment_name)
        
        return missing
    
    def is_well_equipped(self) -> bool:
        """Check if kitchen is well-equipped (has > 5 equipment items)"""
        return len(self.available_equipment) > 5
    
    def __str__(self) -> str:
        equipment_count = len(self.available_equipment)
        return f"{self.space_size.title()} kitchen with {equipment_count} equipment items"
    
    def __repr__(self) -> str:
        return f"Kitchen(space_size='{self.space_size}', equipment={len(self.available_equipment)})"
