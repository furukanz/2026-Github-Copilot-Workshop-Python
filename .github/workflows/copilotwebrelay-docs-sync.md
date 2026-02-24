---
description: Detect changes under 2.copilotWebRelay/ and update documentation to keep docs aligned with source code
on:
  push:
    branches: [main]
    paths:
      - "2.copilotWebRelay/**"
      - "!2.copilotWebRelay/docs/**"
  pull_request:
    types: [opened, reopened, synchronize]
    paths:
      - "2.copilotWebRelay/**"
      - "!2.copilotWebRelay/docs/**"
  workflow_dispatch:
permissions:
  contents: read
  pull-requests: read
  issues: read
tools:
  github:
safe-outputs:
  push-to-pull-request-branch:
  create-pull-request:
    title-prefix: "docs(copilotWebRelay): "
    labels: [documentation]
    draft: true
---

# Copilot Web Relay Documentation Sync

あなたは `2.copilotWebRelay/` 配下のソースコードと、`2.copilotWebRelay/docs/` 配下のドキュメントが常に一致するように保守する AI エージェントです。

## 目的

`2.copilotWebRelay/` 配下の変更が入ったときに、現在の実装内容に合わせてドキュメントを更新し、差分を **Pull Request** として提案してください。

## 作業手順

1. `2.copilotWebRelay/` 配下の **現時点のソースコード**（存在する範囲で）を読み、機能・構成・入出力・プロトコルを把握する。
   - 例: `backend/`（FastAPI / WebSocket / CLI ブリッジ）、`frontend/`（React/Vite）、`e2e/`（Playwright）など
2. 既存の `2.copilotWebRelay/docs/` 配下ドキュメント（存在すれば）を読み、実装との差分を洗い出す。
3. 参考として `2.copilotWebRelay/planning.md` を読み、設計意図と現実装のズレを把握する（ただし **コードに存在しない仕様はドキュメントに断定して書かない**）。
4. `2.copilotWebRelay/docs/` 配下を更新・作成する（必要最小限で可）。
   - 推奨ファイル（必要に応じて増減してよい）
     - `2.copilotWebRelay/docs/overview.md`：現状の概要と起動/利用の最短手順
     - `2.copilotWebRelay/docs/architecture.md`：構成（Frontend/Backend/CLI Bridge）と責務
     - `2.copilotWebRelay/docs/websocket-protocol.md`：メッセージ形式・状態遷移・エラーハンドリング
     - `2.copilotWebRelay/docs/frontend.md`：主要コンポーネント/状態管理/UI 仕様
     - `2.copilotWebRelay/docs/backend.md`：主要モジュール、WebSocket ハンドラ、プロセス管理
5. 更新差分がある場合、トリガーに応じて safe output を使って反映する。
  - **pull_request トリガーの場合**: `push-to-pull-request-branch` を使い、docs 更新コミットを **同じ PR ブランチ** に push する（この PR 内で docs が追従する状態にする）。
  - **push（main）/手動実行の場合**: `create-pull-request` を使い、docs 更新のための **ドラフト PR** を作成する。
    - タイトル: `docs(copilotWebRelay): sync documentation with latest code changes`
    - 本文: 何を更新したか（どの docs を、どの実装変更に追従したか）を簡潔に列挙する
6. 差分がなく、ドキュメントが最新である場合は `noop` を呼び、理由（変更不要）を 1〜2 文で説明する。

## ガイドライン

- ドキュメントは日本語で書く。
- **事実ベース**（実装に根拠があることのみ）で記述する。
- ソースコードは変更しない（`2.copilotWebRelay/docs/` 配下のみ変更する）。
- 例（JSON/コマンド/通信例）があると理解が進む場合は、必要最小限の例を付ける。
