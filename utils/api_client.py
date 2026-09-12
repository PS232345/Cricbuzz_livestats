"""
Cricbuzz Cricket API wrapper (via RapidAPI).

Set your key as an environment variable before running the app:
    export CRICBUZZ_API_KEY="your_rapidapi_key_here"     (Mac/Linux)
    setx CRICBUZZ_API_KEY "your_rapidapi_key_here"        (Windows)

If no key is set, all functions fall back to realistic MOCK data so the
Live Match / Top Stats pages still work end-to-end for demo purposes.
"""
import os
import requests

try:
    import streamlit as st
    _SECRET_KEY = st.secrets.get("CRICBUZZ_API_KEY", "") if hasattr(st, "secrets") else ""
except Exception:
    _SECRET_KEY = ""

API_KEY = os.environ.get("CRICBUZZ_API_KEY", "") or _SECRET_KEY
API_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
}


def _is_configured() -> bool:
    return bool(API_KEY)


def _get(endpoint: str, params: dict = None):
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params or {}, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Mock data (used automatically when CRICBUZZ_API_KEY is not set)
# ---------------------------------------------------------------------------
_MOCK_LIVE_MATCHES = [
    {"match_id": "m1", "series": "India tour of Australia 2026",
     "team1": "India", "team2": "Australia", "status": "India need 45 runs in 6 overs",
     "venue": "Melbourne Cricket Ground, Melbourne", "format": "ODI"},
    {"match_id": "m2", "series": "England vs South Africa T20I Series",
     "team1": "England", "team2": "South Africa", "status": "South Africa won by 4 wickets",
     "venue": "Lord's, London", "format": "T20I"},
    {"match_id": "m3", "series": "Pakistan tri-series",
     "team1": "Pakistan", "team2": "Sri Lanka", "status": "Match starts in 2 hours",
     "venue": "Gaddafi Stadium, Lahore", "format": "ODI"},
]

_MOCK_TOP_BATTING = [
    {"player": "Virat Kohli", "runs": 13906, "average": 58.68, "centuries": 50},
    {"player": "Rohit Sharma", "runs": 10866, "average": 48.96, "centuries": 32},
    {"player": "Babar Azam", "runs": 9339, "average": 56.86, "centuries": 20},
]

_MOCK_TOP_BOWLING = [
    {"player": "Jasprit Bumrah", "wickets": 156, "economy": 4.56},
    {"player": "Rashid Khan", "wickets": 174, "economy": 4.16},
    {"player": "Trent Boult", "wickets": 211, "economy": 4.94},
]


# ---------------------------------------------------------------------------
# Public functions used by the Streamlit pages
# ---------------------------------------------------------------------------
def get_live_matches():
    if not _is_configured():
        return _MOCK_LIVE_MATCHES, "mock"
    try:
        data = _get("/matches/v1/live")
        return data, "live"
    except Exception as e:
        return _MOCK_LIVE_MATCHES, f"mock (API error: {e})"


def get_top_batting_stats(stat_type="mostRuns"):
    if not _is_configured():
        return _MOCK_TOP_BATTING, "mock"
    try:
        data = _get(f"/stats/v1/topstats/0", params={"statsType": stat_type})
        return data, "live"
    except Exception as e:
        return _MOCK_TOP_BATTING, f"mock (API error: {e})"


def get_top_bowling_stats(stat_type="mostWickets"):
    if not _is_configured():
        return _MOCK_TOP_BOWLING, "mock"
    try:
        data = _get(f"/stats/v1/topstats/0", params={"statsType": stat_type})
        return data, "live"
    except Exception as e:
        return _MOCK_TOP_BOWLING, f"mock (API error: {e})"
