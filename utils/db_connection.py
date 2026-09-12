"""
Centralized database connection handling.
Default: SQLite (DB_PATH below). Swap to Postgres/MySQL by editing get_connection()
and installing the relevant connector (psycopg2 / mysql-connector-python) —
the rest of the app only calls get_connection() and run_query(), so no other
code needs to change.
"""
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "cricbuzz_livestats.db")


def get_connection():
    """Returns a DB connection. Swap this function's body to change database engines."""
    if not os.path.exists(DB_PATH):
        _bootstrap_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _bootstrap_db():
    """First-run only: build schema + seed sample data. Keeps Streamlit Cloud
    deployments working even though its filesystem is ephemeral."""
    import subprocess
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    subprocess.run(
        ["python3" if os.name != "nt" else "python", "generate_sample_data.py"],
        cwd=project_root, check=True,
    )


def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """Run a SELECT query and return results as a DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
    return df


def execute_write(query: str, params: tuple = ()) -> int:
    """Run an INSERT/UPDATE/DELETE. Returns lastrowid (for inserts) or rowcount."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        result = cur.lastrowid if cur.lastrowid else cur.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    return result
