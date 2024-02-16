from os import getenv
from typing import Annotated

from redis import Redis
from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

HOST = getenv("HOST", "http://localhost:8000")
REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cache():
    cache = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        yield cache
    finally:
        cache.close()

@app.head("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def index():
    return FileResponse("./static/index.html")


@app.get("/favicon.ico", include_in_schema=False) 
def favicon():
    return FileResponse("./static/favicon.ico")


@app.get("/{id}")
def get_url(id: str, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    if url := cache.get(id):
        return RedirectResponse(str(url))

    item = crud.get_url(db, id)
    if item is None:
        raise HTTPException(status_code=404)
    else:
        cache.set(id, str(item.url))
        return RedirectResponse(str(item.url))


@app.post("/")
def add_url(
        url: Annotated[HttpUrl, Form()],
        id: Annotated[str | None, Form()] = None,
        db: Session = Depends(get_db)
    ):
    try:
        item = crud.create_item(db, schemas.ItemCreate(url=url, id=id))
    except HTTPException as err:
        return HTMLResponse(f"<div>error: {err.detail}</div>")
    return HTMLResponse(f"<div>ok: {HOST}/{item.id}</div>")
