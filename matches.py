from fastapi import APIRouter, Query
from typing import Optional
from app.services.thestatsapi import stats_client

router = APIRouter()

@router.get("/")
async def list_matches(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    competition_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None, enum=["scheduled", "live", "finished", "postponed", "cancelled"]),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    team_id: Optional[str] = Query(None)
):
    """List matches with filters - REAL DATA from TheStatsAPI"""
    return await stats_client.get_matches(
        page=page, per_page=per_page,
        competition_id=competition_id, status=status,
        date_from=date_from, date_to=date_to, team_id=team_id
    )

@router.get("/{match_id}")
async def get_match(match_id: str):
    """Get single match details - REAL DATA"""
    return await stats_client.get_match(match_id)

@router.get("/{match_id}/timeline")
async def get_match_timeline(match_id: str):
    """Get match event timeline - REAL DATA"""
    return await stats_client.get_match_timeline(match_id)
