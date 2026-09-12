import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import run_query, execute_write
from utils.theme import inject_css, hero

st.set_page_config(page_title="CRUD Operations", page_icon="🛠️", layout="wide")
inject_css()
hero("CRUD Operations", "Team Sheet", "ADD · UPDATE · DELETE PLAYER RECORDS")

tab_view, tab_add, tab_update, tab_delete = st.tabs(
    ["📋 View", "➕ Add", "✏️ Update", "🗑️ Delete"])

ROLES = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
BAT_STYLES = ["Right-hand bat", "Left-hand bat"]

with tab_view:
    df = run_query("SELECT * FROM players ORDER BY player_id DESC")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_add:
    with st.form("add_player"):
        name = st.text_input("Player name")
        country = st.text_input("Country")
        role = st.selectbox("Playing role", ROLES)
        bat_style = st.selectbox("Batting style", BAT_STYLES)
        bowl_style = st.text_input("Bowling style (leave blank for pure batsman)")
        submitted = st.form_submit_button("Add player")
        if submitted:
            if not name or not country:
                st.error("Name and country are required.")
            else:
                execute_write(
                    """INSERT INTO players (player_name, country, playing_role, batting_style, bowling_style)
                       VALUES (?, ?, ?, ?, ?)""",
                    (name, country, role, bat_style, bowl_style or None))
                st.success(f"Added {name}.")
                st.rerun()

with tab_update:
    df = run_query("SELECT player_id, player_name FROM players ORDER BY player_id")
    if df.empty:
        st.info("No players yet.")
    else:
        options = dict(zip(df["player_name"] + " (#" + df["player_id"].astype(str) + ")", df["player_id"]))
        choice = st.selectbox("Select player", list(options.keys()))
        pid = options[choice]
        current = run_query("SELECT * FROM players WHERE player_id = ?", (pid,)).iloc[0]
        with st.form("update_player"):
            name = st.text_input("Player name", value=current["player_name"])
            country = st.text_input("Country", value=current["country"])
            role = st.selectbox("Playing role", ROLES, index=ROLES.index(current["playing_role"])
                                 if current["playing_role"] in ROLES else 0)
            submitted = st.form_submit_button("Update player")
            if submitted:
                execute_write(
                    "UPDATE players SET player_name=?, country=?, playing_role=? WHERE player_id=?",
                    (name, country, role, int(pid)))
                st.success("Updated.")
                st.rerun()

with tab_delete:
    df = run_query("SELECT player_id, player_name FROM players ORDER BY player_id")
    if df.empty:
        st.info("No players yet.")
    else:
        options = dict(zip(df["player_name"] + " (#" + df["player_id"].astype(str) + ")", df["player_id"]))
        choice = st.selectbox("Select player to delete", list(options.keys()), key="del_select")
        pid = options[choice]
        if st.button("🗑️ Delete player", type="primary"):
            execute_write("DELETE FROM players WHERE player_id=?", (int(pid),))
            st.success("Deleted.")
            st.rerun()
