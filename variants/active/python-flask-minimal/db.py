import os
import sqlite3
from flask import g

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

def get_db():
    # Flaskのリクエストごとに接続を使い回す
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    # app.dbが無ければ schema.sql で作成
    if os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

