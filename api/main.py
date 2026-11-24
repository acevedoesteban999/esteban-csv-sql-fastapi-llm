from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="esteban-csv-sql-fastapi-llm")


class AskRequest(BaseModel):
    question: str


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/ask")
def ask(body: AskRequest):
    return {"question": body.question, "answer": "test"}