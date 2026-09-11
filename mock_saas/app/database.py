from typing import Dict
from datetime import datetime, timezone
from app.models import Issue, IssueStatus, Priority

IN_MEMORY_DB: Dict[str, Issue] = {}

def get_seed_data() -> Dict[str, Issue]:
    now = datetime.now(timezone.utc)
    return {
        "ISSUE-101": Issue(
            id="ISSUE-101",
            title="Database connection pool exhausted",
            description="High latency on production web pods.",
            status=IssueStatus.IN_PROGRESS,
            priority=Priority.HIGH,
            assignee_id="dev_404",
            created_at=now,
            updated_at=now
        )
    }

def reset_db():
    global IN_MEMORY_DB
    IN_MEMORY_DB = get_seed_data()
