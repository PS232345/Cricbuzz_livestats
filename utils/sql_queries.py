"""
25 SQL practice queries for the SQL Analytics page.
Each entry: (question_text, sql_string)
"""

BEGINNER = {
    "Q1: Indian players (name, role, batting style, bowling style)": """
        SELECT player_name, playing_role, batting_style, bowling_style
        FROM players WHERE country = 'India';
    """,

    "Q2: Matches in the last 30 days": """
        SELECT m.match_description, t1.team_name AS team1, t2.team_name AS team2,
               v.venue_name, v.city, m.match_date
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE m.match_date >= date('now', '-30 day')
        ORDER BY m.match_date DESC;
    """,

    "Q3: Top 10 run scorers (ODI)": """
        SELECT p.player_name,
               SUM(b.runs_scored) AS total_runs,
               ROUND(SUM(b.runs_scored)*1.0 /
                     NULLIF(SUM(CASE WHEN b.not_out = 0 THEN 1 ELSE 0 END), 0), 2) AS batting_average,
               SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.match_format = 'ODI'
        GROUP BY p.player_id
        ORDER BY total_runs DESC
        LIMIT 10;
    """,

    "Q4: Venues with capacity > 50,000": """
        SELECT venue_name, city, country, capacity
        FROM venues WHERE capacity > 50000
        ORDER BY capacity DESC;
    """,

    "Q5: Match wins per team": """
        SELECT t.team_name, COUNT(*) AS total_wins
        FROM matches m
        JOIN teams t ON m.winner_team_id = t.team_id
        GROUP BY t.team_id
        ORDER BY total_wins DESC;
    """,

    "Q6: Player count by playing role": """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        GROUP BY playing_role
        ORDER BY player_count DESC;
    """,

    "Q7: Highest individual score per format": """
        SELECT m.match_format, MAX(b.runs_scored) AS highest_score
        FROM batting_stats b
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY m.match_format;
    """,

    "Q8: Series started in 2024": """
        SELECT series_name, host_country, match_type, start_date, total_matches
        FROM series
        WHERE strftime('%Y', start_date) = '2024';
    """,
}

INTERMEDIATE = {
    "Q9: All-rounders (>1000 runs AND >50 wickets)": """
        SELECT p.player_name,
               SUM(b.runs_scored) AS total_runs,
               SUM(bw.wickets_taken) AS total_wickets,
               m.match_format
        FROM players p
        JOIN batting_stats b ON p.player_id = b.player_id
        JOIN bowling_stats bw ON p.player_id = bw.player_id AND b.match_id = bw.match_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id, m.match_format
        HAVING total_runs > 1000 AND total_wickets > 50;
    """,

    "Q10: Last 20 completed matches": """
        SELECT m.match_description, t1.team_name AS team1, t2.team_name AS team2,
               tw.team_name AS winner, m.victory_margin, m.victory_type, v.venue_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        JOIN teams tw ON m.winner_team_id = tw.team_id
        JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY m.match_date DESC
        LIMIT 20;
    """,

    "Q11: Cross-format performance comparison": """
        SELECT p.player_name,
               SUM(CASE WHEN m.match_format='Test' THEN b.runs_scored ELSE 0 END) AS test_runs,
               SUM(CASE WHEN m.match_format='ODI' THEN b.runs_scored ELSE 0 END) AS odi_runs,
               SUM(CASE WHEN m.match_format='T20I' THEN b.runs_scored ELSE 0 END) AS t20i_runs,
               ROUND(AVG(b.runs_scored), 2) AS overall_batting_average
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id
        HAVING COUNT(DISTINCT m.match_format) >= 2;
    """,

    "Q12: Home vs away team performance": """
        SELECT t.team_name,
               SUM(CASE WHEN v.country = t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
               SUM(CASE WHEN v.country != t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins
        FROM matches m
        JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
        JOIN venues v ON m.venue_id = v.venue_id
        GROUP BY t.team_id
        ORDER BY home_wins DESC;
    """,

    "Q13: Batting partnerships >= 100 runs": """
        SELECT p1.player_name AS batter_1, p2.player_name AS batter_2,
               (b1.runs_scored + b2.runs_scored) AS partnership_runs,
               b1.innings_number
        FROM batting_stats b1
        JOIN batting_stats b2
          ON b1.match_id = b2.match_id
         AND b1.innings_number = b2.innings_number
         AND b2.batting_position = b1.batting_position + 1
        JOIN players p1 ON b1.player_id = p1.player_id
        JOIN players p2 ON b2.player_id = p2.player_id
        WHERE (b1.runs_scored + b2.runs_scored) >= 100
        ORDER BY partnership_runs DESC;
    """,

    "Q14: Bowling performance at venues (>=3 matches, >=4 overs each)": """
        SELECT p.player_name, v.venue_name,
               ROUND(AVG(bw.economy_rate), 2) AS avg_economy,
               SUM(bw.wickets_taken) AS total_wickets,
               COUNT(DISTINCT bw.match_id) AS matches_played
        FROM bowling_stats bw
        JOIN players p ON bw.player_id = p.player_id
        JOIN matches m ON bw.match_id = m.match_id
        JOIN venues v ON m.venue_id = v.venue_id
        WHERE bw.overs_bowled >= 4
        GROUP BY p.player_id, v.venue_id
        HAVING matches_played >= 3
        ORDER BY total_wickets DESC;
    """,

    "Q15: Performance in close matches": """
        SELECT p.player_name,
               ROUND(AVG(b.runs_scored), 2) AS avg_runs_close_matches,
               COUNT(DISTINCT m.match_id) AS close_matches_played,
               SUM(CASE WHEN m.winner_team_id = b.team_id THEN 1 ELSE 0 END) AS close_matches_won
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
           OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
        GROUP BY p.player_id
        ORDER BY avg_runs_close_matches DESC;
    """,

    "Q16: Yearly batting trend (since 2020)": """
        SELECT p.player_name, strftime('%Y', m.match_date) AS year,
               ROUND(AVG(b.runs_scored), 2) AS avg_runs,
               ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.match_date >= '2020-01-01'
        GROUP BY p.player_id, year
        HAVING COUNT(*) >= 5
        ORDER BY p.player_name, year;
    """,
}

