from fastapi import APIRouter, HTTPException
from typing import List
from app.services.thestatsapi import stats_client
from app.models.schemas import MatchAnalysis, KeyStat, OddsComparison, Score

router = APIRouter()

def safe_float(val):
    try:
        return float(val) if val is not None else None
    except:
        return None

def decimal_to_implied_prob(odds_str: str) -> float:
    """Convert decimal odds to implied probability %"""
    try:
        odds = float(odds_str)
        if odds > 0:
            return round((1 / odds) * 100, 2)
        return None
    except:
        return None

@router.get("/{match_id}", response_model=MatchAnalysis)
async def analyze_match(match_id: str):
    """Full match analysis: stats + odds comparison - REAL DATA ONLY

    Combines match statistics with bookmaker odds to generate
    betting insights and probability calculations.
    """
    # Fetch real data from TheStatsAPI
    match_data = await stats_client.get_match(match_id)
    stats_data = await stats_client.get_match_stats(match_id)
    odds_data = await stats_client.get_match_odds(match_id)

    match = match_data.get("data", {})
    stats = stats_data.get("data", {})
    odds = odds_data.get("data", {})

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Build key stats
    key_stats = []
    overview = stats.get("overview", {})

    stat_mappings = {
        "corner_kicks": "Corners",
        "total_shots": "Remates Totales",
        "shots_on_target": "Remates al Arco",
        "expected_goals": "xG (Expected Goals)",
        "yellow_cards": "Tarjetas Amarillas",
        "fouls": "Faltas",
        "ball_possession": "Posesión %",
        "big_chances": "Grandes Chances",
        "goalkeeper_saves": "Paradas de Portero",
        "passes": "Pases",
        "accurate_passes": "Pases Precisos",
        "tackles": "Entradas",
    }

    for key, label in stat_mappings.items():
        if key in overview:
            item = overview[key]
            all_val = item.get("all", {})
            home = safe_float(all_val.get("home"))
            away = safe_float(all_val.get("away"))
            total = None
            if home is not None and away is not None:
                total = round(home + away, 2) if key != "ball_possession" else None

            key_stats.append(KeyStat(
                label=label,
                home=home,
                away=away,
                total=total
            ))

    # Build odds comparison
    odds_comparison = []
    bookmakers = odds.get("bookmakers", [])

    for bm in bookmakers:
        bm_name = bm.get("bookmaker", "Unknown")
        markets = bm.get("markets", {})

        # Match odds (1X2)
        if "match_odds" in markets:
            mo = markets["match_odds"]
            for selection, key in [("Local", "home"), ("Empate", "draw"), ("Visitante", "away")]:
                if key in mo:
                    val = mo[key]
                    odds_comparison.append(OddsComparison(
                        market="1X2",
                        bookmaker=bm_name,
                        selection=selection,
                        opening=val.get("opening"),
                        current=val.get("last_seen"),
                        implied_prob=decimal_to_implied_prob(val.get("last_seen", ""))
                    ))

        # BTTS (Ambos Anotan)
        if "btts" in markets:
            btts = markets["btts"]
            for selection, key in [("Sí (BTTS)", "yes"), ("No (BTTS)", "no")]:
                if key in btts:
                    val = btts[key]
                    odds_comparison.append(OddsComparison(
                        market="Ambos Anotan (BTTS)",
                        bookmaker=bm_name,
                        selection=selection,
                        opening=val.get("opening"),
                        current=val.get("last_seen"),
                        implied_prob=decimal_to_implied_prob(val.get("last_seen", ""))
                    ))

        # Total Goals Over/Under
        if "total_goals" in markets:
            tg = markets["total_goals"]
            for line, values in tg.items():
                for selection, key in [(f"Over {line}", "over"), (f"Under {line}", "under")]:
                    if key in values:
                        val = values[key]
                        odds_comparison.append(OddsComparison(
                            market=f"Total Goles {line}",
                            bookmaker=bm_name,
                            selection=selection,
                            opening=val.get("opening"),
                            current=val.get("last_seen"),
                            implied_prob=decimal_to_implied_prob(val.get("last_seen", ""))
                        ))

        # Corners Over/Under
        if "match_corners" in markets:
            mc = markets["match_corners"]
            for line, values in mc.items():
                for selection, key in [(f"Over {line} Corners", "over"), (f"Under {line} Corners", "under")]:
                    if key in values:
                        val = values[key]
                        odds_comparison.append(OddsComparison(
                            market=f"Corners {line}",
                            bookmaker=bm_name,
                            selection=selection,
                            opening=val.get("opening"),
                            current=val.get("last_seen"),
                            implied_prob=decimal_to_implied_prob(val.get("last_seen", ""))
                        ))

    # Calculate BTTS probability from odds
    btts_yes_odds = None
    btts_no_odds = None
    for oc in odds_comparison:
        if oc.market == "Ambos Anotan (BTTS)" and oc.selection == "Sí (BTTS)":
            btts_yes_odds = safe_float(oc.current)
        if oc.market == "Ambos Anotan (BTTS)" and oc.selection == "No (BTTS)":
            btts_no_odds = safe_float(oc.current)

    btts_prob = None
    if btts_yes_odds and btts_no_odds:
        # Remove vig: normalize probabilities
        p_yes = 1 / btts_yes_odds
        p_no = 1 / btts_no_odds
        total = p_yes + p_no
        if total > 0:
            btts_prob = round((p_yes / total) * 100, 2)

    # Over 2.5 goals probability
    over_25_odds = None
    under_25_odds = None
    for oc in odds_comparison:
        if "Over 2.5" in oc.selection and "Total Goles" in oc.market:
            over_25_odds = safe_float(oc.current)
        if "Under 2.5" in oc.selection and "Total Goles" in oc.market:
            under_25_odds = safe_float(oc.current)

    over_prob = None
    if over_25_odds and under_25_odds:
        p_over = 1 / over_25_odds
        p_under = 1 / under_25_odds
        total = p_over + p_under
        if total > 0:
            over_prob = round((p_over / total) * 100, 2)

    score_data = match.get("score", {})
    score = Score(
        home=score_data.get("home"),
        away=score_data.get("away")
    ) if score_data else None

    return MatchAnalysis(
        match_id=match_id,
        home_team=match.get("home_team", {}).get("name", "Unknown"),
        away_team=match.get("away_team", {}).get("name", "Unknown"),
        status=match.get("status", "unknown"),
        score=score,
        key_stats=key_stats,
        odds_comparison=odds_comparison,
        btts_probability=btts_prob,
        over_goals_probability=over_prob
    )
