"""
config/__init__.py
Central configuration file for
AI College Admission Assistant – BFGI
"""

import os
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


# =========================================================
# CORE APPLICATION CONFIGURATION
# =========================================================
class BaseConfig:
    # Project Metadata
    PROJECT_NAME = os.getenv("PROJECT_NAME", "College Admission Assistant")
    COLLEGE_NAME = os.getenv(
        "COLLEGE_NAME",
        "Baba Farid Group of Institutions, Bathinda"
    )

    # Server Configuration
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-default-secret")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Data & Storage
    DATA_DIR = os.path.join(BASE_DIR, "data")
    ADMISSION_DATA_PATH = os.path.join(DATA_DIR, "admissions.json")

    # Database (future-ready)
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "json")  # json | sqlite | postgres
    DATABASE_URL = os.getenv("DATABASE_URL", "")


# =========================================================
# AI & CHATBOT CONFIGURATION
# =========================================================
class AIConfig:
    # Provider
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

    # AI Behavior Controls
    TEMPERATURE = float(os.getenv("AI_TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", 300))

    # Central System Prompt
    SYSTEM_PROMPT = (
        "You are the official AI Admission Assistant of "
        "Baba Farid Group of Institutions, Bathinda. "
        "Answer student queries clearly and politely about "
        "courses, eligibility, fees, scholarships, hostel, "
        "placements, and admission process using simple language."
    )


# =========================================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# =========================================================
class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


# =========================================================
# CONFIGURATION SELECTOR
# =========================================================
def get_config():
    """
    Returns the appropriate configuration class
    based on ENV environment variable
    """
    env = os.getenv("ENV", "development").lower()

    if env == "production":
        return ProductionConfig

    return DevelopmentConfig


# =========================================================
# EXPORT CONFIG OBJECTS
# =========================================================
AppConfig = get_config()
AISettings = AIConfig
