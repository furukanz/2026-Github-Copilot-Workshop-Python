# ポモドーロタイマーWebアプリ アーキテクチャ案

## 1. ディレクトリ構成

```
1.pomodoro/
  app.py           # Flaskアプリ本体
  timer.py         # タイマーのビジネスロジック
  history.py       # 履歴管理ロジック
  templates/       # HTMLテンプレート
    index.html
  static/
    css/
      style.css    # デザイン
    js/
      timer.js     # タイマー制御
  tests/           # ユニットテスト
    test_timer.py
    test_history.py
    test_app.py
```

## 2. アーキテクチャ概要

### バックエンド（Flask）
- タイマーや履歴管理などのロジックを独立したモジュール（timer.py, history.py）で実装
- APIエンドポイント（タイマー操作、履歴取得など）をRESTfulに設計
- 設定値や履歴の保存は抽象化したインターフェース経由でアクセス

### フロントエンド（HTML/CSS/JavaScript）
- UIモックに基づく画面構成（タイマー表示、ボタン、進捗バーなど）
- JavaScriptでタイマー制御（カウントダウン、アラート、状態切替）
- AjaxでFlask APIと通信（設定変更や履歴取得）
- UIはレスポンシブ対応

## 3. ユニットテストのしやすさへの配慮
- ビジネスロジックをFlaskルートやビューから分離し、直接ユニットテスト可能な構成
- テスト用ディレクトリ（tests/）を設置し、pytest等で自動テスト
- モックやスタブを使ったテストが容易な抽象化
- JavaScriptもモジュール化し、Jest等で単体テスト可能

## 4. 拡張性
- ユーザー認証（必要ならFlask-Login等）
- 履歴保存（SQLiteやファイル、セッション）
- 設定画面や通知機能

---

このアーキテクチャは、シンプルかつ拡張しやすく、ユニットテストのしやすさにも配慮した構成です。