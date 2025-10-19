import sqlite3
import json
import time
from typing import List, Tuple
from health_agent.config.settings import settings
from health_agent.core.openai_client import OpenAIClient
from health_agent.core.logger import get_logger
import math

log = get_logger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,           -- 'user', 'agent', 'note'
  content TEXT NOT NULL,
  embedding TEXT,               -- JSON array of floats
  created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at);
"""

def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb + 1e-9)

class MemoryStore:
    def __init__(self, path: str | None = None):
        self.path = path or settings.DB_PATH
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.executescript(SCHEMA)
        self.client = OpenAIClient()

    def save(self, content: str, mtype: str = "note", embed: bool = True) -> int:
        emb_json = None
        if embed:
            emb = self.client.embed([content])[0]
            emb_json = json.dumps(emb)
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memories(type, content, embedding, created_at) VALUES (?, ?, ?, ?)",
            (mtype, content, emb_json, time.time()),
        )
        self.conn.commit()
        return cur.lastrowid

    def search(self, query: str, top_k: int = None, min_sim: float = None) -> List[Tuple[int, str, float]]:
        top_k = top_k or settings.MEMORY_TOP_K
        min_sim = min_sim or settings.MEMORY_MIN_SIM
        q_emb = self.client.embed([query])[0]
        rows = self.conn.execute("SELECT id, content, embedding FROM memories WHERE embedding IS NOT NULL").fetchall()
        scored = []
        for rid, content, emb_json in rows:
            try:
                emb = json.loads(emb_json)
                sim = cosine(q_emb, emb)
                if sim >= min_sim:
                    scored.append((rid, content, sim))
            except Exception:
                continue
        scored.sort(key=lambda x: x[2], reverse=True)
        return scored[:top_k]

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass