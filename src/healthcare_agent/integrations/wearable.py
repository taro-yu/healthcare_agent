from datetime import date, timedelta
from typing import Dict, Any, Optional, List

def get_metrics(start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
    # スタブ: 実装時は各APIのOAuthとデータ取得を実装
    # start/endはYYYY-MM-DD
    return {
        "period": {"start": start, "end": end},
        "steps": 6420,
        "sleep_hours": 6.5,
        "water_ml": 1200,
        "resting_hr": 78,
        "calories_out": 2050,
    }

def trend(metric: str, days: int = 7) -> List[float]:
    # スタブ: ランダムな緩やかなトレンド
    base = 6000 if metric == "steps" else 7.0
    return [base + (i - days/2) * 120 for i in range(days)]