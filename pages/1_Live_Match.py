import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import get_live_matches
from utils.theme import inject_css, hero, MUTED

st.set_page_config(page_title="Live Match", page_icon="🔴", layout="wide")
inject_css()
hero("Live Match", "Matchday", "LIVE SCORES · SCORECARDS · VENUE DETAILS")

c1, c2 = st.columns([1, 5])
with c1:
    if st.button("↻ Refresh"):
        st.rerun()

matches, source = get_live_matches()
with c2:
    if source != "live":
        st.markdown(f"<span class='eyebrow'>sample data ({source}) — set CRICBUZZ_API_KEY for live feed</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='eyebrow'>live — cricbuzz api</span>", unsafe_allow_html=True)

st.write("")

def classify(status: str) -> str:
    s = status.lower()
    if "won" in s or "drawn" in s or "abandoned" in s:
        return "completed"
    if "starts" in s or "upcoming" in s:
        return "upcoming"
    return "live"

if not matches:
    st.info("No matches found.")
else:
    for m in matches:
        state = classify(m.get("status", ""))
        css_class = "live" if state == "live" else ("upcoming" if state == "upcoming" else "")
        dot = "live-dot" if state == "live" else ""
        st.markdown(f"""
        <div class="scorecard {css_class}">
            <div class="status-tag {dot}">{state}  ·  {m.get('format','-')}</div>
            <div style="font-family:'Spectral',serif; font-size:20px; font-weight:600; margin:4px 0 2px 0;">
                {m.get('team1','?')} <span style="color:{MUTED}; font-weight:400;">vs</span> {m.get('team2','?')}
            </div>
            <div style="font-size:13px; color:{MUTED}; margin-bottom:6px;">{m.get('series','')}</div>
            <div style="font-family:'IBM Plex Mono',monospace; font-size:13px;">{m.get('status','')}</div>
            <div style="font-size:12px; color:{MUTED}; margin-top:6px;">📍 {m.get('venue','')}</div>
        </div>
        """, unsafe_allow_html=True)
