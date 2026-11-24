from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "csv_generator" / "csv.csv"
DB_PATH = ROOT / "orders.db"
VIEWS_SQL_PATH = ROOT / "sql" / "views.sql"
ALLOWED_TABLES = {"orders", "sales_by_month_country", "top_10_customers"}