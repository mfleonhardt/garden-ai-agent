from enum import Enum

class MeasurementUnit(Enum):
    """Units for different types of measurements."""
    # Temperature
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    
    # Moisture/Humidity
    PERCENT = "%"
    
    # Rainfall
    MILLIMETERS = "mm"
    INCHES = "in"
    
    # Solar Radiation
    WATTS_PER_SQM = "W/m²"
    
    # Wind Speed
    METERS_PER_SEC = "m/s"
    KILOMETERS_PER_HOUR = "km/h"
    MILES_PER_HOUR = "mph"
    
    # Soil measurements
    PH = "pH"
    MICROSIEMENS = "µS/cm"  # For conductivity
    PPM = "ppm"  # For salinity 