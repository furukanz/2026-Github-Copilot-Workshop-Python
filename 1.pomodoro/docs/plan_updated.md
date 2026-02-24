# 作業計画（更新版）

目的: テストを一箇所にまとめて、CI やローカル実行を簡単にする。

実施済み:

- `tests/test_timer.py` をルートの `tests/` に追加。
- `1.pomodoro/tests/test_timer.py` を削除して重複を解消。
- `pytest -q` を実行し、4 件のテストが通過することを確認。

今後の候補:

- ドキュメント内の古い参照（`1.pomodoro/docs/*`）を統一してリンクを更新する。
- CI（GitHub Actions 等）で `pytest -q tests` を自動実行するワークフローを追加する。

テスト実行コマンド:

```bash
pytest -q tests
```
