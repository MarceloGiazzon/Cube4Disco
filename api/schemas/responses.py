from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class CorrelateAcceptedResponse(BaseModel):
    job_id: str
    status: str
    estimated_time_seconds: int
    check_status_url: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    findings: Optional[List[Dict[str, Any]]] = None
