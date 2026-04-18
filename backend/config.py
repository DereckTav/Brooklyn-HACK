"""Balance constants and runtime settings for Mogul Blocks."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Balance:
    STARTING_CASH: int = 22_000
    MAX_TURNS: int = 20
    EARLY_WIN_TURN: int = 10
    EARLY_WIN_NET_WORTH: int = 100_000
    EARLY_WIN_MIN_PROPERTIES: int = 3

    AP_DICE_SIDES: int = 4
    AP_DICE_MODIFIER: int = 1
    AP_MIN: int = 2
    AP_MAX: int = 5

    LOW_ROLL_PENALTY_CASH: int = 1_000

    PROPERTY_EXPIRY_TURNS: int = 5
    FLIPPER_EYES_WARN_TURNS_EASY: int = 2
    FLIPPER_EYES_WARN_TURNS_HARD: int = 1

    BASE_YIELD_PERCENT: float = 0.12

    MORTGAGE_UNLOCK_TURN: int = 10
    HEAT_INDICATOR_TURNS_BEFORE: int = 2
    AI_BID_NOISE: float = 0.10


BALANCE = Balance()


CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_TRIVIA_MODEL = os.getenv("OPENAI_TRIVIA_MODEL", "gpt-4o-mini")
DB_PATH = os.getenv("MOGUL_BLOCKS_DB_PATH", "backend/data/mogul_blocks.db")
