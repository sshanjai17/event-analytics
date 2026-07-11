# app/main.py
from fastapi import FastAPI, HTTPException
from app.database import SessionLocal
from app.models import Event, Site
from app.schemas import EventIn

app = FastAPI(title="Event Analytics")

@app.post("/events", status_code=202)
def ingest_event(event: EventIn):
    db = SessionLocal()
    try:
        site = db.query(Site).filter(Site.api_key == event.api_key).first()
        if not site:
            raise HTTPException(status_code=401, detail="Unknown api_key")
        db.add(Event(**event.model_dump()))
        db.commit()
    finally:
        db.close()
    return {"status": "accepted"}