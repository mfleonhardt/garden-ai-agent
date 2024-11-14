from typing import Optional, Tuple
from sqlalchemy.orm import validates

from ..database import db
from ..fields import SunExposure, WindExposure, Drainage

class GardenLocation(db.Model):
    """
    Represents a specific location within a garden with its environmental characteristics.
    
    Each garden location belongs to an irrigation zone and has specific geographical
    coordinates and environmental conditions that affect plant growth and care requirements.
    """
    __tablename__ = 'garden_locations'

    id = db.Column(db.Integer, primary_key=True)
    irrigation_zone_id = db.Column(
        db.Integer, 
        db.ForeignKey('irrigation_zones.id', name='fk_garden_locations_irrigation_zone'), 
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=True)  # in feet above sea level
    _sun_exposure = db.Column("sun_exposure", db.Enum(SunExposure), nullable=False)
    _wind_exposure = db.Column("wind_exposure", db.Enum(WindExposure), nullable=False)
    _drainage = db.Column("drainage", db.Enum(Drainage), nullable=False)
    plants = db.relationship(
        'Plant',
        backref='garden_location',
        lazy='select'
    )

    @validates('name')
    def validate_name(self, key, value: str) -> str:
        """
        Validates the location name.
        
        Args:
            key: Field name (unused)
            value: Location name to validate
            
        Returns:
            str: Validated and stripped name
            
        Raises:
            ValueError: If name is empty or too long
        """
        if not value or not value.strip():
            raise ValueError("Location name cannot be empty")
        if len(value) > 100:
            raise ValueError("Location name cannot exceed 100 characters")
        return value.strip()

    @validates('latitude')
    def validate_latitude(self, key, value: float) -> float:
        """
        Validates the latitude value.
        
        Args:
            key: Field name (unused)
            value: Latitude to validate
            
        Returns:
            float: Validated latitude
            
        Raises:
            ValueError: If latitude is outside valid range
            TypeError: If latitude is not a number
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value: float) -> float:
        """
        Validates the longitude value.
        
        Args:
            key: Field name (unused)
            value: Longitude to validate
            
        Returns:
            float: Validated longitude
            
        Raises:
            ValueError: If longitude is outside valid range
            TypeError: If longitude is not a number
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return float(value)

    @validates('elevation')
    def validate_elevation(self, key, value: Optional[float]) -> Optional[float]:
        """
        Validates the elevation value if provided.
        
        Args:
            key: Field name (unused)
            value: Elevation to validate
            
        Returns:
            Optional[float]: Validated elevation or None
            
        Raises:
            TypeError: If elevation is provided but not a number
            ValueError: If elevation is below sea level (negative)
        """
        if value is None:
            return None
        if not isinstance(value, (int, float)):
            raise TypeError("Elevation must be a number")
        if value < 0:
            raise ValueError("Elevation cannot be below sea level")
        return float(value)

    @property
    def sun_exposure(self) -> SunExposure:
        return SunExposure(self._sun_exposure)

    @sun_exposure.setter
    def sun_exposure(self, value: SunExposure | str) -> None:
        """
        Sets the sun exposure value, converting strings to SunExposure enum if needed.
        
        Args:
            value: SunExposure enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any SunExposure enum
            TypeError: If value is neither string nor SunExposure enum
        """
        if isinstance(value, str):
            try:
                value = SunExposure[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid sun exposure value: {value}")
        self._sun_exposure = value

    @property
    def wind_exposure(self) -> WindExposure:
        return WindExposure(self._wind_exposure)

    @wind_exposure.setter
    def wind_exposure(self, value: WindExposure | str) -> None:
        """
        Sets the wind exposure value, converting strings to WindExposure enum if needed.
        
        Args:
            value: WindExposure enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any WindExposure enum
            TypeError: If value is neither string nor WindExposure enum
        """
        if isinstance(value, str):
            try:
                value = WindExposure[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid wind exposure value: {value}")
        self._wind_exposure = value

    @property
    def drainage(self) -> Drainage:
        return Drainage(self._drainage)

    @drainage.setter
    def drainage(self, value: Drainage | str) -> None:
        """
        Sets the drainage value, converting strings to Drainage enum if needed.
        
        Args:
            value: Drainage enum or string matching enum name (case-insensitive)
            
        Raises:
            ValueError: If string value doesn't match any Drainage enum
            TypeError: If value is neither string nor Drainage enum
        """
        if isinstance(value, str):
            try:
                value = Drainage[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid drainage value: {value}")
        self._drainage = value

    def __repr__(self) -> str:
        return (f"<GardenLocation(name={self.name}, "
                f"location=({self.longitude}, {self.latitude}), "
                f"elevation={self.elevation})>")

    @property
    def coordinates(self) -> Tuple[float, float]:
        """
        Gets the location's coordinates as a tuple.
        
        Returns:
            Tuple[float, float]: (latitude, longitude)
        """
        return (self.latitude, self.longitude)

    def json(self):
        return {
            'name': self.name,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'elevation': self.elevation,
            'sun_exposure': self.sun_exposure.name,
            'wind_exposure': self.wind_exposure.name,
            'drainage': self.drainage.name,
            'irrigation_zone_id': self.irrigation_zone_id
        }