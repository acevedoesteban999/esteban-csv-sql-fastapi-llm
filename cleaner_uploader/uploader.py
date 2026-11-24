import csv
import sqlite3

from cleaner_uploader.cleaner import clean_rows
from config import CSV_PATH, DB_PATH

CREATE_ORDERS = """
    CREATE TABLE orders (
        order_id   INTEGER PRIMARY KEY,
        order_date TEXT    NOT NULL,
        customer   TEXT    NOT NULL,
        country    TEXT    NOT NULL,
        product    TEXT    NOT NULL,
        amount     REAL    NOT NULL CHECK (amount >= 0),
        status     TEXT    NOT NULL
    )
"""

INSERT_ORDER = """
    INSERT INTO orders VALUES
    (:order_id, :order_date, :customer, :country, :product, :amount, :status)
"""


def read_csv(csv_path=CSV_PATH):
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    with open(csv_path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def upload_to_sqlite(rows, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS orders")
        conn.execute(CREATE_ORDERS)
        conn.executemany(INSERT_ORDER, rows)
    return db_path


def main(csv_path=CSV_PATH, db_path=DB_PATH):
    raw_rows = read_csv(csv_path)
    clean, _ = clean_rows(raw_rows)
    upload_to_sqlite(clean, db_path)
    print(f"Uploaded to {db_path}")


if __name__ == "__main__":
    main()