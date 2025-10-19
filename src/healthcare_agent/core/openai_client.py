from typing import List, Dict, Any
from openai import OpenAI
from health_agent.config.settings import settings
from health_agent.core.logger import get_logger

log = get_logger(__name__)

class OpenAIClient:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def chat(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] | None = None):
        resp = self.client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else "none",
            temperature=0.3,
        )
        return resp

    def embed(self, texts: List[str]) -> List[List[float]]:
        resp = self.client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=texts,
        )
        return [d.embedding for d in resp.data]