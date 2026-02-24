# アーキテクチャ（更新版）

このプロジェクトは軽量な Flask フロントエンドに、クライアント側の UI 実装（HTML/CSS/JS）と、タイマーのロジックを提供するモジュールで構成されています。

主な構成:

- Flask アプリケーション: `1.pomodoro/app.py`（エントリポイント）
- テンプレート: `1.pomodoro/templates/index.html`（UI の HTML）
- スタティック資産: `1.pomodoro/static/css/style.css`, `1.pomodoro/static/js/timer.js`（デザインとクライアントロジック）
- タイマー実装（バックエンド補助）: `1.pomodoro/timer.py`（`PomodoroTimer` クラス）
- テスト: ルートの `tests/test_timer.py` に統合（重複ファイルは削除）

今回のフロントエンド更新のポイント:

- 円形のプログレスリング（SVG）を用いた視覚的なタイマー表示
- グラデーションを用いた背景とカードデザイン、角丸レイアウト
- 「開始」「リセット」ボタン、今日の進捗セクションを追加

ローカルでの起動手順:

```bash
cd 1.pomodoro
source .venv/bin/activate   # 仮想環境を利用している場合
python app.py
```

ブラウザで http://127.0.0.1:5000 を開くと UI を確認できます。

（このファイルはアーキテクチャの概要と、今回追加したフロントエンド資産の位置・役割を示します。）
