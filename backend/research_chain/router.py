import logging

from typing import Any  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, Request, encoders

from backend.auth import dependencies as auth_dependencies
from backend.research_chain.schema import ResearchRequest, ResearchReportUpdate
from backend.research_chain import service as research_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/research/report/create")
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
            status_code=500, detail="Error starting research") from e


@router.get("/research/get_report/{report_id}")
async def get_report(
    report_id: str,
    user: dict[str, Any] = Depends(auth_dependencies.valid_refresh_token)
):
    try:
        report = await research_service.get_report(report_id)
        return encoders.jsonable_encoder(report)
    except Exception as e:
        logger.error(f"Error getting report: {e}")
        raise HTTPException(
            status_code=500, detail="Error getting report") from e


@router.get("/research/get_all")
async def get_all_research_reports(
    request: Request,
    user: dict[str, Any] = Depends(auth_dependencies.valid_refresh_token)
):
    try:
        reports = await research_service.get_all_reports(user)
        return encoders.jsonable_encoder(reports)
    except Exception as e:
        logger.error(f"Error getting all research reports: {e}")
        raise HTTPException(
            status_code=500, detail="Error getting all research reports") from e


@router.put("/research/update_report/{report_id}")
async def update_report(
    report_id: str,
    report: ResearchReportUpdate,
    user: dict[str, Any] = Depends(auth_dependencies.valid_refresh_token)
):
    try:
        await research_service.update_report(report_id, report)
        return {"message": "Research report updated"}
    except Exception as e:
        logger.error(f"Error updating report: {e}")
        raise HTTPException(
            status_code=500, detail="Error updating report") from e


@router.delete("/research/delete_report/{report_id}")
async def delete_report(
    report_id: str,
    user: dict[str, Any] = Depends(auth_dependencies.valid_refresh_token)
):
    try:
        await research_service.delete_report(report_id)
        return {"message": "Research report deleted"}
    except Exception as e:
        logger.error(f"Error deleting report: {e}")
        raise HTTPException(
            status_code=500, detail="Error deleting report") from e
