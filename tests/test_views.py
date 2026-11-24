import sqlite3
from cleaner_uploader.uploader import create_views, upload_to_sqlite


def _order(order_id, date, customer, country, amount, status="completed"):
    return {"order_id": order_id, "order_date": date, "customer": customer,
            "country": country, "product": "Laptop", "amount": amount,
            "status": status}

def _setup_db(tmp_path, rows):
    db_path = tmp_path / "test.db"
    upload_to_sqlite(rows, db_path)
    create_views(db_path)
    return db_path

def test_views_created(tmp_path):
    db_path = _setup_db(tmp_path, [])

    with sqlite3.connect(db_path) as conn:
        views = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'view' ORDER BY name"
        ).fetchall()
    assert views == [("sales_by_month_country",), ("top_10_customers",)]

def test_sales_month_country(tmp_path):
    db_path = _setup_db(tmp_path, [
        _order(1, "2024-03-01", "Customer 001", "España", 100.0),
        _order(2, "2024-03-20", "Customer 002", "España", 50.0),
        _order(3, "2024-03-10", "Customer 003", "España", 999.0, status="cancelled"),
        _order(4, "2024-04-05", "Customer 001", "Chile", 30.0),
    ])

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT month, country, orders, total_sales FROM sales_by_month_country "
            "ORDER BY month, country"
        ).fetchall()

    assert rows == [
        ("2024-03", "España", 2, 150.0),
        ("2024-04", "Chile", 1, 30.0),
    ]


def test_top_10_customers(tmp_path):
    rows = [_order(i, "2024-01-01", f"Customer {i:03d}", "España", float(i))
            for i in range(1, 13)]  
    db_path = _setup_db(tmp_path, rows)

    with sqlite3.connect(db_path) as conn:
        top = conn.execute("SELECT customer, total_spent FROM top_10_customers").fetchall()

    assert len(top) == 10
    assert top[0] == ("Customer 012", 12.0)
    assert top[-1] == ("Customer 003", 3.0)