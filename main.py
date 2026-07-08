from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enforce open CORS policy as required by the grader
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_tjank51ogyac12qeaghw1815"

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsPayload(BaseModel):
    events: List[Event]

@app.post("/analytics")
def compute_analytics(payload: AnalyticsPayload, x_api_key: Optional[str] = Header(None)):
    # 1. Strict Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = payload.events
    
    unique_users = set()
    total_revenue = 0.0
    user_positive_revenue = {}

    # 2. Single-pass Aggregation
    for event in events:
        unique_users.add(event.user)
        
        # Only aggregate positive amounts for revenue and top_user
        if event.amount > 0:
            total_revenue += event.amount
            user_positive_revenue[event.user] = user_positive_revenue.get(event.user, 0.0) + event.amount

    # 3. Determine top user
    top_user = max(user_positive_revenue, key=user_positive_revenue.get) if user_positive_revenue else ""

    return {
        "email": "23f3003934@ds.study.iitm.ac.in",
        "total_events": len(events),
        "unique_users": len(unique_users),
        "revenue": total_revenue,
        "top_user": top_user
    }