from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime, timezone
from app.models import Issue, IssueCreate
from app.database import IN_MEMORY_DB, reset_db

app = FastAPI(title="Mock Enterprise SaaS Engine", version="1.0.0")

@app.on_event("startup")
def startup_event():
    reset_db()

@app.post("/admin/reset", status_code=status.HTTP_200_OK)
def reset_environment():
    """Resets DB to deterministic initial state for clean evaluation runs."""
    reset_db()
    return {"status": "success", "message": "Environment reset complete."}

@app.get("/api/v1/issues", response_model=List[Issue])
def list_issues():
    return list(IN_MEMORY_DB.values())

@app.post("/api/v1/issues", response_model=Issue, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    issue_id = f"ISSUE-{len(IN_MEMORY_DB) + 101}"
    now = datetime.now(timezone.utc)
    new_issue = Issue(
        id=issue_id,
        created_at=now,
        updated_at=now,
        **payload.model_dump()
    )
    IN_MEMORY_DB[issue_id] = new_issue
    return new_issue
