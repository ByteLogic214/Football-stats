import httpx
from typing import Optional, List, Dict, Any
from app.config import get_settings

class TheStatsAPIClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.THESTATSAPI_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.settings.THESTATSAPI_KEY}",
            "Accept": "application/json"
        }

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated GET request to TheStatsAPI"""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self.headers, params=params or {})
            response.raise_for_status()
            return response.json()

    async def health_check(self) -> Dict[str, Any]:
        """Check API health (no auth required)"""
        url = f"{self.base_url}/health"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def get_competitions(self, page: int = 1, per_page: int = 20, 
                                country: Optional[str] = None,
                                search: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page}
        if country:
            params["country"] = country
        if search:
            params["search"] = search
        return await self._get("/football/competitions", params)

    async def get_matches(self, page: int = 1, per_page: int = 20,
                          competition_id: Optional[str] = None,
                          status: Optional[str] = None,
                          date_from: Optional[str] = None,
                          date_to: Optional[str] = None,
                          team_id: Optional[str] = None) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page}
        if competition_id:
            params["competition_id"] = competition_id
        if status:
            params["status"] = status
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if team_id:
            params["team_id"] = team_id
        return await self._get("/football/matches", params)

    async def get_match(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}")

    async def get_match_stats(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/stats")

    async def get_live_stats(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/live-stats")

    async def get_match_odds(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/odds")

    async def get_live_odds(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/odds/live")

    async def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/timeline")

    async def get_player_stats(self, match_id: str) -> Dict[str, Any]:
        return await self._get(f"/football/matches/{match_id}/player-stats")

# Singleton instance
stats_client = TheStatsAPIClient()
