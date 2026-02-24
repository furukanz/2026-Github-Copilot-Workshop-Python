# 機能一覧（更新版）

主な変更点（更新）:

- `PomodoroTimer` のユニットテストを `tests/test_timer.py` に追加しました。
- 重複していた `1.pomodoro/tests/test_timer.py` は削除して、テストを一元化しました。
- 現在、テストは 4 件通過しています（`pytest -q tests` 実行時）。

主要ファイル:

- `1.pomodoro/timer.py` — タイマー本体
- `1.pomodoro/app.py` — Flask エントリポイント
- `tests/test_timer.py` — ユニットテスト（統合済み）
