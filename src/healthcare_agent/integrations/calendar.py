from typing import Dict

def set_reminder(text: str, when_iso: str) -> Dict[str, str]:
    # スタブ: 実装時はGoogle Calendar等へ登録
    return {"status": "scheduled", "text": text, "when": when_iso}