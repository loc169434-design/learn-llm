from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_GEMINI_MODEL = "gemini-flash-lite-latest"


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = DEFAULT_GEMINI_MODEL


def get_settings() -> Settings:
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
    )
