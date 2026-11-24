import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from api.db import run_query
from api.llm import LLMError, generate_sql
from api.sql_validator import InvalidQueryError, validate_sql

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="esteban-csv-sql-fastapi-llm")


class AskRequest(BaseModel):
    question: str = Field(min_length=3, examples=["Cuánto vendimos en España en marzo?"])


class AskResponse(BaseModel):
    question: str
    sql: str
    rows: list[dict]


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    try:
        sql = generate_sql(body.question)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    try:
        sql = validate_sql(sql)
    except InvalidQueryError as e:
        raise HTTPException(status_code=400, detail=f"Invalid query: {e}")

    try:
        rows = run_query(sql)
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {e}")

    return AskResponse(question=body.question, sql=sql, rows=rows)