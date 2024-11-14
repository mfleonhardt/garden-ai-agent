from enum import Enum

class ObservationType(Enum):
    """Categories of plant observations"""
    HEIGHT = "HEIGHT"  # Height in inches
    SPREAD = "SPREAD"  # Spread/width in inches
    HEALTH = "HEALTH"  # Health rating (1-5)
    LEAF_COUNT = "LEAF_COUNT"  # Number of leaves
    FLOWER_COUNT = "FLOWER_COUNT"  # Number of flowers
    FRUIT_COUNT = "FRUIT_COUNT"  # Number of fruits
    GROWTH_STAGE = "GROWTH_STAGE"  # Current growth stage
    PEST_DAMAGE = "PEST_DAMAGE"  # Pest damage rating (1-5)
    DISEASE_SEVERITY = "DISEASE_SEVERITY"  # Disease severity rating (1-5)
