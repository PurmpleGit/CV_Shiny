from enum import Enum

class Confidence(float, Enum):
    VERY_LOW = 0.95
    LOW = 0.98
    MEDIUM = 0.985
    HIGH = 0.99
    HIGHER = 0.994
    VERY_HIGH = 0.995
    PERFECT = 0.999