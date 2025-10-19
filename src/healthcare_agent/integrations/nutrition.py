from typing import Dict, Any

def lookup_food(query: str) -> Dict[str, Any]:
    # スタブ: 実装時はEdamam/USDA等のAPIに接続
    # 例として簡易的な栄養情報を返す
    sample = {
        "chicken breast 100g": {"kcal": 165, "protein_g": 31, "fat_g": 3.6, "carb_g": 0},
        "tofu 150g": {"kcal": 108, "protein_g": 10, "fat_g": 6, "carb_g": 3},
        "banana 1": {"kcal": 96, "protein_g": 1.2, "fat_g": 0.3, "carb_g": 21},
    }
    best = None
    for k in sample.keys():
        if query.lower() in k:
            best = k
            break
    if not best:
        best = "banana 1"
    return {"item": best, "nutrients": sample[best]}