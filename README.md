# 🏏 Cricbuzz LiveStats

A cricket analytics dashboard integrating the Cricbuzz API with a SQL database, built with
Python + Streamlit.

## Features
- **Live Match** — live scores/status from the Cricbuzz API (mock fallback if no API key)
- **Top Player Stats** — top batting & bowling leaderboards
- **SQL Analytics** — 25 practice queries (8 beginner, 8 intermediate, 9 advanced) run live
  against the local database
- **CRUD Operations** — add / update / delete player records via a form UI

## Setup
```bash
pip install -r requirements.txt
python generate_sample_data.py      # builds schema + seeds sample data
streamlit run main.py
```

### Live API data (optional)
Get a free key at [RapidAPI — Cricbuzz Cricket](https://rapidapi.com/), then:
```bash
export CRICBUZZ_API_KEY="your_rapidapi_key_here"   # Mac/Linux
setx CRICBUZZ_API_KEY "your_rapidapi_key_here"      # Windows
```
Without a key, the Live Match / Top Player Stats pages automatically show clearly-labeled
mock data so the app still runs end-to-end for grading/demo purposes.

## Project Structure
```
cricbuzz-livestats/
├── main.py                    # Home page (Streamlit entry point)
├── pages/
│   ├── 1_Live_Match.py
│   ├── 2_Top_Player_Stats.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD_Operations.py
├── utils/
│   ├── db_connection.py       # centralized DB connection (swap engine here)
│   ├── api_client.py          # Cricbuzz API wrapper + mock fallback
│   └── sql_queries.py         # all 25 SQL practice queries
├── schema.sql                 # table definitions + indexes
├── generate_sample_data.py    # seeds realistic sample data
├── data/cricbuzz_livestats.db # SQLite DB (generated)
└── requirements.txt
```

## Database
SQLite by default (`data/cricbuzz_livestats.db`). Swap to Postgres/MySQL by editing
`get_connection()` in `utils/db_connection.py` — every other module only calls
`run_query()` / `execute_write()`, so no other code changes are needed.

Tables: `teams`, `players`, `venues`, `series`, `matches`, `batting_stats`,
`bowling_stats`, `fielding_stats`.

## Tech Stack
Python · Streamlit · SQLite · Cricbuzz REST API · pandas · requests

## Author
**Prachi Sable**|Data Analyst|Pune
