import json
import os
import sqlite3

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs.db")


def _conn():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, api TEXT, passed INTEGER, failed INTEGER,
        error_rate REAL, availability REAL,
        latency_avg INTEGER, latency_p95 INTEGER, details TEXT)""")
    return c


def save_run(run):
    s = run["summary"]
    with _conn() as c:
        c.execute("""INSERT INTO runs (timestamp, api, passed, failed, error_rate,
                     availability, latency_avg, latency_p95, details)
                     VALUES (?,?,?,?,?,?,?,?,?)""",
                  (run["timestamp"], run["api"], s["passed"], s["failed"],
                   s["error_rate"], s["availability"], s["latency_ms_avg"],
                   s["latency_ms_p95"], json.dumps(run["tests"])))


def list_runs(limit=50):
    c = _conn()
    c.row_factory = sqlite3.Row
    rows = [dict(r) for r in c.execute(
        "SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))]
    c.close()
    for r in rows:
        r["details"] = json.loads(r["details"])
    return rows
