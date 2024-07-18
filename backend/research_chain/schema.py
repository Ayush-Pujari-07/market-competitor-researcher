from typing import List

from pydantic import BaseModel, Field
from datetime import datetime


class ResearchRequest(BaseModel):
    industry: str | None
    company: str | None
    competitors: List[str] | None
    market_research: bool = Field(default=False)
    competitor_research: bool = Field(default=False)


class ResearchReportOut(BaseModel):
    id: str
    type: str
    query: str
    report: str
    user_id: str
