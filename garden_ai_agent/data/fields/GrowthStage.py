from enum import Enum

class GrowthStage(Enum):
    """Plant growth stages"""
    SEED = "SEED"
    GERMINATION = "GERMINATION" 
    SEEDLING = "SEEDLING"
    VEGETATIVE = "VEGETATIVE"
    FLOWERING = "FLOWERING"
    FRUITING = "FRUITING"
    DORMANT = "DORMANT"
    DEAD = "DEAD"
