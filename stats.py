from fastapi import APIRouter
from app.services.thestatsapi import stats_client

router = APIRouter()

@router.get("/{match_id}/stats")
async def get_match_stats(match_id: str):
    """Get full match statistics - REAL DATA from TheStatsAPI

    Returns: corners, shots (total/on target/off target), goals, cards, 
    possession, xG, passes, tackles, fouls, etc.
    """
    return await stats_client.get_match_stats(match_id)

@router.get("/{match_id}/live-stats")
async def get_live_stats(match_id: str):
    """Get live in-match statistics - REAL TIME DATA"""
    return await stats_client.get_live_stats(match_id)

@router.get("/{match_id}/player-stats")
async def get_player_stats(match_id: str):
    """Get per-player statistics - REAL DATA"""
    return await stats_client.get_player_stats(match_id)
