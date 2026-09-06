"""Shaka vulnerability test range -- a small, deliberately vulnerable Flask
app for validating Shaka's own scanners (nuclei, sqlmap, ffuf, trivy,
TruffleHog) and for client demos.

NOT FOR PRODUCTION USE. NOT FOR PUBLIC DEPLOYMENT. Every vulnerability here
is intentional -- run it locally/throwaway only when you need a live HTTP
target (e.g. for --sqlmap or a nuclei/ffuf pass). See README.md for the full
catalogue of what's planted and which Shaka flag exercises it.
"""

import sqlite3

from flask import Flask, request

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, username TEXT, role TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'administrator')")
    conn.execute("INSERT INTO users VALUES (2, 'alice', 'user')")
    conn.execute("INSERT INTO users VALUES (3, 'bob', 'user')")
    return conn


@app.route("/")
def index() -> str:
    return "Shaka vulnerability test range. See /user?id=1 for the planted SQL injection."


@app.route("/user")
def user() -> dict:
    # VULNERABLE (CWE-89): raw string interpolation into a SQL query.
    # Try: /user?id=1 OR 1=1 -- or a real sqlmap/nuclei SQLi pass.
    user_id = request.args.get("id", "1")
    conn = get_db()
    cur = conn.execute(f"SELECT id, username, role FROM users WHERE id = {user_id}")
    rows = cur.fetchall()
    return {"results": rows}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
