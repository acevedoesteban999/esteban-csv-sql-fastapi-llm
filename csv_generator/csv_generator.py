import csv
import random
from datetime import date, timedelta
from pathlib import Path

OUTPUT = Path(__file__).parent / "csv.csv"
HEADER = ["order_id", "date", "customer", "country", "product", "amount", "status"]

CUSTOMERS = [f"Customer {i:03d}" for i in range(1, 151)]
COUNTRIES = ["España", "México", "Argentina", "Colombia", "Chile", "Perú"]
PRODUCTS = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam"]
STATUSES = ["completed", "pending", "cancelled", "returned"]
INVALID_DATES = ["2024-13-45", "32/01/2024", "may 2024", "2024/02/30", "yesterday", "test", "test-wrong-data"]


def generate_orders(n=1000, seed=42, n_duplicates=30, error_rate=0.05):
    rnd = random.Random(seed)
    start = date(2024, 1, 1)
    rows = []
    for i in range(1, n + 1):
        order_date = (start + timedelta(days=rnd.randint(0, 364))).isoformat()
        amount = f"{rnd.uniform(5, 2000):.2f}"
        if rnd.random() < error_rate:
            order_date = rnd.choice(INVALID_DATES)
        if rnd.random() < error_rate:
            amount = ""
        rows.append([
            i,
            order_date,
            rnd.choice(CUSTOMERS),
            rnd.choice(COUNTRIES),
            rnd.choice(PRODUCTS),
            amount,
            rnd.choice(STATUSES),
        ])
    rows += rnd.sample(rows, n_duplicates)
    rnd.shuffle(rows)
    return rows


def write_csv(rows, path=OUTPUT):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    path = write_csv(generate_orders())
    print(f"CSV generated at {path}")