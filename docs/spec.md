# spec.md
## Yokogushi（ナレッジスペースアプリ）共通仕様

本ファイルは、複数言語・複数実装（variants）で **同一の学習対象** を作るための、言語非依存の仕様を定義する。  
実装は `variants/active` および `variants/extensions` に置く。完成度や本番運用は目的としない。

---

## 1. 目的（教育用途）
- HTML/CSS/JS/Python/DB/Linux（および他言語）を **1つのシステムとして観察**する
- 「動くもの」を早く用意し、**読む・壊す・直す・説明する** を促す
- 同一仕様の多実装により、設計思想・責務分割・言語特性の差を比較する

---

## 2. 用語
- **エントリ（Entry）**：知識の最小単位（質問・メモ・手順・トラブル記録等）
- **ステータス（Status）**：`open` / `closed`
  - open：未整理・対応中・追加情報待ち
  - closed：解決済み・整理済み
- **実装（Variant）**：同一仕様を別言語・別スタックで実現したもの

---

## 3. 対象範囲（MVP）
### 必須（MUST）
- エントリの作成（title, body）
- エントリの一覧表示
- エントリの詳細表示
- ステータスの切替（open/closed）

### 任意（SHOULD / MAY）
- 簡易検索（タイトル/本文の部分一致）
- タグ（文字列の配列/カンマ区切り）
- 更新日時の表示
- JSON API（後述）

---

## 4. データモデル（共通）
### 4.1 entries
| フィールド | 型（概念） | 必須 | 説明 |
|---|---:|:---:|---|
| id | integer / uuid | ✓ | 一意ID |
| title | text | ✓ | タイトル |
| body | text | ✓ | 本文（markdownは任意） |
| status | text | ✓ | `open` or `closed` |
| created_at | datetime | ✓ | 作成日時 |
| updated_at | datetime | ✓ | 更新日時 |

- 初期値：`status=open`
- `updated_at` は status 切替や本文更新で更新される（実装により省略可）

---

## 5. 画面（SSR前提の最小）
※ UI/見た目は自由。重要なのは **機能が観察できること**。

### 5.1 一覧（List）
- URL例：`/` または `/entries`
- 表示要素：
  - title
  - status
  - created_at（任意）
- 操作：
  - 新規作成への導線
  - 詳細へのリンク

### 5.2 詳細（Detail）
- URL例：`/entries/{id}`
- 表示要素：
  - title, body, status
- 操作：
  - status 切替（open ↔ closed）
  - 一覧へ戻る導線

### 5.3 新規作成（Create）
- URL例：`/entries/new`（フォーム表示）
- 送信先：
  - `POST /entries`
- 入力：
  - title（必須）
  - body（必須）

---

## 6. ルーティング（HTTP）
以下は推奨。実装言語の都合で変更してよいが、**同じ役割のURL**を保つこと。

- `GET  /` or `GET /entries`：一覧
- `GET  /entries/new`：新規フォーム
- `POST /entries`：作成
- `GET  /entries/{id}`：詳細
- `POST /entries/{id}/status`：ステータス切替  
  - bodyに `status=open|closed` を含めてもよい  
  - もしくはトグル専用でもよい

---

## 7. JSON API（任意 / 比較用）
SSRだけでもよいが、横串として「APIの存在」を見せたい場合に追加する。

- `GET  /api/entries`：一覧（JSON）
- `GET  /api/entries/{id}`：詳細（JSON）
- `POST /api/entries`：作成（JSON）
- `PATCH /api/entries/{id}`：更新（JSON）
- `PATCH /api/entries/{id}/status`：ステータス更新（JSON）

### JSON例（entries）
```json
{
  "id": 1,
  "title": "dnf update が遅い",
  "body": "症状…観察…仮説…確認…",
  "status": "open",
  "created_at": "2026-02-06T09:00:00+09:00",
  "updated_at": "2026-02-06T09:10:00+09:00"
}
```

---

## 8. 永続化（DB）

- 推奨：SQLite（MVP）
- 許容：ファイル（JSON/CSV）※PurePython最小で採用可
- 重要：状態が残ること（再起動しても一覧に残る）

---

## 9. 観察ポイント（教育用の非機能要求）

実装は以下の観察ができるよう、ログや出力を工夫してよい。

- HTTP：メソッド、パス、ステータスコード
- DB：INSERT/SELECT/UPDATE がどこで起きるか
- Linux：プロセス、ポート、ログ出力（標準出力でも良い）
- エラー：入力不足などの扱い（400/バリデーション表示等）

---

## 10. 非目標（やらないこと）

- 認証・認可（ログイン等）
- 本番運用のセキュリティ対策（CSRF/Rate limit 等）
- 高度な最適化・パフォーマンス設計
- 完璧なUI/UX

本プロジェクトは教材であり、未完成さ・改善余地を意図的に残す。

---

## 11. バリアント運用ルール（簡易）

- variants/active：授業で扱う実装（最大1〜2個）
- variants/extensions：発展・比較用（任意）

各実装は以下を必ず含める：

- README.md（狙い／観察ポイント／起動方法）
- src/（実装）
- 必要なら templates/ static/ scripts/

8. 永続化（DB）

推奨：SQLite（MVP）

許容：ファイル（JSON/CSV）※PurePython最小で採用可

重要：状態が残ること（再起動しても一覧に残る）

9. 観察ポイント（教育用の非機能要求）

実装は以下の観察ができるよう、ログや出力を工夫してよい。

HTTP：メソッド、パス、ステータスコード

DB：INSERT/SELECT/UPDATE がどこで起きるか

Linux：プロセス、ポート、ログ出力（標準出力でも良い）

エラー：入力不足などの扱い（400/バリデーション表示等）

10. 非目標（やらないこと）

認証・認可（ログイン等）

本番運用のセキュリティ対策（CSRF/Rate limit 等）

高度な最適化・パフォーマンス設計

完璧なUI/UX

本プロジェクトは 教材であり、未完成さ・改善余地を意図的に残す。

11. バリアント運用ルール（簡易）

variants/active：授業で扱う実装（最大1〜2個）

variants/extensions：発展・比較用（任意）

各実装は以下を必ず含める：

README.md（狙い／観察ポイント／起動方法）

src/（実装）

必要なら templates/ static/ scripts/