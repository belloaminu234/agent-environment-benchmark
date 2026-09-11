import requests
from typing import Dict, Any

class SaaSConnector:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def reset_state(self) -> bool:
        resp = requests.post(f"{self.base_url}/admin/reset")
        return resp.status_code == 200

    def execute_tool(self, name: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if name == "create_issue":
            resp = requests.post(f"{self.base_url}/api/v1/issues", json=kwargs)
            return resp.json()
        raise ValueError(f"Unknown tool name: {name}")
