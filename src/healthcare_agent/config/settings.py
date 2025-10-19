import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    DB_PATH: str = os.getenv("DB_PATH", "./ai_health_agent.sqlite3")
    DEFAULT_LOCALE: str = os.getenv("DEFAULT_LOCALE", "ja-JP")
    MAX_TOOL_ITERATIONS: int = 4
    MEMORY_TOP_K: int = 4
    MEMORY_MIN_SIM: float = 0.25

settings = Settings()