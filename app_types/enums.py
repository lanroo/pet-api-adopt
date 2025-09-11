"""
Enum definitions for Pet Adoption API

This module contains all the enum types used in the application.
"""

import enum


class GenderEnum(str, enum.Enum):
    """Gender enumeration for pets"""
    MALE = "male"
    FEMALE = "female"


class SpeciesEnum(str, enum.Enum):
    """Species enumeration for pets"""
    DOG = "dog"
    CAT = "cat"


class StatusEnum(str, enum.Enum):
    """Status enumeration for pets"""
    AVAILABLE = "available"
    ADOPTED = "adopted"
    PENDING = "pending"
