
# ## `variants/active/python-flask-addition/app.py`

from flask import Flask, render_template, request

app = Flask(__name__)

def parse_int(s: str):
    """空文字や数値以外を弾き、エラーメッセージを返す。"""
    if s is None or s.strip() == "":
        return None, "空欄です"
    try:
        return int(s), None
    except ValueError:
        return None, f"整数に変換できません: {s!r}"

@app.get("/")
def index_get():
    # 初期表示：空のフォーム
    return render_template("index.html", a="", b="", result=None, error=None)

@app.post("/")
def index_post():
    a_raw = request.form.get("a", "")
    b_raw = request.form.get("b", "")

    a, err_a = parse_int(a_raw)
    b, err_b = parse_int(b_raw)

    if err_a or err_b:
        # どこがダメかをまとめて表示
        msgs = [m for m in [err_a, err_b] if m]
        return render_template(
            "index.html",
            a=a_raw,
            b=b_raw,
            result=None,
            error=" / ".join(msgs),
        )

    result = a + b
    return render_template("index.html", a=a_raw, b=b_raw, result=result, error=None)

if __name__ == "__main__":
    # VirtualBoxなどでホストから叩くなら 0.0.0.0
    # ローカルのみなら 127.0.0.1
    app.run(host="0.0.0.0", port=5000, debug=False)

