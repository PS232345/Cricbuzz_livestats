-- Cricbuzz LiveStats — Database Schema
-- SQLite (database-agnostic style; works on Postgres/MySQL with minor type tweaks)

DROP TABLE IF EXISTS fielding_stats;
DROP TABLE IF EXISTS bowling_stats;
DROP TABLE IF EXISTS batting_stats;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name   TEXT NOT NULL UNIQUE,
    country     TEXT NOT NULL
);

CREATE TABLE players (
    player_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name    TEXT NOT NULL,
    country        TEXT NOT NULL,
    playing_role   TEXT NOT NULL,   -- Batsman / Bowler / All-rounder / Wicket-keeper
    batting_style  TEXT,            -- Right-hand bat / Left-hand bat
    bowling_style  TEXT,            -- Right-arm fast / Left-arm orthodox / etc. (NULL for pure batsmen)
    team_id        INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE venues (
    venue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name  TEXT NOT NULL,
    city        TEXT NOT NULL,
    country     TEXT NOT NULL,
    capacity    INTEGER
);

CREATE TABLE series (
    series_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name     TEXT NOT NULL,
    host_country    TEXT NOT NULL,
    match_type      TEXT NOT NULL,  -- Test / ODI / T20I
    start_date      DATE NOT NULL,
    total_matches   INTEGER
);

CREATE TABLE matches (
    match_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id           INTEGER,
    match_description   TEXT,
    team1_id            INTEGER NOT NULL,
    team2_id            INTEGER NOT NULL,
    venue_id            INTEGER NOT NULL,
    match_date          DATE NOT NULL,
    match_format         TEXT NOT NULL, -- Test / ODI / T20I
    winner_team_id       INTEGER,
    victory_margin       INTEGER,
    victory_type         TEXT,          -- runs / wickets
    toss_winner_team_id  INTEGER,
    toss_decision        TEXT,          -- bat / bowl
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (toss_winner_team_id) REFERENCES teams(team_id)
);

CREATE TABLE batting_stats (
    stat_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id         INTEGER NOT NULL,
    player_id        INTEGER NOT NULL,
    team_id          INTEGER NOT NULL,
    innings_number   INTEGER NOT NULL,
    batting_position INTEGER,
    runs_scored      INTEGER DEFAULT 0,
    balls_faced      INTEGER DEFAULT 0,
    fours            INTEGER DEFAULT 0,
    sixes            INTEGER DEFAULT 0,
    strike_rate      REAL,
    dismissal_type   TEXT,
    not_out          INTEGER DEFAULT 0, -- 1 = not out
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE bowling_stats (
    stat_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER NOT NULL,
    player_id       INTEGER NOT NULL,
    team_id         INTEGER NOT NULL,
    overs_bowled    REAL DEFAULT 0,
    runs_conceded   INTEGER DEFAULT 0,
    wickets_taken   INTEGER DEFAULT 0,
    economy_rate    REAL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE fielding_stats (
    stat_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id    INTEGER NOT NULL,
    player_id   INTEGER NOT NULL,
    catches     INTEGER DEFAULT 0,
    stumpings   INTEGER DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_batting_player ON batting_stats(player_id);
CREATE INDEX idx_batting_match ON batting_stats(match_id);
CREATE INDEX idx_bowling_player ON bowling_stats(player_id);
CREATE INDEX idx_bowling_match ON bowling_stats(match_id);
CREATE INDEX idx_players_country ON players(country);
