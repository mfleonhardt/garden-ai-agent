from datetime import datetime
from typing import Optional
from sqlalchemy.orm import validates

from ..database import db
from ..fields import MeasurementType, MeasurementUnit

class Measurement(db.Model):
    """
    Represents a measurement taken at a specific garden location.
    
    Each measurement record contains the type of measurement (e.g., temperature, rainfall),
    the value and unit, when it was taken, and optional metadata like measurement period
    and data source.
    """
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    garden_location_id = db.Column(
        db.Integer,
        db.ForeignKey('garden_locations.id', name='fk_measurements_garden_location'),
        nullable=False
    )
    _measurement_type = db.Column("measurement_type", db.Enum(MeasurementType), nullable=False)
    _unit = db.Column("unit", db.Enum(MeasurementUnit), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    period_minutes = db.Column(db.Integer, nullable=True)  # For measurements over time (e.g., rainfall over 24h)
    source = db.Column(db.String(50), nullable=True)  # e.g., 'SENSOR', 'MANUAL', 'WEATHER_API'
    notes = db.Column(db.Text, nullable=True)
    
    # Relationship to garden location
    garden_location = db.relationship(
        'GardenLocation',
        backref='measurements',
        lazy='select'
    )

    @validates('value')
    def validate_value(self, key, value: float) -> float:
        """
        Validates the measurement value.
        
        Args:
            key: Field name (unused)
            value: Measurement value to validate
            
        Returns:
            float: Validated value
            
        Raises:
            TypeError: If value is not a number
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Measurement value must be a number")
        return float(value)

    @validates('period_minutes')
    def validate_period_minutes(self, key, value: Optional[int]) -> Optional[int]:
        """
        Validates the measurement period if provided.
        
        Args:
            key: Field name (unused)
            value: Period in minutes to validate
            
        Returns:
            Optional[int]: Validated period or None
            
        Raises:
            TypeError: If period is provided but not an integer
            ValueError: If period is negative or zero
        """
        if value is None:
            return None
        if not isinstance(value, int):
            raise TypeError("Period must be an integer number of minutes")
        if value <= 0:
            raise ValueError("Period must be greater than 0 minutes")
        return value

    @validates('source')
    def validate_source(self, key, value: Optional[str]) -> Optional[str]:
        """Validates the measurement source if provided."""
        if value is None:
            return None
        value = value.strip().upper()
        if len(value) > 50:
            raise ValueError("Source identifier cannot exceed 50 characters")
        return value

    @property
    def measurement_type(self) -> MeasurementType:
        return MeasurementType(self._measurement_type)

    @measurement_type.setter
    def measurement_type(self, value: MeasurementType | str) -> None:
        """Sets the measurement type, converting strings to enum if needed."""
        if isinstance(value, str):
            try:
                value = MeasurementType[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid measurement type: {value}")
        self._measurement_type = value

    @property
    def unit(self) -> MeasurementUnit:
        return MeasurementUnit(self._unit)

    @unit.setter
    def unit(self, value: MeasurementUnit | str) -> None:
        """Sets the measurement unit, converting strings to enum if needed."""
        if isinstance(value, str):
            try:
                value = MeasurementUnit[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid measurement unit: {value}")
        self._unit = value

    def __repr__(self) -> str:
        return (f"<Measurement(type={self.measurement_type.name}, "
                f"value={self.value}{self.unit.value}, "
                f"location_id={self.garden_location_id}, "
                f"timestamp={self.timestamp})>")

    def json(self):
        """Returns a dictionary representation suitable for JSON serialization."""
        return {
            'id': self.id,
            'garden_location_id': self.garden_location_id,
            'measurement_type': self.measurement_type.name,
            'unit': self.unit.name,
            'value': self.value,
            'timestamp': self.timestamp.isoformat(),
            'period_minutes': self.period_minutes,
            'source': self.source,
            'notes': self.notes
        } 