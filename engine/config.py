import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
MYSELF_DIR = BASE_DIR / "myself"
OPPORTUNITIES_DIR = BASE_DIR / "opportunities"
TEMPLATES_DIR = BASE_DIR / "templates"
PROMPTS_DIR = BASE_DIR / "prompts"
EXPORTS_DIR = BASE_DIR / "exports"

class Settings(BaseModel):
    app_name: str = "Career-Application-Agent"
    version: str = "1.0.0"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    default_model: str = "gemini-2.5-flash"  # or openai/anthropic/local
    target_ats_score: float = 95.0

settings = Settings()
