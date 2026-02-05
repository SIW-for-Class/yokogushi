# python-flask-addition

最小の「足し算」Webアプリ（yokogushiの観察対象）

## 目的（観察ポイント）
- Linux: プロセス/ポート/起動ディレクトリ/ログ
- Web: フォーム(POST) → サーバ処理 → HTML表示
- Python: def / 引数 / 返り値 / 例外処理（入力の扱い）

## 起動
```bash
# 例: 5000番で起動（必要なら変える）
python3 app.py
```
ブラウザ：
http://127.0.0.1:5000/

##よく使う観察
```bash
ss -lntp | grep 5000
ps aux | grep python
