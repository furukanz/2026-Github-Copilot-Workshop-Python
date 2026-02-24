# フロントエンドドキュメント

## 概要

フロントエンドはバニラ JavaScript・HTML・CSS で構成されており、サーバーとの通信を行わずブラウザ内でタイマーのすべての制御を完結させます。

---

## HTMLテンプレート

**ファイル:** `1.pomodoro/templates/index.html`

Flask の `render_template` によって `/` ルートで配信されます。

### 主要要素

| 要素 ID / クラス | タグ | 説明 |
|----------------|------|------|
| `#minutes` | `<span>` | 残り時間の「分」部分を表示 |
| `#seconds` | `<span>` | 残り時間の「秒」部分を表示 |
| `#start` | `<button>` | タイマー開始ボタン |
| `#reset` | `<button>` | タイマーリセットボタン |
| `#state` | `<div>` | 現在の状態テキスト（「作業中」または「休憩中」）を表示 |
| `.container` | `<div>` | ページ全体のカードコンテナ |
| `.buttons` | `<div>` | ボタングループ |

---

## JavaScript モジュール

**ファイル:** `1.pomodoro/static/js/timer.js`

### グローバル変数

| 変数名 | 初期値 | 説明 |
|--------|--------|------|
| `workSeconds` | `25 * 60` | 作業時間（秒） |
| `breakSeconds` | `5 * 60` | 休憩時間（秒） |
| `state` | `'work'` | 現在の状態（`'work'` または `'break'`） |
| `remaining` | `workSeconds` | 残り時間（秒） |
| `timerInterval` | `null` | `setInterval` の識別子 |

### 関数

#### `updateDisplay()`

`remaining` と `state` の値をもとに、HTML 要素の表示を更新します。

- `#minutes` に残り分（2桁ゼロ埋め）を設定
- `#seconds` に残り秒（2桁ゼロ埋め）を設定
- `#state` に `'work'` → `'作業中'`、`'break'` → `'休憩中'` を設定

#### `tick()`

1秒ごとに呼び出されるコールバック関数（`setInterval` で登録）。

- `remaining > 0` の場合: `remaining` を 1 減算し `updateDisplay()` を呼び出す
- `remaining == 0` の場合:
  - `clearInterval(timerInterval)` でタイマーを停止
  - 状態を切り替え（`'work'` ↔ `'break'`）、対応する残り時間を設定
  - `alert()` でユーザーに通知
  - `updateDisplay()` を呼び出す

### イベントリスナー

#### `#start` ボタンクリック

`timerInterval` が `null`（タイマー未起動）の場合のみ `setInterval(tick, 1000)` を呼び出してタイマーを開始します。すでに起動中の場合は何もしません（一時停止機能はありません）。

```javascript
document.getElementById('start').addEventListener('click', function() {
    if (!timerInterval) {
        timerInterval = setInterval(tick, 1000);
    }
});
```

#### `#reset` ボタンクリック

タイマーを停止し、状態を作業時間の初期値に戻します。

```javascript
document.getElementById('reset').addEventListener('click', function() {
    clearInterval(timerInterval);
    timerInterval = null;
    state = 'work';
    remaining = workSeconds;
    updateDisplay();
});
```

### 初期化

スクリプト読み込み時に `updateDisplay()` を呼び出し、初期表示（`25:00`・`作業中`）を設定します。

---

## スタイルシート

**ファイル:** `1.pomodoro/static/css/style.css`

### レイアウト

- `body`: Flexbox で画面中央にコンテンツを配置（`justify-content: center; align-items: center; height: 100vh`）

### 主要スタイル

| セレクタ | 概要 |
|---------|------|
| `body` | 背景色 `#f5f5f5`、フォント Arial |
| `.container` | 白背景、`padding: 32px`、角丸（`border-radius: 8px`）、ドロップシャドウ |
| `#timer` | フォントサイズ `48px`、上下マージン `16px` |
| `.buttons button` | 背景色 `#4caf50`（緑）、白文字、角丸、ホバー時 `#388e3c` |
| `#state` | フォントサイズ `18px`、色 `#333` |

---

## 動作フロー

```
ページロード
  │
  ▼
updateDisplay() → 「25:00 / 作業中」表示
  │
  │  [開始ボタン]
  ▼
setInterval(tick, 1000) 開始
  │
  │  tick() 毎秒実行
  │  remaining-- → updateDisplay()
  │
  │  remaining == 0
  ▼
アラート表示 → 状態切替 → updateDisplay()
  │
  │  [リセットボタン]
  ▼
タイマー停止 → state='work', remaining=workSeconds → updateDisplay()
```
