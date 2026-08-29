from fastapi import APIRouter
from app.services.thestatsapi import stats_client

router = APIRouter()

@router.get("/{match_id}/odds")
async def get_match_odds(match_id: str):
    """Get pre-match odds from multiple bookmakers - REAL DATA

    Markets: Match Result, BTTS (Ambos Anotan), Total Goals, Corners, Asian Handicap
    """
    return await stats_client.get_match_odds(match_id)

@router.get("/{match_id}/odds/live")
async def get_live_odds(match_id: str):
    """Get live in-play odds - REAL TIME DATA"""
    return await stats_client.get_live_odds(match_id)
