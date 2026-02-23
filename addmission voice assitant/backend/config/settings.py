import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "admission-secret")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", 0.7))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", 300))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")