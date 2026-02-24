# ポモドーロタイマーWebアプリ アーキテクチャ

## 1. ディレクトリ構成

```
1.pomodoro/
  app.py             # Flask アプリケーションエントリポイント
  timer.py           # タイマービジネスロジック（PomodoroTimer クラス）
  templates/
    index.html       # メイン画面 HTML テンプレート
  static/
    css/
      style.css      # スタイルシート
    js/
      timer.js       # フロントエンドタイマー制御
  docs/              # ドキュメント
tests/
  test_timer.py      # PomodoroTimer ユニットテスト
```

## 2. アーキテクチャ概要

### バックエンド（Flask）

- `app.py` — Flask アプリケーションを生成し、ルートパス（`/`）で `index.html` を返す単一ルート構成
- `timer.py` — `PomodoroTimer` クラスによるタイマーのビジネスロジックをバックエンド側で定義（現状はフロントエンドと独立）

現時点では REST API エンドポイントは存在せず、Flask はテンプレート配信のみを担当しています。

### フロントエンド（HTML/CSS/JavaScript）

- `templates/index.html` — タイマー表示・ボタン（開始・リセット）・状態表示を含むシンプルなページ
- `static/js/timer.js` — ブラウザ上でカウントダウン・状態切替・アラート通知を完結させるバニラ JavaScript（サーバー通信なし）
- `static/css/style.css` — 中央配置・カード型レイアウトのスタイリング

## 3. レイヤー間の依存関係

```
ブラウザ（timer.js）  ←→  Flask（app.py）  ←  timer.py（独立モジュール）
```

- `timer.js` はサーバーと通信せず、すべてのタイマーロジックをブラウザ内で処理します。
- `timer.py` の `PomodoroTimer` クラスはバックエンドテスト用に定義されており、現在は Flask ルートからは参照されていません。

## 4. テスト構成

- `tests/test_timer.py` — `PomodoroTimer` クラスのユニットテスト（pytest）
- テスト実行コマンド:

```bash
pytest -q tests
```

## 5. 拡張の方向性

- REST API 化（タイマー状態のサーバー管理、履歴保存など）
- `timer.py` を Flask ルートに統合し、バックエンドでタイマーを管理
- 設定画面、ブラウザ通知、履歴表示などの UI 拡張