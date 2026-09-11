import json
import argparse
import requests
from typing import Dict, Any
from environment.connector import SaaSConnector

def evaluate_task(task_filepath: str, base_url: str = "http://localhost:8000") -> bool:
    connector = SaaSConnector(base_url=base_url)
    
    # Reset DB to starting state
    connector.reset_state()

    with open(task_filepath, "r") as f:
        task = json.load(f)

    print(f"Executing Task [{task['task_id']}]: {task['instruction']}")
    
    # Simulating agent execution:
    connector.execute_tool("create_issue", {
        "title": "Payment Gateway API Timeout",
        "description": "Auto-triaged by AI agent.",
        "priority": "high",
        "assignee_id": "dev_404"
    })

    # Programmatic Rubric Evaluation: Query system state directly
    resp = requests.get(f"{base_url}/api/v1/issues")
    all_issues = resp.json()

    req = task["expected_state"]["required_record"]
    matched = any(
        issue["title"] == req["title"] and
        issue["priority"] == req["priority"] and
        issue["assignee_id"] == req["assignee_id"]
        for issue in all_issues
    )

    if matched:
        print("EVALUATION SUCCESS: State delta matches rubric criteria.")
        return True
    else:
        print("EVALUATION FAILURE: Required state change was not produced.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="Path to task JSON definition file")
    args = parser.parse_args()
    
    evaluate_task(args.task)