ADVANCED = {
    "Q17: Toss impact on match outcome": """
        SELECT m.toss_decision,
               ROUND(100.0 * SUM(CASE WHEN m.toss_winner_team_id = m.winner_team_id THEN 1 ELSE 0 END)
                     / COUNT(*), 2) AS win_pct_after_winning_toss
        FROM matches m
        GROUP BY m.toss_decision;
    """,

    "Q18: Most economical limited-overs bowlers": """
        SELECT p.player_name,
               ROUND(SUM(bw.runs_conceded)*1.0 / NULLIF(SUM(bw.overs_bowled),0), 2) AS economy_rate,
               SUM(bw.wickets_taken) AS total_wickets,
               COUNT(DISTINCT bw.match_id) AS matches_played
        FROM bowling_stats bw
        JOIN players p ON bw.player_id = p.player_id
        JOIN matches m ON bw.match_id = m.match_id
        WHERE m.match_format IN ('ODI', 'T20I')
        GROUP BY p.player_id
        HAVING matches_played >= 10 AND (SUM(bw.overs_bowled)*1.0 / matches_played) >= 2
        ORDER BY economy_rate ASC;
    """,

    "Q19: Most consistent batsmen (since 2022)": """
        SELECT p.player_name,
               ROUND(AVG(b.runs_scored), 2) AS avg_runs,
               ROUND(
                 SQRT(AVG(b.runs_scored * b.runs_scored) - AVG(b.runs_scored) * AVG(b.runs_scored)), 2
               ) AS stddev_runs
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        WHERE b.balls_faced >= 10 AND m.match_date >= '2022-01-01'
        GROUP BY p.player_id
        ORDER BY stddev_runs ASC;
    """,

    "Q20: Format-wise matches & averages (>=20 total matches)": """
        SELECT p.player_name,
               SUM(CASE WHEN m.match_format='Test' THEN 1 ELSE 0 END) AS test_matches,
               SUM(CASE WHEN m.match_format='ODI' THEN 1 ELSE 0 END) AS odi_matches,
               SUM(CASE WHEN m.match_format='T20I' THEN 1 ELSE 0 END) AS t20i_matches,
               ROUND(AVG(CASE WHEN m.match_format='Test' THEN b.runs_scored END), 2) AS test_avg,
               ROUND(AVG(CASE WHEN m.match_format='ODI' THEN b.runs_scored END), 2) AS odi_avg,
               ROUND(AVG(CASE WHEN m.match_format='T20I' THEN b.runs_scored END), 2) AS t20i_avg
        FROM batting_stats b
        JOIN players p ON b.player_id = p.player_id
        JOIN matches m ON b.match_id = m.match_id
        GROUP BY p.player_id
        HAVING (test_matches + odi_matches + t20i_matches) >= 20;
    """,

    "Q21: Composite player performance ranking": """
        SELECT p.player_name, m.match_format,
               ROUND(SUM(b.runs_scored) * 0.01
                   + AVG(b.runs_scored) * 0.5
                   + AVG(b.strike_rate) * 0.3, 2) AS batting_points,
               ROUND(SUM(bw.wickets_taken) * 2
                   + (50 - COALESCE(AVG(bw.runs_conceded * 1.0 / NULLIF(bw.wickets_taken,0)), 50)) * 0.5
                   + (6 - AVG(bw.economy_rate)) * 2, 2) AS bowling_points,
               ROUND(SUM(f.catches) * 3 + SUM(f.stumpings) * 5, 2) AS fielding_points
        FROM players p
        LEFT JOIN batting_stats b ON p.player_id = b.player_id
        LEFT JOIN bowling_stats bw ON p.player_id = bw.player_id AND b.match_id = bw.match_id
        LEFT JOIN fielding_stats f ON p.player_id = f.player_id AND b.match_id = f.match_id
        LEFT JOIN matches m ON b.match_id = m.match_id
        WHERE m.match_format IS NOT NULL
        GROUP BY p.player_id, m.match_format
        ORDER BY m.match_format, batting_points DESC;
    """,

    "Q22: Head-to-head team analysis (last 3 years, >=5 matches)": """
        SELECT t1.team_name AS team_a, t2.team_name AS team_b,
               COUNT(*) AS total_matches,
               SUM(CASE WHEN m.winner_team_id = m.team1_id THEN 1 ELSE 0 END) AS team_a_wins,
               SUM(CASE WHEN m.winner_team_id = m.team2_id THEN 1 ELSE 0 END) AS team_b_wins,
               ROUND(AVG(m.victory_margin), 2) AS avg_victory_margin
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        WHERE m.match_date >= date('now', '-3 years')
        GROUP BY m.team1_id, m.team2_id
        HAVING total_matches >= 5;
    """,

    "Q23: Recent player form & momentum": """
        WITH ranked AS (
            SELECT b.player_id, b.runs_scored, m.match_date,
                   ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS rn
            FROM batting_stats b JOIN matches m ON b.match_id = m.match_id
        )
        SELECT p.player_name,
               ROUND(AVG(CASE WHEN rn <= 5 THEN runs_scored END), 2) AS avg_last_5,
               ROUND(AVG(CASE WHEN rn <= 10 THEN runs_scored END), 2) AS avg_last_10,
               SUM(CASE WHEN rn <= 10 AND runs_scored > 50 THEN 1 ELSE 0 END) AS scores_above_50,
               CASE
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 45 THEN 'Excellent Form'
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 30 THEN 'Good Form'
                   WHEN AVG(CASE WHEN rn <= 5 THEN runs_scored END) >= 15 THEN 'Average Form'
                   ELSE 'Poor Form'
               END AS form_category
        FROM ranked r
        JOIN players p ON r.player_id = p.player_id
        WHERE rn <= 10
        GROUP BY p.player_id;
    """,

    "Q24: Best batting partnerships (>=5 partnerships)": """
        SELECT p1.player_name AS batter_1, p2.player_name AS batter_2,
               ROUND(AVG(b1.runs_scored + b2.runs_scored), 2) AS avg_partnership_runs,
               SUM(CASE WHEN (b1.runs_scored + b2.runs_scored) > 50 THEN 1 ELSE 0 END) AS partnerships_over_50,
               MAX(b1.runs_scored + b2.runs_scored) AS highest_partnership,
               COUNT(*) AS total_partnerships,
               ROUND(100.0 * SUM(CASE WHEN (b1.runs_scored + b2.runs_scored) > 50 THEN 1 ELSE 0 END)
                     / COUNT(*), 2) AS success_rate_pct
        FROM batting_stats b1
        JOIN batting_stats b2
          ON b1.match_id = b2.match_id AND b1.innings_number = b2.innings_number
         AND b2.batting_position = b1.batting_position + 1
        JOIN players p1 ON b1.player_id = p1.player_id
        JOIN players p2 ON b2.player_id = p2.player_id
        GROUP BY p1.player_id, p2.player_id
        HAVING total_partnerships >= 5
        ORDER BY avg_partnership_runs DESC;
    """,

    "Q25: Career trajectory (quarterly time-series)": """
        WITH quarterly AS (
            SELECT b.player_id,
                   strftime('%Y', m.match_date) || '-Q' ||
                   ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1) AS quarter,
                   AVG(b.runs_scored) AS avg_runs,
                   AVG(b.strike_rate) AS avg_sr,
                   COUNT(*) AS matches_in_quarter
            FROM batting_stats b JOIN matches m ON b.match_id = m.match_id
            GROUP BY b.player_id, quarter
            HAVING matches_in_quarter >= 3
        )
        SELECT p.player_name, q.quarter, q.avg_runs, q.avg_sr,
               CASE
                 WHEN q.avg_runs > LAG(q.avg_runs) OVER (PARTITION BY q.player_id ORDER BY q.quarter) THEN 'Improving'
                 WHEN q.avg_runs < LAG(q.avg_runs) OVER (PARTITION BY q.player_id ORDER BY q.quarter) THEN 'Declining'
                 ELSE 'Stable'
               END AS trend
        FROM quarterly q
        JOIN players p ON q.player_id = p.player_id
        ORDER BY p.player_name, q.quarter;
    """,
}

ALL_QUERIES = {"Beginner": BEGINNER, "Intermediate": INTERMEDIATE, "Advanced": ADVANCED}
