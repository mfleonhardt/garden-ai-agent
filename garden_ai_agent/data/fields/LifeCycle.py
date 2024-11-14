import enum

class LifeCycle(enum.Enum):
    """Plant's life cycle classification"""
    ANNUAL = "ANNUAL"  # Completes lifecycle in one growing season
    BIENNIAL = "BIENNIAL"  # Completes lifecycle in two growing seasons
    PERENNIAL = "PERENNIAL"  # Lives for multiple years
    EPHEMERAL = "EPHEMERAL"  # Short-lived perennial