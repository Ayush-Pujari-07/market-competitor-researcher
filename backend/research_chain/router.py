import logging

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request

from backend.auth import dependencies as auth_dependencies
from backend.research_chain.schema import ResearchRequest
from backend.research_chain import service as research_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/research/create")
async def research_report(
    request: Request,
    research_report: ResearchRequest,
    user: dict[str, Any] = Depends(auth_dependencies.valid_refresh_token)
):
    try:
        report = await research_service.create_report(research_report, user)
        return {"message": "Research report created", "report": report}
    except Exception as e:
        logger.error(f"Error starting research: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error") from e
