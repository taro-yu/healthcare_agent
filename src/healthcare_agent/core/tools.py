import json
from typing import Any, Dict, Callable, List
from health_agent.integrations import wearable, nutrition, calendar
from health_agent.core.memory import MemoryStore
from health_agent.core.health_rules import basic_suggestions

class ToolRegistry:
    def __init__(self, memory: MemoryStore):
        self.memory = memory
        self.impls: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            "get_wearable_metrics": self.get_wearable_metrics,
            "trend_analysis": self.trend_analysis,
            "log_meal": self.log_meal,
            "search_nutrition": self.search_nutrition,
            "set_reminder": self.set_reminder,
            "save_memory": self.save_memory,
            "retrieve_memory": self.retrieve_memory,
            "get_health_tips": self.get_health_tips,
        }

    def tool_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_wearable_metrics",
                    "description": "ウェアラブルの指標を取得する（スタブ）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "description": "YYYY-MM-DD"},
                            "end": {"type": "string", "description": "YYYY-MM-DD"},
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "trend_analysis",
                    "description": "指定メトリクスの直近トレンドを取得する（スタブ）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric": {"type": "string", "enum": ["steps", "sleep_hours", "water_ml", "resting_hr"]},
                            "days": {"type": "integer", "minimum": 3, "maximum": 30, "default": 7},
                        },
                        "required": ["metric"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "log_meal",
                    "description": "食事ログを保存する（長期メモリ）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_nutrition",
                    "description": "食品の簡易栄養情報を検索する（スタブ）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "set_reminder",
                    "description": "リマインダーを設定する（スタブ）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "when_iso": {"type": "string", "description": "ISO8601 datetime"},
                        },
                        "required": ["text", "when_iso"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "save_memory",
                    "description": "有用なメモを長期記憶に保存する",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "note": {"type": "string"},
                        },
                        "required": ["note"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_memory",
                    "description": "長期記憶から意味検索で取り出す",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "top_k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 4},
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_health_tips",
                    "description": "メトリクスから簡易アドバイスを生成（ローカル）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metrics": {"type": "object"},
                        },
                        "required": ["metrics"],
                    },
                },
            },
        ]

    # 実装群
    def get_wearable_metrics(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return wearable.get_metrics(start=args.get("start"), end=args.get("end"))

    def trend_analysis(self, args: Dict[str, Any]) -> Dict[str, Any]:
        metric = args["metric"]
        days = int(args.get("days", 7))
        series = wearable.trend(metric, days)
        return {"metric": metric, "days": days, "series": series}

    def log_meal(self, args: Dict[str, Any]) -> Dict[str, Any]:
        text = args["text"]
        self.memory.save(f"MEAL_LOG: {text}", mtype="note", embed=True)
        return {"status": "logged", "text": text}

    def search_nutrition(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return nutrition.lookup_food(args["query"])

    def set_reminder(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return calendar.set_reminder(args["text"], args["when_iso"])

    def save_memory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        note = args["note"]
        mid = self.memory.save(note, mtype="note", embed=True)
        return {"status": "saved", "id": mid}

    def retrieve_memory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        q = args["query"]
        k = int(args.get("top_k", 4))
        results = self.memory.search(q, top_k=k)
        return {"results": [{"id": rid, "content": c, "score": s} for rid, c, s in results]}

    def get_health_tips(self, args: Dict[str, Any]) -> Dict[str, Any]:
        tips = basic_suggestions(args["metrics"])
        return {"tips": tips}

    def run(self, name: str, arguments_json: str) -> Dict[str, Any]:
        fn = self.impls.get(name)
        if not fn:
            return {"error": f"Unknown tool: {name}"}
        try:
            args = json.loads(arguments_json or "{}")
        except Exception:
            args = {}
        return fn(args)