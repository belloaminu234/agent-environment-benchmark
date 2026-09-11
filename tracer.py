import json
from datetime import datetime, timezone
from typing import Dict, Any

class ExecutionTracer:
    def __init__(self, log_filepath: str = "trace.jsonl"):
        self.log_filepath = log_filepath

    def log_step(self, step_number: int, action_type: str, details: Dict[str, Any]):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step_number,
            "action": action_type,
            "details": details
        }
        with open(self.log_filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
