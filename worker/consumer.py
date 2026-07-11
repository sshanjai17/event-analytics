# worker/consumer.py
import time
from app.database import SessionLocal
from app.models import Event
from app.services.queue import pop_batch

BATCH_SIZE = 500
POLL_INTERVAL = 1  # seconds to sleep when queue is empty

def process_batch() -> int:
    events = pop_batch(BATCH_SIZE)
    if not events:
        return 0

    db = SessionLocal()
    try:
        db.bulk_insert_mappings(Event, events)
        db.commit()
        return len(events)
    except Exception as e:
        db.rollback()
        print(f"Batch insert failed: {e}")
        return 0
    finally:
        db.close()

def run():
    print("Worker started, watching queue...")
    while True:
        count = process_batch()
        if count:
            print(f"Inserted {count} events")
        else:
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    run()