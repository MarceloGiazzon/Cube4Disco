from typing import List, Optional
from pydantic import BaseModel

class GeoScope(BaseModel):
    level: str
    ibge_codes: List[str]

class DateRange(BaseModel):
    start: str
    end: str

class CorrelateRequest(BaseModel):
    client_id: str
    metric_target: str
    geo_scope: GeoScope
    date_range: DateRange
    external_dimensions: List[str]
    webhook_url: Optional[str] = None
