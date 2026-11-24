from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]


def _parse_date(value):
    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _parse_amount(value):
    try:
        amount = float(value.strip())
    except ValueError:
        return None
    return amount if amount >= 0 else None


def clean_rows(rows):
    clean = []
    seen_ids = set()
    stats = {"duplicates": 0, "invalid_date": 0, "invalid_amount": 0}

    for row in rows:
        order_id = int(row["order_id"])
        if order_id in seen_ids:
            stats["duplicates"] += 1
            continue
        seen_ids.add(order_id)

        order_date = _parse_date(row["date"])
        if order_date is None:
            stats["invalid_date"] += 1
            continue

        amount = _parse_amount(row["amount"])
        if amount is None:
            stats["invalid_amount"] += 1
            continue

        clean.append({
            "order_id": order_id,
            "order_date": order_date.isoformat(),
            "customer": row["customer"].strip(),
            "country": row["country"].strip(),
            "product": row["product"].strip(),
            "amount": round(amount, 2),
            "status": row["status"].strip().lower(),
        })

    return clean, stats