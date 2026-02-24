# アーキテクチャ（更新版）

このプロジェクトは軽量な Flask フロントエンドと、`PomodoroTimer` を提供するモジュールで構成されています。

- Flask アプリケーション: `1.pomodoro/app.py`
- タイマー実装: `1.pomodoro/timer.py` （`PomodoroTimer` クラス）
- テスト: ルートの `tests/test_timer.py` に統合されています（重複ファイルは削除済み）。

テストの実行方法:

```bash
pytest -q tests
```

注意: 既存のドキュメントファイルはそのまま残してあります。こちらは参照用の「更新版」です。
