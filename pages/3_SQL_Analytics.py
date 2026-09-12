import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import run_query
from utils.sql_queries import ALL_QUERIES
from utils.theme import inject_css, hero, MUTED

st.set_page_config(page_title="SQL Analytics", page_icon="🧮", layout="wide")
inject_css()
hero("SQL Queries & Analytics", "Scorebook", "25 QUERIES · BEGINNER → ADVANCED")

c1, c2 = st.columns(2)
with c1:
    level = st.selectbox("Difficulty level", list(ALL_QUERIES.keys()))
with c2:
    questions = ALL_QUERIES[level]
    question = st.selectbox("Question", list(questions.keys()))

sql = questions[question]
with st.expander("View SQL"):
    st.code(sql.strip(), language="sql")

st.write("")
try:
    df = run_query(sql)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown(f"<span class='eyebrow'>{len(df)} rows returned</span>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Query failed: {e}")
    st.info("Make sure you've run `python generate_sample_data.py` first.")
