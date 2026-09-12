import sqlite3
import os
import sys
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
    deployments working even though its filesystem is ephemeral. Calls the
    seeder in-process (not via subprocess) so it works reliably regardless
    of the host's PATH/sandboxing."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    import generate_sample_data
    generate_sample_data.main()


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