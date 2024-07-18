import logging

from typing import Any
from datetime import datetime
from bson.objectid import ObjectId

from backend.db import get_db
from backend.config import settings
from backend.research_chain.market_research_chain import chain as market_research_chain
from backend.research_chain.competitor_research_chain import chain as competitor_research_chain
from backend.research_chain.schema import ResearchRequest, ResearchReportOut

logger = logging.getLogger(__name__)

db = get_db(settings.PROJECT_NAME)


async def create_report(report: ResearchRequest, user: dict[str, Any]):
    try:
        logger.info(report)
        if report.competitor_research:
            query_type = "competitor_research"
            query = f"Create a compititor researchreport on {report.company} that operates in the {report.industry} industry and has the following competitors: {report.competitors}"
            logger.info(query)
            report_res = await competitor_research_chain.ainvoke(input={"question": query})
            logger.info(report_res)
        else:
            query_type = "market_research"
            query = f"Create a market research report on {report.company} that operates in the {report.industry} industry"
            logger.info(query)
            report_res = await market_research_chain.ainvoke(input={"question": query})
            logger.info(report_res)

        research_report = await db.research_reports.insert_one({
            "query": query,
            "user_id": ObjectId(user["user_id"]),
            "research_report": report_res,
            "type": query_type,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })

        return ResearchReportOut.model_validate({
            "id": str(research_report.inserted_id),
            "type": query_type,
            "query": query,
            "report": report_res,
            "user_id": str(user["user_id"]),
        })
    except Exception as e:
        logger.error(e)
        raise e
