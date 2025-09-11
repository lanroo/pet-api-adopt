"""
Validation utilities for Pet Adoption API

This module contains validation functions and utilities.
"""

from typing import Optional
from .enums import GenderEnum, SpeciesEnum, StatusEnum


def validate_age(age: Optional[float]) -> bool:
    """
    Validate if age is within acceptable range (0-300 months)
    """
    if age is None:
        return True
    return 0 <= age <= 300


def validate_gender(gender: str) -> bool:
    """
    Validate if gender is a valid enum value
    """
    try:
        GenderEnum(gender)
        return True
    except ValueError:
        return False


def validate_species(species: str) -> bool:
    """
    Validate if species is a valid enum value
    """
    try:
        SpeciesEnum(species)
        return True
    except ValueError:
        return False


def validate_status(status: str) -> bool:
    """
    Validate if status is a valid enum value
    """
    try:
        StatusEnum(status)
        return True
    except ValueError:
        return False
