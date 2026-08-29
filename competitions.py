from fastapi import APIRouter, Query
from typing import Optional
from app.services.thestatsapi import stats_client

router = APIRouter()

@router.get("/")
async def list_competitions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    country: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """List all football competitions from TheStatsAPI (REAL DATA)"""
    return await stats_client.get_competitions(
        page=page, per_page=per_page, country=country, search=search
    )
