# scripts/seed.py
from app.database import SessionLocal
from app.models import Site

db = SessionLocal()
if not db.query(Site).filter_by(api_key="demo_123").first():
    db.add(Site(name="Demo Blog", api_key="demo_123"))
    db.commit()
    print("Seeded demo site")
else:
    print("Already seeded")
db.close()