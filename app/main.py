# app/main.py
from fastapi import FastAPI, HTTPException
from app.database import SessionLocal
from app.models import Site
from app.schemas import EventIn
from app.services.queue import push_event
from app.services.cache import is_valid_api_key
from app.routers.stats import router as stats_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Event Analytics")
app.include_router(stats_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # dev-only; production would list real domains
    allow_methods=["*"],
    allow_headers=["*"],
)

def _db_has_key(api_key: str) -> bool:
    db = SessionLocal()
    try:
        return db.query(Site).filter(Site.api_key == api_key).first() is not None
    finally:
        db.close()

@app.post("/events", status_code=202)
def ingest_event(event: EventIn):
    if not is_valid_api_key(event.api_key, _db_has_key):
        raise HTTPException(status_code=401, detail="Unknown api_key")
    push_event(event.model_dump())
    return {"status": "accepted"}