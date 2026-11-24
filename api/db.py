import sqlite3

from config import DB_PATH


def run_query(sql: str, db_path=DB_PATH) -> list[dict]:
    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(sql).fetchall()]