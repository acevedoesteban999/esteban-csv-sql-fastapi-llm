import os
import re

from openai import OpenAI, OpenAIError

SYSTEM_PROMPT = """You translate business questions (usually in Spanish) into a single SQLite SELECT query.

Database schema:
- orders(order_id INTEGER, order_date TEXT 'YYYY-MM-DD', customer TEXT, country TEXT,
         product TEXT, amount REAL, status TEXT)
  status values: 'completed', 'pending', 'cancelled', 'returned'
- sales_by_month_country(month TEXT 'YYYY-MM', country TEXT, orders INTEGER, total_sales REAL)
  Only completed orders.
- top_10_customers(customer TEXT, orders INTEGER, total_spent REAL)
  Only completed orders, sorted by total_spent desc.

Rules:
- Country names are stored in Spanish: 'España', 'México', 'Argentina', 'Colombia', 'Chile', 'Perú'.
- Data covers the year 2024. If the question gives a month without a year, use 2024.
- "Ventas" means completed orders: prefer the views when they answer the question.
- Return ONLY the SQL query. No explanation, no markdown.
- If the question cannot be answered with these tables, return exactly: CANNOT_ANSWER
"""


class LLMError(Exception):
    pass


def _extract_sql(text: str):
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return (match.group(1) if match else text).strip()


def generate_sql(question: str):
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    if not api_key or not model:
        raise LLMError("LLM_API_KEY and LLM_MODEL must be set in .env")

    client = OpenAI(api_key=api_key, base_url=base_url or None)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0,
        )
    except OpenAIError as e:
        raise LLMError(str(e))

    sql = _extract_sql(response.choices[0].message.content or "")
    if not sql:
        raise LLMError("empty response from the model")
    if sql == "CANNOT_ANSWER":
        raise LLMError("the question cannot be answered with the available data")
    return sql