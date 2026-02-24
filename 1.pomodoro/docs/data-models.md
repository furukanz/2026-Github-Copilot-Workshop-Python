# データモデル

## 概要

ポモドーロタイマーのビジネスロジックは `1.pomodoro/timer.py` の `PomodoroTimer` クラスで定義されています。

---

## PomodoroTimer クラス

**ファイル:** `1.pomodoro/timer.py`

### コンストラクタ

```python
PomodoroTimer(work_minutes=25, break_minutes=5)
```

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `work_minutes` | `float` | `25` | 作業時間（分） |
| `break_minutes` | `float` | `5` | 休憩時間（分） |

### 属性

| 属性 | 型 | 説明 |
|------|----|------|
| `work_seconds` | `float` | 作業時間を秒に変換した値（`work_minutes * 60`） |
| `break_seconds` | `float` | 休憩時間を秒に変換した値（`break_minutes * 60`） |
| `state` | `str` | 現在の状態。`'work'`（作業中）または `'break'`（休憩中） |
| `remaining` | `float` | 残り時間（秒）。初期値は `work_seconds` |
| `running` | `bool` | タイマーが動作中かどうか。初期値は `False` |

### メソッド

#### `start()`

タイマーを開始します。`running` を `True` に設定し、`state` を `'work'`、`remaining` を `work_seconds` にリセットします。

```python
timer = PomodoroTimer()
timer.start()
# timer.running == True
# timer.state == 'work'
```

#### `tick()`

タイマーが動作中（`running == True`）かつ残り時間がある場合、`remaining` を 1 減算します。残り時間を返します。

```python
timer.tick()  # remaining が 1 減少（running=True の場合）
```

#### `switch()`

作業と休憩の状態を切り替え、対応する残り時間を設定します。

| 現在の `state` | 切替後の `state` | `remaining` の設定値 |
|---------------|-----------------|-------------------|
| `'work'` | `'break'` | `break_seconds` |
| `'break'` | `'work'` | `work_seconds` |

#### `reset()`

現在の状態に応じた初期時間に `remaining` をリセットし、`running` を `False` に設定します。

```python
timer.reset()
# timer.running == False
# timer.remaining == work_seconds（state=='work'の場合）
```

#### `is_finished()`

`remaining == 0` の場合に `True` を返します。

```python
if timer.is_finished():
    timer.switch()  # 次のフェーズへ
```

---

## 状態遷移図

```
初期化
  │
  ▼
[running=False, state='work']
  │  start()
  ▼
[running=True, state='work']
  │  tick() × N → remaining=0
  │  switch()
  ▼
[running=True, state='break']
  │  tick() × N → remaining=0
  │  switch()
  ▼
[running=True, state='work']  ← 繰り返し
  │  reset()
  ▼
[running=False, remaining=初期値]
```
