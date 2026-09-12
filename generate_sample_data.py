import sqlite3
import random
from datetime import date, timedelta
from utils.db_connection import DB_PATH
import os

random.seed(42)

COUNTRIES = ["India", "Australia", "England", "South Africa",
             "New Zealand", "Pakistan", "Sri Lanka", "Bangladesh"]

VENUES = [
    ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    ("Eden Gardens", "Kolkata", "India", 66000),
    ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
    ("Lord's", "London", "England", 30000),
    ("The Wanderers Stadium", "Johannesburg", "South Africa", 34000),
    ("Sydney Cricket Ground", "Sydney", "Australia", 48000),
    ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    ("R Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
    ("Sher-e-Bangla Stadium", "Dhaka", "Bangladesh", 26000),
    ("Basin Reserve", "Wellington", "New Zealand", 11600),
]

FIRST_NAMES = ["Rohit", "Virat", "Steve", "Joe", "Kane", "Babar", "Ben", "Quinton",
               "David", "Jos", "Shakib", "Rashid", "Trent", "Pat", "Mitchell", "Shaheen",
               "Jasprit", "Ravindra", "Marnus", "Dawid", "Faf", "Temba", "Litton", "Mahmudullah",
               "Glenn", "Travis", "Aiden", "Harry", "Mohammad", "Fakhar", "Mushfiqur", "Tom",
               "Rishabh", "Hardik", "Shubman", "Yashasvi", "Nathan", "Adam", "Alex", "Chris"]
LAST_NAMES = ["Sharma", "Kohli", "Smith", "Root", "Williamson", "Azam", "Stokes", "de Kock",
              "Warner", "Buttler", "Al Hasan", "Khan", "Boult", "Cummins", "Starc", "Afridi",
              "Bumrah", "Jadeja", "Labuschagne", "Malan", "du Plessis", "Bavuma", "Das", "Riyad",
              "Maxwell", "Head", "Markram", "Brook", "Rizwan", "Zaman", "Rahim", "Latham",
              "Pant", "Pandya", "Gill", "Jaiswal", "Lyon", "Zampa", "Carey", "Woakes"]

ROLES = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
BAT_STYLES = ["Right-hand bat", "Left-hand bat"]
BOWL_STYLES = ["Right-arm fast", "Left-arm fast", "Right-arm off break",
               "Left-arm orthodox", "Right-arm leg break", None]

FORMATS = ["Test", "ODI", "T20I"]


def build_teams(cur):
    for c in COUNTRIES:
        cur.execute("INSERT INTO teams (team_name, country) VALUES (?, ?)", (c, c))


def build_venues(cur):
    for v in VENUES:
        cur.execute(
            "INSERT INTO venues (venue_name, city, country, capacity) VALUES (?, ?, ?, ?)", v)


def build_players(cur, per_team=14):
    team_ids = [r[0] for r in cur.execute("SELECT team_id FROM teams").fetchall()]
    used_names = set()
    assignments = team_ids * per_team  # guarantees exactly per_team players per team
    for team_id in assignments:
        while True:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            if name not in used_names:
                used_names.add(name)
                break
        country = cur.execute("SELECT country FROM teams WHERE team_id=?", (team_id,)).fetchone()[0]
        role = random.choice(ROLES)
        bat_style = random.choice(BAT_STYLES)
        bowl_style = None if role == "Batsman" else random.choice(BOWL_STYLES[:-1])
        cur.execute("""INSERT INTO players
            (player_name, country, playing_role, batting_style, bowling_style, team_id)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, country, role, bat_style, bowl_style, team_id))


def build_series(cur):
    start = date(2020, 1, 1)
    series_list = []
    for i in range(8):
        host = random.choice(COUNTRIES)
        mtype = random.choice(FORMATS)
        s_start = start + timedelta(days=random.randint(0, 2100))
        n_matches = random.choice([2, 3, 5])
        cur.execute("""INSERT INTO series (series_name, host_country, match_type, start_date, total_matches)
            VALUES (?, ?, ?, ?, ?)""",
            (f"{host} {mtype} Series {s_start.year}", host, mtype, s_start.isoformat(), n_matches))
        series_list.append(cur.lastrowid)
    return series_list


def build_matches(cur, series_ids, n=140):
    team_ids = [r[0] for r in cur.execute("SELECT team_id FROM teams").fetchall()]
    venue_ids = [r[0] for r in cur.execute("SELECT venue_id FROM venues").fetchall()]
    match_ids = []
    today = date.today()
    for i in range(n):
        t1, t2 = random.sample(team_ids, 2)
        venue = random.choice(venue_ids)
        series_id = random.choice(series_ids)
        fmt = random.choice(FORMATS)
        # spread dates: most historical, ~12 within the last 30 days
        if i < 12:
            m_date = today - timedelta(days=random.randint(0, 29))
        else:
            m_date = today - timedelta(days=random.randint(30, 2100))
        winner = random.choice([t1, t2])
        margin = random.randint(5, 120) if fmt != "T20I" else random.randint(2, 60)
        vtype = random.choice(["runs", "wickets"])
        toss_winner = random.choice([t1, t2])
        toss_decision = random.choice(["bat", "bowl"])
        desc = f"{fmt} - Match {i+1}"
        cur.execute("""INSERT INTO matches
            (series_id, match_description, team1_id, team2_id, venue_id, match_date,
             match_format, winner_team_id, victory_margin, victory_type,
             toss_winner_team_id, toss_decision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (series_id, desc, t1, t2, venue, m_date.isoformat(), fmt,
             winner, margin, vtype, toss_winner, toss_decision))
        match_ids.append((cur.lastrowid, t1, t2, fmt, m_date))
    return match_ids


def build_innings_stats(cur, matches):
    players_by_team = {}
    for pid, tid in cur.execute("SELECT player_id, team_id FROM players").fetchall():
        players_by_team.setdefault(tid, []).append(pid)

    for match_id, t1, t2, fmt, m_date in matches:
        for innings_no, (batting_team, bowling_team) in enumerate([(t1, t2), (t2, t1)], start=1):
            batters = players_by_team.get(batting_team, [])
            bowlers = players_by_team.get(bowling_team, [])
            if not batters or not bowlers:
                continue
            lo = min(6, len(batters))
            hi = min(11, len(batters))
            lineup = random.sample(batters, random.randint(lo, hi)) if hi > 0 else []
            for pos, pid in enumerate(lineup, start=1):
                balls = random.randint(1, 90) if fmt != "Test" else random.randint(1, 220)
                runs = int(balls * random.uniform(0.3, 1.6))
                fours = random.randint(0, max(1, runs // 15))
                sixes = random.randint(0, max(0, runs // 25))
                sr = round((runs / balls) * 100, 2) if balls else 0
                not_out = 1 if random.random() < 0.2 else 0
                dismissal = None if not_out else random.choice(
                    ["Bowled", "Caught", "LBW", "Run Out", "Stumped"])
                cur.execute("""INSERT INTO batting_stats
                    (match_id, player_id, team_id, innings_number, batting_position,
                     runs_scored, balls_faced, fours, sixes, strike_rate, dismissal_type, not_out)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (match_id, pid, batting_team, innings_no, pos, runs, balls,
                     fours, sixes, sr, dismissal, not_out))

            blo = min(4, len(bowlers))
            bhi = min(6, len(bowlers))
            bowl_lineup = random.sample(bowlers, random.randint(blo, bhi)) if bhi > 0 else []
            for pid in bowl_lineup:
                overs = round(random.uniform(2, 10) if fmt != "Test" else random.uniform(5, 30), 1)
                runs_c = int(overs * random.uniform(2.5, 9))
                wkts = random.choices([0, 1, 2, 3, 4, 5], weights=[30, 25, 20, 13, 8, 4])[0]
                econ = round(runs_c / overs, 2) if overs else 0
                cur.execute("""INSERT INTO bowling_stats
                    (match_id, player_id, team_id, overs_bowled, runs_conceded, wickets_taken, economy_rate)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (match_id, pid, bowling_team, overs, runs_c, wkts, econ))

            for pid in random.sample(bowlers, min(3, len(bowlers))):
                catches = random.choices([0, 1, 2], weights=[60, 30, 10])[0]
                stump = random.choices([0, 1], weights=[95, 5])[0]
                if catches or stump:
                    cur.execute("""INSERT INTO fielding_stats (match_id, player_id, catches, stumpings)
                        VALUES (?, ?, ?, ?)""", (match_id, pid, catches, stump))


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    project_root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(project_root, "schema.sql")) as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    cur = conn.cursor()

    build_teams(cur)
    build_venues(cur)
    build_players(cur, per_team=14)
    series_ids = build_series(cur)
    matches = build_matches(cur, series_ids, n=140)
    build_innings_stats(cur, matches)

    conn.commit()
    conn.close()
    print(f"Sample data generated -> {DB_PATH}")


if __name__ == "__main__":
    main()