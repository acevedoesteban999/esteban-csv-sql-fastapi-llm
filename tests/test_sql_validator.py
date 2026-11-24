from api.sql_validator import InvalidQueryError,validate_sql
import pytest

def test_valid_select_passes():
    sql = "SELECT total_sales FROM sales_by_month_country WHERE country = 'España';"
    assert validate_sql(sql) == "SELECT total_sales FROM sales_by_month_country WHERE country = 'España'"

def test_select_with_not_allowed_table_is_rejected():
    sql = "SELECT * FROM orders JOIN secrets ON orders.order_id = secrets.id"
    with pytest.raises(InvalidQueryError, match="Tables not allowed: secrets"):
        validate_sql(sql)