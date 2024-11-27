from enum import Enum, auto

class MeasurementType(Enum):
    """Types of measurements that can be recorded."""
    TEMPERATURE = auto()
    HUMIDITY = auto()
    SOIL_MOISTURE = auto()
    SOIL_PH = auto()
    RAINFALL = auto()
    SOLAR_RADIATION = auto()
    WIND_SPEED = auto()
    SOIL_TEMPERATURE = auto()
    SOIL_CONDUCTIVITY = auto()
    SOIL_SALINITY = auto()
