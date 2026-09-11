from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class IssueStatus(str, Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class IssueCreate(BaseModel):
    title: str = Field(..., example="Authentication timeout on web app")
    description: Optional[str] = Field(None, example="Sessions drop after 5 minutes of inactivity.")
    status: IssueStatus = IssueStatus.BACKLOG
    priority: Priority = Priority.MEDIUM
    assignee_id: Optional[str] = Field(None, example="eng_user_01")

class Issue(IssueCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
