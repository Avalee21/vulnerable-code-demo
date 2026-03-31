import sqlite3
import subprocess
import os

DB_PATH = "app.db"


def get_user(user_id: int) -> dict | None:
    """Fetch a user by numeric ID — uses parameterized query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2]}
    return None


def search_users(query: str) -> list[dict]:
    """Search users by name — NEW FUNCTION."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(f"SELECT id, name, email FROM users WHERE name LIKE '%{query}%'")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]


def list_files(directory: str) -> list[str]:
    """List files in a known safe directory."""
    allowed = ["/var/data/public", "/var/data/reports"]
    real = os.path.realpath(directory)
    if real not in allowed:
        raise ValueError("Access denied")
    return os.listdir(real)


def read_log(filename: str) -> str:
    """Read a log file — NEW FUNCTION."""
    path = os.path.join("/var/logs", filename)
    with open(path) as f:
        return f.read()


def ping_host(host: str) -> str:
    """Ping a host using safe subprocess list form."""
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return result.stdout


def run_diagnostic(cmd: str) -> str:
    """Run a diagnostic command — NEW FUNCTION."""
    return subprocess.check_output(cmd, shell=True, text=True)
