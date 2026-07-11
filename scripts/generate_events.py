# scripts/generate_events.py
import random
from datetime import datetime, timedelta, timezone
from app.database import SessionLocal
from app.models import Event

N = 50_000
PAGES = ["/home", "/blog/fastapi-tips", "/blog/docker-basics", "/pricing",
         "/about", "/blog/sql-indexing", "/contact", "/docs"]
EVENT_TYPES = ["page_view", "page_view", "page_view", "page_view",
               "click", "click", "signup"]  # weighted: views most common
now = datetime.now(timezone.utc)

events = []
for _ in range(N):
    ts = now - timedelta(
        days=random.randint(0, 29),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    events.append({
        "api_key": "demo_123",
        "event_type": random.choice(EVENT_TYPES),
        "page": random.choice(PAGES),
        "properties": {},
        "timestamp": ts,
    })

db = SessionLocal()
db.bulk_insert_mappings(Event, events)
db.commit()
db.close()
print(f"Inserted {N} events across 30 days")