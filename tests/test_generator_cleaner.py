from csv_generator.csv_generator import HEADER, INVALID_DATES, generate_orders
from cleaner_uploader.cleaner import clean_rows

N_ORDERS = 100
N_DUPLICATES = 10


def _generate_as_csv_dicts():
    rows = generate_orders(n=N_ORDERS, seed=42, n_duplicates=N_DUPLICATES, error_rate=0.2)
    # simulate what csv.DictReader returns: dicts with string values
    return [dict(zip(HEADER, map(str, row))) for row in rows]


def _expected_stats(rows):
    unique = {r["order_id"]: r for r in rows}.values()
    invalid_date = [r for r in unique if r["date"] in INVALID_DATES]
    invalid_amount = [r for r in unique
                      if r["date"] not in INVALID_DATES and r["amount"] == ""]
    return {
        "duplicates": len(rows) - len(unique),
        "invalid_date": len(invalid_date),
        "invalid_amount": len(invalid_amount),
    }


def test_cleaner_all_generated_errors():
    rows = _generate_as_csv_dicts()
    clean, stats = clean_rows(rows)
    expected = _expected_stats(rows)

    # sanity check: the sample really contains every kind of error
    assert expected["duplicates"] == N_DUPLICATES
    assert expected["invalid_date"] > 0
    assert expected["invalid_amount"] > 0

    assert stats == expected


def test_clean_output_no_errors():
    clean, _ = clean_rows(_generate_as_csv_dicts())

    ids = [r["order_id"] for r in clean]
    assert len(ids) == len(set(ids)), "no duplicates left"
    assert all(r["amount"] >= 0 for r in clean), "every amount is valid"
    assert all(r["order_date"] not in INVALID_DATES for r in clean), "no invalid dates left"