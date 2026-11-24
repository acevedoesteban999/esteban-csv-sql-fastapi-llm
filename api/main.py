from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from api.llm import LLMError, generate_sql

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="esteban-csv-sql-fastapi-llm")


class AskRequest(BaseModel):
    question: str


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/ask")
def ask(body: AskRequest):
    try:
        answer = generate_sql(body.question)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")
    return {"question": body.question, "answer": answer}