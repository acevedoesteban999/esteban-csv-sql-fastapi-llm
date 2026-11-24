import re

from config import ALLOWED_TABLES

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|pragma|vacuum)\b",
    re.IGNORECASE,
)
TABLE_REFERENCE = re.compile(r"\b(?:from|join)\s+([a-z_][a-z0-9_]*)", re.IGNORECASE)


class InvalidQueryError(Exception):
    pass


def validate_sql(sql: str) -> str:
    sql = sql.strip().rstrip(";").strip()

    if not sql:
        raise InvalidQueryError("Empty query")
    if ";" in sql:
        raise InvalidQueryError("Only one statement is allowed")
    if not re.match(r"select\b", sql, re.IGNORECASE):
        raise InvalidQueryError("Only SELECT queries are allowed")
    if FORBIDDEN_KEYWORDS.search(sql):
        raise InvalidQueryError("Query contains forbidden keywords")

    tables = {t.lower() for t in TABLE_REFERENCE.findall(sql)}
    if not tables:
        raise InvalidQueryError("Query must read from an allowed table")
    not_allowed = tables - ALLOWED_TABLES
    if not_allowed:
        raise InvalidQueryError(f"Tables not allowed: {', '.join(sorted(not_allowed))}")

    return sql