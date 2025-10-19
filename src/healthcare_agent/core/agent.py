import json
from typing import List, Dict, Any
from health_agent.core.openai_client import OpenAIClient
from health_agent.core.tools import ToolRegistry
from health_agent.core.prompts import SYSTEM_PROMPT
from health_agent.core.memory import MemoryStore
from health_agent.config.settings import settings
from health_agent.core.logger import get_logger

log = get_logger(__name__)

class HealthAgent:
    def __init__(self):
        self.client = OpenAIClient()
        self.memory = MemoryStore()
        self.tools = ToolRegistry(self.memory)
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def _retrieve_context(self, user_text: str) -> str:
        hits = self.memory.search(user_text)
        if not hits:
            return ""
        lines = [f"- {c}" for _, c, _ in hits]
        return "参考メモ:\n" + "\n".join(lines)

    def handle_user_message(self, user_text: str, locale: str = "ja-JP") -> str:
        # 短期: 履歴に追加
        self.history.append({"role": "user", "content": user_text})
        # 長期: 関連メモを取得してコンテキストに付与
        context = self._retrieve_context(user_text)
        if context:
            self.history.append({"role": "system", "content": context})

        # ツール使用の対話ループ
        iterations = 0
        while iterations < settings.MAX_TOOL_ITERATIONS:
            iterations += 1
            resp = self.client.chat(messages=self.history, tools=self.tools.tool_schemas())
            choice = resp.choices[0]
            msg = choice.message

            # ツールコールがある場合は実行
            if msg.tool_calls:
                self.history.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})
                for tc in msg.tool_calls:
                    name = tc.function.name
                    args_json = tc.function.arguments
                    result = self.tools.run(name, args_json)
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": name,
                        "content": json.dumps(result, ensure_ascii=False),
                    })
                # 続けて再呼び出し
                continue

            # 最終応答
            content = msg.content or "(応答が空でした)"
            # ユーザの有益情報をメモ化（保存はコスト抑制のため任意）
            if len(user_text) < 300:
                try:
                    self.memory.save(f"USER_NOTE: {user_text}", mtype="user", embed=True)
                except Exception as e:
                    log.warning(f"memory save failed: {e}")
            self.history.append({"role": "assistant", "content": content})
            return content

        # 失敗フォールバック
        fallback = "うまく処理できませんでした。もう一度お願いできますか？"
        self.history.append({"role": "assistant", "content": fallback})
        return fallback