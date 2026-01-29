import csv
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from collections import Counter, defaultdict

router = APIRouter(prefix="/api/analytics")

CSV_FILE = "events.csv"

class Event(BaseModel):
    event_type: str       # "product_view" or "add_to_cart"
    product_id: int
    user_id: str = "guest"
    metadata: dict = {}

def append_csv(row: dict):
    try:
        with open(CSV_FILE, "r") as f:
            exists = True
    except FileNotFoundError:
        exists = False

    with open(CSV_FILE, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def read_csv():
    events = []
    try:
        with open(CSV_FILE, "r") as f:
            for row in csv.DictReader(f):
                events.append(row)
    except FileNotFoundError:
        pass
    return events


# ============ TRACKING ============

@router.post("/analytics/track")
def track_event(event: Event):
    if event.event_type not in ["product_view", "add_to_cart"]:
        return {"status": "ignored", "reason": "unsupported_event"}

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event.event_type,
        "product_id": str(event.product_id),
        "user_id": event.user_id,
        "metadata": str(event.metadata)
    }
    append_csv(row)
    return {"status": "ok"}


# ============ GLOBAL ============

@router.get("/analytics/global")
def get_global():
    events = read_csv()

    views = Counter(e["product_id"] for e in events if e["event_type"] == "product_view")
    adds = Counter(e["product_id"] for e in events if e["event_type"] == "add_to_cart")

    # engagement score
    score = {pid: views[pid] + 2 * adds[pid] for pid in set(views.keys()) | set(adds.keys())}

    return {
        "views": views,
        "add_to_cart": adds,
        "score": score
    }


# ============ PER USER ============

@router.get("/analytics/users")
def get_users():
    events = read_csv()

    per_user = defaultdict(lambda: {"views": Counter(), "add_to_cart": Counter()})

    for e in events:
        u = e["user_id"]
        p = e["product_id"]
        if e["event_type"] == "product_view":
            per_user[u]["views"][p] += 1
        elif e["event_type"] == "add_to_cart":
            per_user[u]["add_to_cart"][p] += 1

    return per_user


# ============ TOP PRODUCTS ============

@router.get("/analytics/top")
def get_top(limit: int = 10):
    global_stats = get_global()

    score = global_stats["score"]

    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return [{"product_id": pid, "score": score} for pid, score in ranked][:limit]


# ---------------- SUMMARY ----------------
@router.get("/analytics/summary")
def analytics_summary():
    events = read_csv()

    views_global = Counter(e["product_id"] for e in events if e["event_type"] == "product_view")
    cart_global = Counter(e["product_id"] for e in events if e["event_type"] == "add_to_cart")

    views_by_user = defaultdict(lambda: defaultdict(int))
    cart_by_user = defaultdict(lambda: defaultdict(int))

    for e in events:
        pid = e["product_id"]
        uid = e["user_id"]
        if e["event_type"] == "product_view":
            views_by_user[pid][uid] += 1
        elif e["event_type"] == "add_to_cart":
            cart_by_user[pid][uid] += 1

    return {
        "global": {
            "views": views_global,
            "add_to_cart": cart_global,
        },
        "per_user": {
            "views": views_by_user,
            "add_to_cart": cart_by_user,
        }
    }