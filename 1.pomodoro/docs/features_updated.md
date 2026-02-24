# 機能一覧（更新版）

主な変更点（更新）:


主要ファイル:

# 機能一覧（更新版）

主な機能（今回の更新を含む）:

- 円形のプログレスリングによる視覚的タイマー表示（SVG）
- 大きな中央タイム表示とステータスラベル（作業中 / 休憩中）
- `開始` / `リセット` ボタンによる操作
- 今日の進捗サマリー（完了数・合計集中時間）の表示
- モバイル/デスクトップ両対応のカード型 UI（レスポンシブ）
- 単体テストはルートの `tests/test_timer.py` に集約済み（テストは既に通過確認）

主要ファイル:

- `1.pomodoro/templates/index.html` — UI の HTML
- `1.pomodoro/static/css/style.css` — デザイン（グラデーション、カード、ボタン）
- `1.pomodoro/static/js/timer.js` — クライアントタイマーロジックとプログレス表示
- `1.pomodoro/timer.py` — `PomodoroTimer` クラス（タイマー本体）
- `1.pomodoro/app.py` — Flask エントリポイント
- `tests/test_timer.py` — ユニットテスト

実行/確認コマンド:

```bash
cd 1.pomodoro
source .venv/bin/activate   # 必要な場合
python app.py               # 127.0.0.1:5000 を開く
pytest -q tests             # テスト実行
```

必要に応じて、色やフォント、アニメーションの微調整を行うことで見た目をさらに改善できます。
