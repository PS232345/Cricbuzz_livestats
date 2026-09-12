import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import get_top_batting_stats, get_top_bowling_stats
from utils.theme import inject_css, hero, MUTED, INK

st.set_page_config(page_title="Top Player Stats", page_icon="📊", layout="wide")
inject_css()
hero("Top Player Stats", "Leaderboard", "BATTING · BOWLING · CAREER LEADERS")


def leaderboard(rows, cols):
    """cols: list of (key, label) in display order, first is the name."""
    for i, r in enumerate(rows, start=1):
        badge_class = "gold" if i <= 3 else ""
        stats = "  ·  ".join(f"{label}: {r.get(key,'-')}" for key, label in cols[1:])
        st.markdown(f"""
        <div class="scorecard" style="padding:10px 16px; display:flex; align-items:center;">
            <span class="rank-badge {badge_class}">{i}</span>
            <span style="font-family:'Spectral',serif; font-weight:600; font-size:16px; margin-right:14px;">
                {r.get(cols[0][0], '-')}
            </span>
            <span style="font-family:'IBM Plex Mono',monospace; font-size:13px; color:{MUTED};">{stats}</span>
        </div>
        """, unsafe_allow_html=True)


tab1, tab2 = st.tabs(["🏏 Batting", "🎯 Bowling"])

with tab1:
    data, source = get_top_batting_stats()
    if source != "live":
        st.markdown(f"<span class='eyebrow'>sample data ({source})</span>", unsafe_allow_html=True)
    st.write("")
    if data:
        leaderboard(data, [("player", ""), ("runs", "Runs"), ("average", "Avg"), ("centuries", "100s")])
    with st.expander("Raw table"):
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

with tab2:
    data, source = get_top_bowling_stats()
    if source != "live":
        st.markdown(f"<span class='eyebrow'>sample data ({source})</span>", unsafe_allow_html=True)
    st.write("")
    if data:
        leaderboard(data, [("player", ""), ("wickets", "Wkts"), ("economy", "Econ")])
    with st.expander("Raw table"):
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
