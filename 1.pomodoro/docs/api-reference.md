# APIリファレンス

## 概要

現在のポモドーロタイマーアプリは、Flask によるシンプルなページ配信のみを行っています。REST API エンドポイントは存在せず、タイマーのすべてのロジックはブラウザ上の JavaScript で完結しています。

---

## エンドポイント一覧

### GET /

メイン画面を返します。

**リクエスト**

```
GET / HTTP/1.1
Host: localhost:5000
```

**レスポンス**

- ステータスコード: `200 OK`
- Content-Type: `text/html`
- ボディ: `templates/index.html` をレンダリングした HTML

**例**

```bash
curl http://localhost:5000/
```

---

## 静的ファイル

Flask の静的ファイル配信機能により、以下のパスでリソースにアクセスできます。

| パス | 内容 |
|------|------|
| `/static/css/style.css` | スタイルシート |
| `/static/js/timer.js` | タイマー制御 JavaScript |

---

## 備考

- 現時点では JSON を返す REST API エンドポイントは実装されていません。
- タイマーの開始・リセット・状態切替はすべてフロントエンド（`timer.js`）で処理されます。
- サーバー側の `PomodoroTimer` クラス（`timer.py`）は現在 Flask ルートから呼び出されておらず、バックエンド API として公開されていません。
