import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

class FailureReporter:
    def __init__(self, output_filepath: str = "reports/failure_analysis.md"):
        self.output_filepath = output_filepath

    def generate_report(self, eval_results: Dict[str, Any], task_def: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.output_filepath), exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        status_str = "PASSED" if eval_results.get("passed") else "FAILED"

        markdown_content = f"""# Agent Task Evaluation & Diagnostic Failure Report

**Task ID:** `{task_def.get('task_id')}`  
**Evaluation Status:** `{status_str}`  
**Overall Rubric Score:** `{eval_results.get('score')} / 1.0`  
**Timestamp:** `{timestamp}`  

---

## Task Instruction & Context
> {task_def.get('instruction')}

---

## Multi-Rubric Score Breakdown

| Rubric Criteria | Status | Target Constraint |
|---|---|---|
| **State Correctness** | {'PASSED' if eval_results.get('state_correctness') else 'FAILED'} | Target record created in database |
| **Forbidden Actions** | {'PASSED' if eval_results.get('no_forbidden_actions') else 'FAILED'} | Zero calls to restricted tools |
| **Step Efficiency** | {'PASSED' if eval_results.get('step_efficiency') else 'FAILED'} | Task finished within step budget |

---

## Detailed Failure Diagnosis & Actionable Feedback

"""
        if eval_results.get("details"):
            for detail in eval_results["details"]:
                markdown_content += f"- **Diagnostic Alert:** {detail}
"
        else:
            markdown_content += "- **No failures detected.** All rubric criteria satisfied end-to-end.
"

        markdown_content += """
---

## Recommended Engineering Next Steps
1. **Connector Team:** Verify tool schema definitions and API endpoint parameter parsing if parameters were dropped.
2. **Task/Prompt Engineering:** Clarify edge-case boundary conditions in prompt instructions to eliminate agent ambiguity.
"""

        with open(self.output_filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Diagnostic report written to: {self.output_filepath}")
