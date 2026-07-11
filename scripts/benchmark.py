# scripts/benchmark.py
import time
import requests

N = 200
event = {"api_key": "demo_123", "event_type": "page_view", "page": "/bench"}

start = time.time()
for i in range(N):
    requests.post("http://127.0.0.1:8000/events", json=event)
elapsed = time.time() - start

print(f"{N} events in {elapsed:.2f}s -> {N/elapsed:.0f} events/sec")