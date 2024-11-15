from enum import Enum

class UseCategory(Enum):
    """Primary use or purpose of the plant"""
    ORNAMENTAL = "ORNAMENTAL"
    VEGETABLE = "VEGETABLE"
    FRUIT = "FRUIT"
    HERB_CULINARY = "HERB_CULINARY"
    HERB_MEDICINAL = "HERB_MEDICINAL"
    GROUND_COVER = "GROUND_COVER"
    SHADE = "SHADE"
    PRIVACY = "PRIVACY"
    NATIVE_HABITAT = "NATIVE_HABITAT"
    POLLINATOR = "POLLINATOR"