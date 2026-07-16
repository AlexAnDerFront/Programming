"""
sqlite3 helpers. Uses pandas' to_sql/read_sql for convenience since
we're already working with DataFrames elsewhere in the pipeline.
"""
import sqlite3
import os
import pandas as pd


def get_connection(db_path: str) -> sqlite3.Connection:
    """Open (and implicitly create) a sqlite connection."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def init_db(db_path: str) -> None:
    """
    Create the database file and any baseline tables if they don't exist yet.
    Safe to call every time the app starts.
    """
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def save_dataframe(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> None:
    """Append a DataFrame's rows into the given table."""
    df.to_sql(table_name, conn, if_exists="append", index=False)


def read_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    """Read an entire table back into a DataFrame."""
    return pd.read_sql(f"SELECT * FROM {table_name}", conn)