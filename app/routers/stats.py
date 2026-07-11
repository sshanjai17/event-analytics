# app/routers/stats.py
import json
from fastapi import APIRouter, HTTPException
from sqlalchemy import func, text
from app.database import SessionLocal
from app.models import Event
from app.services.cache import r

router = APIRouter(prefix="/stats", tags=["stats"])
CACHE_TTL = 60

def cached(key: str, compute):
    hit = r.get(key)
    if hit:
        return json.loads(hit)
    result = compute()
    r.setex(key, CACHE_TTL, json.dumps(result, default=str))
    return result

@router.get("/{api_key}/daily")
def daily_views(api_key: str):
    def compute():
        db = SessionLocal()
        try:
            rows = db.query(
                func.date(Event.timestamp).label("day"),
                func.count().label("views"),
            ).filter(
                Event.api_key == api_key,
                Event.event_type == "page_view",
            ).group_by(text("day")).order_by(text("day")).all()
            return [{"day": str(d), "views": v} for d, v in rows]
        finally:
            db.close()
    return cached(f"stats:{api_key}:daily", compute)

@router.get("/{api_key}/top-pages")
def top_pages(api_key: str, limit: int = 10):
    def compute():
        db = SessionLocal()
        try:
            rows = db.query(
                Event.page, func.count().label("views")
            ).filter(
                Event.api_key == api_key,
                Event.event_type == "page_view",
            ).group_by(Event.page).order_by(func.count().desc()).limit(limit).all()
            return [{"page": p, "views": v} for p, v in rows]
        finally:
            db.close()
    return cached(f"stats:{api_key}:top", compute)

@router.get("/{api_key}/event-types")
def event_types(api_key: str):
    def compute():
        db = SessionLocal()
        try:
            rows = db.query(
                Event.event_type, func.count().label("count")
            ).filter(Event.api_key == api_key
            ).group_by(Event.event_type).order_by(func.count().desc()).all()
            return [{"event_type": t, "count": c} for t, c in rows]
        finally:
            db.close()
    return cached(f"stats:{api_key}:types", compute)