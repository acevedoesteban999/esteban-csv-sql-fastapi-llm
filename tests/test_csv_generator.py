import csv
from datetime import date

from csv_generator.csv_generator import HEADER, generate_orders, write_csv


def _read_rows(tmp_path):
    path = write_csv(generate_orders(), tmp_path / "test.csv")
    with open(path, encoding="utf-8") as f:
        return list(csv.reader(f))


def _is_valid_date(value):
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def test_header_len(tmp_path):
    rows = _read_rows(tmp_path)
    assert rows[0] == HEADER
    assert len(rows) - 1 >= 1000


def test_errors(tmp_path):
    data = _read_rows(tmp_path)[1:]
    as_tuples = [tuple(r) for r in data]
    assert len(as_tuples) > len(set(as_tuples)), "should contain duplicates"
    assert any(r[5] == "" for r in data), "should contain empty amounts"
    assert any(not _is_valid_date(r[1]) for r in data), "should contain invalid dates"