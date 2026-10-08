import sqlite3
from datetime import datetime

from config import DB_NAME


def connect():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    conn = connect()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS whitelist (name TEXT PRIMARY KEY, added_at TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, pid INTEGER, name TEXT, exe TEXT, rule TEXT, weight INTEGER, score INTEGER)"
    )
    conn.commit()
    conn.close()


def is_whitelisted(name):
    if name is None:
        return False

    name = str(name).strip().lower()
    if name == "":
        return False

    conn = connect()
    row = conn.execute(
        "SELECT 1 FROM whitelist WHERE name = ?",
        (name,),
    ).fetchone()
    conn.close()

    if row is None:
        return False
    return True


def add_to_whitelist(name):
    if name is None:
        return

    name = str(name).strip().lower()
    if name == "":
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = connect()
    conn.execute(
        "INSERT OR REPLACE INTO whitelist (name, added_at) VALUES (?, ?)",
        (name, now),
    )
    conn.commit()
    conn.close()


def remove_from_whitelist(name):
    if name is None:
        return

    name = str(name).strip().lower()
    if name == "":
        return

    conn = connect()
    conn.execute("DELETE FROM whitelist WHERE name = ?", (name,))
    conn.commit()
    conn.close()


def log_event(pid, name, exe, rule, weight, score, ts=None):
    if ts is None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = connect()
    conn.execute(
        "INSERT INTO events (ts, pid, name, exe, rule, weight, score) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ts, pid, name, exe, rule, weight, score),
    )
    conn.commit()
    conn.close()
