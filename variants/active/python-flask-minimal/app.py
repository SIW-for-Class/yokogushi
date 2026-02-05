from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from db import get_db, init_db

app = Flask(__name__)

@app.get("/")
def index():
    db = get_db()
    rows = db.execute(
        "SELECT id, title, status, created_at FROM tickets ORDER BY id DESC LIMIT 3"
    ).fetchall()
    return render_template("index.html", recent=rows)

@app.get("/new")
def new_ticket():
    return render_template("new.html")

@app.post("/new")
def create_ticket():
    title = (request.form.get("title") or "").strip()
    body = (request.form.get("body") or "").strip()
    category = (request.form.get("category") or "general").strip()
    priority = (request.form.get("priority") or "normal").strip()

    # 教材として分かりやすく：最低限のバリデーションのみ
    errors = []
    if not title:
        errors.append("タイトルは必須です。")
    if len(title) > 80:
        errors.append("タイトルは80文字以内にしてください。")
    if len(body) > 2000:
        errors.append("本文は2000文字以内にしてください。")

    if errors:
        return render_template("new.html", errors=errors, form=request.form), 400

    db = get_db()
    db.execute(
        "INSERT INTO tickets(title, body, category, priority, status) VALUES(?,?,?,?,?)",
        (title, body, category, priority, "open"),
    )
    db.commit()
    return redirect(url_for("tickets"))

@app.get("/tickets")
def tickets():
    q = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "all").strip()

    where = []
    params = []

    if q:
        where.append("(title LIKE ? OR body LIKE ?)")
        like = f"%{q}%"
        params.extend([like, like])

    if status in ("open", "closed"):
        where.append("status = ?")
        params.append(status)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    db = get_db()
    rows = db.execute(
        f"""
        SELECT id, title, category, priority, status, created_at
        FROM tickets
        {where_sql}
        ORDER BY id DESC
        """,
        params,
    ).fetchall()

    return render_template("tickets.html", rows=rows, q=q, status=status)

@app.get("/tickets/<int:ticket_id>")
def ticket_detail(ticket_id: int):
    db = get_db()
    row = db.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,),
    ).fetchone()
    if row is None:
        abort(404)
    return render_template("ticket_detail.html", t=row)

# JSから叩く最小API：open/closed切替
@app.post("/api/tickets/<int:ticket_id>/toggle")
def api_toggle(ticket_id: int):
    db = get_db()
    row = db.execute("SELECT status FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if row is None:
        return jsonify({"ok": False, "error": "not_found"}), 404

    new_status = "closed" if row["status"] == "open" else "open"
    db.execute("UPDATE tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
    db.commit()
    return jsonify({"ok": True, "id": ticket_id, "status": new_status})

@app.cli.command("init-db")
def init_db_command():
    """flask init-db でDB初期化できるようにする"""
    init_db()
    print("Initialized the database.")

if __name__ == "__main__":
    # 初回起動でDBが無ければ作る（教材用に親切に）
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)


