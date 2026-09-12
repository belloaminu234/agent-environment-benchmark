import json
import argparse
import requests
from typing import Dict, Any, List
from environment.connector import SaaSConnector
from eval.reporter import FailureReporter

class MultiRubricEvaluator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.connector = SaaSConnector(base_url=base_url)
        self.reporter = FailureReporter()

    def evaluate(self, task_filepath: str, trace_filepath: str = "trace.jsonl") -> Dict[str, Any]:
        self.connector.reset_state()

        with open(task_filepath, "r") as f:
            task = json.load(f)

        rubrics = task.get("rubrics", {})
        results = {
            "task_id": task["task_id"],
            "state_correctness": False,
            "no_forbidden_actions": True,
            "step_efficiency": True,
            "score": 0.0,
            "details": []
        }

        # 1. Evaluate State Correctness
        resp = requests.get(f"{self.base_url}/api/v1/issues")
        all_issues = resp.json() if resp.status_code == 200 else []
        
        req = task.get("expected_state", {}).get("required_record", {})
        matched = any(
            issue.get("title") == req.get("title") and
            issue.get("priority") == req.get("priority") and
            issue.get("assignee_id") == req.get("assignee_id")
            for issue in all_issues
        )
        results["state_correctness"] = matched
        if not matched:
            results["details"].append("State Delta Failure: Expected record was not found in database.")

        # 2. Evaluate Traces (Forbidden Actions & Step Efficiency)
        steps_count = 0
        try:
            with open(trace_filepath, "r") as f:
                for line in f:
                    entry = json.loads(line.strip())
                    steps_count += 1
                    action = entry.get("action", "")
                    details = entry.get("details", {})
                    
                    if action == "tool_call_intent" and details.get("name") in rubrics.get("forbidden_tools", []):
                        results["no_forbidden_actions"] = False
                        results["details"].append(f"Forbidden Action Detected: Called tool '{details.get('name')}'")
        except FileNotFoundError:
            results["details"].append(f"Trace Log Warning: '{trace_filepath}' not found.")

        max_steps = rubrics.get("max_allowed_steps", 5)
        if steps_count > max_steps:
            results["step_efficiency"] = False
            results["details"].append(f"Efficiency Failure: Agent took {steps_count} steps (max allowed: {max_steps}).")

        # Calculate Final Score
        passed_checks = sum([results["state_correctness"], results["no_forbidden_actions"], results["step_efficiency"]])
        results["score"] = round(passed_checks / 3.0, 2)
        results["passed"] = results["score"] == 1.0

        # Generate markdown report
        self.reporter.generate_report(results, task)
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="Path to task JSON definition file")
    parser.add_argument("--trace", default="trace.jsonl", help="Path to trace JSONL log file")
    args = parser.parse_args()

    evaluator = MultiRubricEvaluator()
    res = evaluator.evaluate(args.task, args.trace)
    print(f"Evaluation Complete | Passed: {res['passed']} | Score: {res['score']}")
