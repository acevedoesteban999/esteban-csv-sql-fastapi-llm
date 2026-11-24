from cleaner_uploader.cleaner import clean_rows, _parse_date


def _make_row(**overrides):
    row = {"order_id": "1", "date": "2024-03-15", "customer": "Customer 001",
           "country": "España", "product": "Laptop", "amount": "100.50",
           "status": "completed"}
    row.update(overrides)
    return row


def test_parse_date_formats():
    assert _parse_date("2024-03-15").isoformat() == "2024-03-15"
    assert _parse_date("15/03/2024").isoformat() == "2024-03-15"
    assert _parse_date("2024-13-45") is None
    assert _parse_date("yesterday") is None


def test_clean_rows_removes_errors():
    rows = [
        _make_row(order_id="1"),
        _make_row(order_id="1"),                      # duplicate
        _make_row(order_id="2", date="32/01/2024"),   # invalid date
        _make_row(order_id="3", amount=""),           # empty amount
        _make_row(order_id="4", status=" PENDING "),  # normalized
    ]
    clean, stats = clean_rows(rows)

    assert [r["order_id"] for r in clean] == [1, 4]
    assert clean[1]["status"] == "pending"
    assert stats == {"input": 5, "duplicates": 1, "invalid_date": 1,
                     "invalid_amount": 1, "output": 2}