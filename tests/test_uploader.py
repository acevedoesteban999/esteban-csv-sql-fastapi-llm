import sqlite3
from cleaner_uploader.uploader import main, read_csv

def test_main_uploads_clean_rows(tmp_path):
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text(
        "order_id,date,customer,country,product,amount,status\n"
        "1,2024-03-15,Customer 001,España,Laptop,100.50,completed\n"
        "1,2024-03-15,Customer 001,España,Laptop,100.50,completed\n"
        "2,yesterday,Customer 002,Chile,Mouse,20,pending\n"
        "3,2024-03-16,Customer 003,Perú,Webcam,,pending\n",
        encoding="utf-8",
    )
    db_path = tmp_path / "test.db"

    main(csv_path, db_path)

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT order_id, amount FROM orders").fetchall()
    assert rows == [(1, 100.5)]


def test_main_not_duplicate(tmp_path):
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text(
        "order_id,date,customer,country,product,amount,status\n"
        "1,2024-03-15,Customer 001,España,Laptop,100.50,completed\n",
        encoding="utf-8",
    )
    db_path = tmp_path / "test.db"

    main(csv_path, db_path)
    main(csv_path, db_path)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert count == 1