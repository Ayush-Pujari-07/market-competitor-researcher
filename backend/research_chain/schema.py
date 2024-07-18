from typing import List, Optional  # type: ignore
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    industry: Optional[str] = None
    company: Optional[str] = None
    competitors: Optional[List[str]] = None
    market_research: bool = Field(default=False)
    competitor_research: bool = Field(default=False)


class ResearchReportOut(BaseModel):
    id: str
    type: str
    query: str
    report: str
    user_id: str


class ResearchReportUpdate(BaseModel):
    research_report: Optional[str] = None
