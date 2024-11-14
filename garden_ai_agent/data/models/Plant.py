from typing import Optional
from sqlalchemy.orm import validates

from ..database import db
from ..fields import GrowthForm, LifeCycle, UseCategory

class Plant(db.Model):
    """
    Represents a plant in a specific garden location.
    
    Contains static reference data about the plant species and variety.
    Dynamic data like growth status and measurements are tracked in the plant_logs table.
    """
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    garden_location_id = db.Column(
        db.Integer,
        db.ForeignKey('garden_locations.id', name='fk_plants_garden_location'),
        nullable=False
    )
    
    # Basic plant information
    name = db.Column(db.String(100), nullable=False)  # Common name
    scientific_name = db.Column(db.String(100), nullable=True)
    variety = db.Column(db.String(100), nullable=True)  # Specific cultivar or variety
    
    # Classification
    _growth_form = db.Column("growth_form", db.Enum(GrowthForm), nullable=False)
    _life_cycle = db.Column("life_cycle", db.Enum(LifeCycle), nullable=False)
    _primary_use = db.Column("primary_use", db.Enum(UseCategory), nullable=False)
    _secondary_use = db.Column("secondary_use", db.Enum(UseCategory), nullable=True)
    
    # Physical characteristics (reference values)
    expected_height_inches = db.Column(db.Integer, nullable=True)
    expected_spread_inches = db.Column(db.Integer, nullable=True)
    
    # Growing requirements
    hardiness_zone_min = db.Column(db.Integer, nullable=True)
    hardiness_zone_max = db.Column(db.Integer, nullable=True)
    preferred_soil_ph_min = db.Column(db.Float, nullable=True)
    preferred_soil_ph_max = db.Column(db.Float, nullable=True)
    
    # Planting reference
    planting_depth_inches = db.Column(db.Float, nullable=True)
    spacing_inches = db.Column(db.Integer, nullable=True)  # Recommended spacing between plants
    
    # Additional information
    description = db.Column(db.Text, nullable=True)  # General description
    care_instructions = db.Column(db.Text, nullable=True)  # Basic care guidelines
    notes = db.Column(db.Text, nullable=True)  # Additional notes

    @validates('name')
    def validate_name(self, key, value: str) -> str:
        """Validates the plant's common name."""
        if not value or not value.strip():
            raise ValueError("Plant name cannot be empty")
        if len(value) > 100:
            raise ValueError("Plant name cannot exceed 100 characters")
        return value.strip()

    @validates('scientific_name')
    def validate_scientific_name(self, key, value: Optional[str]) -> Optional[str]:
        """Validates the plant's scientific name if provided."""
        if value is None:
            return None
        value = value.strip()
        if len(value) > 100:
            raise ValueError("Scientific name cannot exceed 100 characters")
        return value

    @validates('variety')
    def validate_variety(self, key, value: Optional[str]) -> Optional[str]:
        """Validates the plant variety/cultivar if provided."""
        if value is None:
            return None
        value = value.strip()
        if len(value) > 100:
            raise ValueError("Variety name cannot exceed 100 characters")
        return value

    @property
    def growth_form(self) -> GrowthForm:
        return GrowthForm(self._growth_form)

    @growth_form.setter
    def growth_form(self, value: GrowthForm | str) -> None:
        """
        Sets the growth form value, converting strings to GrowthForm enum if needed.
        
        Args:
            value: GrowthForm enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any GrowthForm enum
            TypeError: If value is neither string nor GrowthForm enum
        """
        if isinstance(value, str):
            try:
                value = GrowthForm[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid growth form value: {value}")
        self._growth_form = value

    @property
    def life_cycle(self) -> LifeCycle:
        return LifeCycle(self._life_cycle)

    @life_cycle.setter
    def life_cycle(self, value: LifeCycle | str) -> None:
        """
        Sets the life cycle value, converting strings to LifeCycle enum if needed.
        
        Args:
            value: LifeCycle enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any LifeCycle enum
            TypeError: If value is neither string nor LifeCycle enum
        """
        if isinstance(value, str):
            try:
                value = LifeCycle[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid life cycle value: {value}")
        self._life_cycle = value

    @property
    def primary_use(self) -> UseCategory:
        return UseCategory(self._primary_use)

    @primary_use.setter
    def primary_use(self, value: UseCategory | str) -> None:
        """
        Sets the primary use value, converting strings to UseCategory enum if needed.
        
        Args:
            value: UseCategory enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any UseCategory enum
            TypeError: If value is neither string nor UseCategory enum
        """
        if isinstance(value, str):
            try:
                value = UseCategory[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid primary use value: {value}")
        self._primary_use = value

    @property
    def secondary_use(self) -> Optional[UseCategory]:
        return UseCategory(self._secondary_use) if self._secondary_use else None

    @secondary_use.setter
    def secondary_use(self, value: Optional[UseCategory | str]) -> None:
        """
        Sets the secondary use value, converting strings to UseCategory enum if needed.
        
        Args:
            value: UseCategory enum, string matching enum name (case-insensitive), or None
            
        Raises:
            ValueError: If string value doesn't match any UseCategory enum
            TypeError: If value is neither string, UseCategory enum, nor None
        """
        if value is None:
            self._secondary_use = None
        elif isinstance(value, str):
            try:
                self._secondary_use = UseCategory[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid secondary use value: {value}")
        else:
            self._secondary_use = value

    @validates('hardiness_zone_min', 'hardiness_zone_max')
    def validate_hardiness_zone(self, key, value: Optional[int]) -> Optional[int]:
        """Validates hardiness zone values if provided."""
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("Hardiness zone must be an integer")
            if not 1 <= value <= 13:
                raise ValueError("Hardiness zone must be between 1 and 13")
        return value

    @validates('preferred_soil_ph_min', 'preferred_soil_ph_max')
    def validate_soil_ph(self, key, value: Optional[float]) -> Optional[float]:
        """Validates soil pH values if provided."""
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Soil pH must be a number")
            if not 0 <= value <= 14:
                raise ValueError("Soil pH must be between 0 and 14")
        return float(value) if value is not None else None

    def json(self):
        """
        Returns a dictionary representation of the plant suitable for JSON serialization.
        """
        return {
            'id': self.id,
            'garden_location_id': self.garden_location_id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'variety': self.variety,
            'growth_form': self.growth_form.name,
            'life_cycle': self.life_cycle.name,
            'primary_use': self.primary_use.name,
            'secondary_use': self.secondary_use.name if self.secondary_use else None,
            'expected_height_inches': self.expected_height_inches,
            'expected_spread_inches': self.expected_spread_inches,
            'hardiness_zone_min': self.hardiness_zone_min,
            'hardiness_zone_max': self.hardiness_zone_max,
            'preferred_soil_ph_min': self.preferred_soil_ph_min,
            'preferred_soil_ph_max': self.preferred_soil_ph_max,
            'planting_depth_inches': self.planting_depth_inches,
            'spacing_inches': self.spacing_inches,
            'description': self.description,
            'care_instructions': self.care_instructions,
            'notes': self.notes
        }

    def __repr__(self) -> str:
        return f"<Plant(name={self.name}, form={self.growth_form.value})>"
