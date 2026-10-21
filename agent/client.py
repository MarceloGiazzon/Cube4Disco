import httpx
from typing import Any, Dict

class Cube4DiscoAgentClient:
    """
    Dispara cargas agregadas via HTTPS Outbound (porta 443) para o Web Service.
    """
    def __init__(self, endpoint_url: str, api_token: str):
        self.endpoint_url = endpoint_url
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def push_aggregated_dataset(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.endpoint_url}/api/v1/ingest/aggregated",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
