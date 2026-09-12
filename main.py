import streamlit as st
from utils.theme import inject_css, hero, INK, MUTED, CARD, PAPER_LINE

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")
inject_css()

hero("Cricbuzz LiveStats", "Match Analytics Dashboard",
     "SEASON 2026 · LIVE SCORES · 25 SQL ANALYSES · FULL CRUD")

st.markdown(f"""
<p style="max-width:640px; line-height:1.6;">
A cricket analytics dashboard that integrates the <b>Cricbuzz API</b> with a <b>SQL
database</b> to deliver real-time match updates, player statistics, SQL-driven
analytics, and full CRUD operations — laid out like a scorer's ledger.
</p>
""", unsafe_allow_html=True)

st.write("")
pages = [
    ("🔴", "Live Match", "pages/1_Live_Match.py", "Live scores, status and venue details from the Cricbuzz API."),
    ("📊", "Top Player Stats", "pages/2_Top_Player_Stats.py", "Batting and bowling leaderboards."),
    ("🧮", "SQL Analytics", "pages/3_SQL_Analytics.py", "25 practice queries, run live against the local DB."),
    ("🛠️", "CRUD Operations", "pages/4_CRUD_Operations.py", "Add, update, delete player records."),
]
cols = st.columns(4)
for col, (icon, label, target, desc) in zip(cols, pages):
    with col:
        st.markdown(f"""
        <div class="scorecard" style="min-height:150px;">
            <div style="font-size:22px;">{icon}</div>
            <div style="font-family:'Spectral',serif; font-weight:600; font-size:17px; margin:6px 0 4px 0;">{label}</div>
            <div style="font-size:13px; color:{MUTED}; line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(target, label=f"Open {label}", icon="➡️")

st.divider()

with st.expander("⚙️ Setup instructions"):
    st.markdown("""
    1. `pip install -r requirements.txt`
    2. `python generate_sample_data.py` — builds and seeds the local database
    3. *(Optional)* `export CRICBUZZ_API_KEY="your_key"` for live data — without it,
       Live Match / Top Player Stats show clearly-labeled sample data.
    4. `streamlit run main.py`
    """)

st.markdown(f"""
<p style="font-family:'IBM Plex Mono',monospace; font-size:12px; color:{MUTED}; margin-top:8px;">
TECH — Python · Streamlit · SQLite · Cricbuzz REST API · pandas · requests
</p>
""", unsafe_allow_html=True)
