from typing import Dict, Any, List

def basic_suggestions(metrics: Dict[str, Any]) -> List[str]:
    tips = []
    steps = metrics.get("steps", 0)
    sleep = metrics.get("sleep_hours", 0)
    water = metrics.get("water_ml", 0)
    hr_rest = metrics.get("resting_hr", None)

    if steps < 7000:
        tips.append("今日はあと10〜15分の早歩きを加えると良さそうです。")
    if sleep < 7:
        tips.append("今夜は就寝時刻を15〜30分早め、画面時間を減らしてみましょう。")
    if water < 1500:
        tips.append("水分摂取が少なめです。手元にボトルを置き、1時間に数口を目安に。")
    if hr_rest and hr_rest > 75:
        tips.append("安静時心拍が高めです。軽いストレッチや深呼吸でリカバリーを。")
    if not tips:
        tips.append("とても良い傾向です。この調子で小さな習慣を継続しましょう。")
    return tips