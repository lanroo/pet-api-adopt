"""
Constants for Pet Adoption API

This module contains application-wide constants.
"""

# API Configuration
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# File Upload
UPLOAD_DIR = "uploads"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Database
DATABASE_URL = "sqlite:///./pet_adoption.db"

# Age limits (in months)
MIN_AGE_MONTHS = 0
MAX_AGE_MONTHS = 300  # 25 years

# String lengths
MAX_NAME_LENGTH = 100
MAX_BREED_LENGTH = 100
MAX_CITY_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000
MAX_EMAIL_LENGTH = 255
MAX_PHONE_LENGTH = 20
MAX_FULL_NAME_LENGTH = 200
