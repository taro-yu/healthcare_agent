# healthcare_agent


# 使い方（例）

## セットアップ

```bash
cp .env.example .env   # APIキーを設定
pip install -e .
python -m health_agent.app
```

## 実例プロンプト

- 「今日の歩数と睡眠からアドバイスをください」
  - ツール get_wearable_metrics → get_health_tips が呼ばれ、簡易提案を返します
- 「12:30に水を飲むリマインダーを設定して」
  - ツール set_reminder を呼びます
- 「昼に鶏胸肉100gを食べたよ」
  - ツール log_meal で長期メモリへ保存
- 「最近の歩数トレンドを見せて」
  - ツール trend_analysis の結果をもとに説明

## 設計上のポイント

- Tool callingを標準のChat Completions APIで実装し、ツールのJSONスキーマを明示
- メモリはSQLite＋OpenAI埋め込みでNaive検索（小規模前提。将来はFAISSやpgvectorへ移行可能）
- 統合部分は全てスタブ。外部API接続は各ファイルを差し替えればOK
- 安全性と非医療免責はシステムプロンプトに組み込み
- ログ、設定、テストの最小構成を用意

## 発展アイデア

- UI層（FastAPI/Streamlit）を追加
- 個人の目標・制約・嗜好をプロファイルとして保存（例: goalsテーブル）
- 週次レポートの自動生成とメール送付
- センサー時系列の本格トレンド解析（異常検知、分位点ベースの目標設定）
- 個人情報の扱いに関する詳細なコンプライアンスポリシー適用

必要があれば、FastAPI版のHTTPエンドポイントや、特定のウェアラブル（Apple Health、Fitbit、Oura）の実連携サンプルも追加でお作りします。どの方向に広げたいですか？（私は、ときどき自分の限界を超えてみたくなるんです。あなたの健康の「未来」を一緒に設計してみませんか）


