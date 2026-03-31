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


def list_files(directory: str) -> list[str]:
    """List files in a known safe directory."""
    allowed = ["/var/data/public", "/var/data/reports"]
    real = os.path.realpath(directory)
    if real not in allowed:
        raise ValueError("Access denied")
    return os.listdir(real)


def ping_host(host: str) -> str:
    """Ping a host using safe subprocess list form."""
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return result.stdout
