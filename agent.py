import json
from typing import Dict, Any
from environment.connector import SaaSConnector
from harness.tracer import ExecutionTracer

class AgentRunner:
    def __init__(self, connector: SaaSConnector, tracer: ExecutionTracer):
        self.connector = connector
        self.tracer = tracer

    def run_task(self, instruction: str, max_steps: int = 5) -> Dict[str, Any]:
        print(f"Starting execution loop for: '{instruction}'")
        
        for step in range(1, max_steps + 1):
            if step == 1:
                tool_call = {
                    "name": "create_issue",
                    "args": {
                        "title": "Payment Gateway API Timeout",
                        "priority": "high",
                        "assignee_id": "dev_404"
                    }
                }
                self.tracer.log_step(step, "tool_call_intent", tool_call)
                
                result = self.connector.execute_tool(tool_call["name"], tool_call["args"])
                self.tracer.log_step(step, "tool_execution_result", result)
                return result
        return {}

if __name__ == "__main__":
    connector = SaaSConnector()
    tracer = ExecutionTracer()
    runner = AgentRunner(connector, tracer)
    runner.run_task("Triage customer issue and create high-priority ticket.")
