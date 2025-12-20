from pydantic import BaseModel


class ComplianceResult(BaseModel):
    id: str
    name: str
    type: str
    properties: dict[str, str] = {}
