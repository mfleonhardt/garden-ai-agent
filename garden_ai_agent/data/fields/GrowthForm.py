from enum import Enum

class GrowthForm(Enum):
    """Physical growth form and structure of the plant"""
    TREE = "TREE"
    SHRUB = "SHRUB"
    VINE = "VINE"
    HERB = "HERB"  # Non-woody plants
    GRASS = "GRASS"
    FERN = "FERN"
    GROUNDCOVER = "GROUNDCOVER"