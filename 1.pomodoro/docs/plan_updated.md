# 作業計画（更新版）

目的: ドキュメントと UI を整備し、ローカルでの確認と自動化（CI）につなげる。

実施済み:

- 単体テストをルートの `tests/test_timer.py` に集約し、重複ファイルを削除
- フロントエンドの UI を実装（`templates/index.html`, `static/css/style.css`, `static/js/timer.js`）
- SVG プログレスリングとカード型レイアウトを追加

現在の状況:

- ローカルで `python app.py` を実行して UI の動作確認可能
- `pytest -q tests` で既存テストが実行できる状態

今後の優先事項:

- UI の微調整（色、タイポグラフィ、モバイル表示の細部）
- プログレスリングの滑らかなアニメーション追加
- セッションや完了数の永続化（ローカルストレージ / サーバ保存）
- アクセシビリティ（キーボード操作、ARIA 属性）の改善
- CI（GitHub Actions）でのテスト実行と自動デプロイ検討

確認/実行コマンド:

```bash
cd 1.pomodoro
source .venv/bin/activate   # 必要に応じて
python app.py               # アプリ起動（http://127.0.0.1:5000）
pytest -q tests             # テスト実行
```

次のアクションを希望する場合は教えてください（例: アニメーション追加、永続化の実装、CI ワークフロー作成）。
