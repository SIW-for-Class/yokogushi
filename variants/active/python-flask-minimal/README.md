# Mini Support Desk（最小プロトタイプ）

目的：完成ではなく「読む・壊す・直す・説明する」教材にする。

## 機能
- 投稿（title/body/category/priority）
- 一覧（検索/ステータス絞り込み）
- 詳細
- open/closed の切替（最小API + JS fetch）

## 動かし方
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# mac/linux:
# source .venv/bin/activate

pip install flask
python app.py

