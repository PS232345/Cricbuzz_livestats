"""
Shared visual identity for the whole app: a cricket scorebook aesthetic —
ruled ivory paper, navy 'ink', a grass-green pencil for live/positive marks,
a wicket-red pencil for outs/alerts, and tabular monospace for every number
(the way a scorer fills a grid).
"""
import streamlit as st

INK = "#1B2A4A"
PAPER = "#F6F1E4"
PAPER_LINE = "#E4DCC8"
CARD = "#FFFDF7"
WICKET_RED = "#A23B3B"
GRASS = "#3B6E45"
BRASS = "#B8860B"
MUTED = "#6B6355"


def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600&family=Inter:wght@400;500;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {PAPER};
        background-image: repeating-linear-gradient(to bottom, transparent, transparent 27px, {PAPER_LINE} 28px);
        color: {INK};
        font-family: 'Inter', sans-serif;
    }}
    [data-testid="stHeader"] {{ background: transparent; }}

    [data-testid="stSidebar"] {{
        background-color: {INK};
        background-image: none;
    }}
    [data-testid="stSidebar"] * {{ color: #EDE7D8 !important; }}
    [data-testid="stSidebarNav"] a {{ font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; }}

    h1, h2, h3 {{ font-family: 'Spectral', serif !important; color: {INK}; }}
    h1 {{ font-weight: 700 !important; }}

    [data-testid="stMetricValue"] {{ font-family: 'IBM Plex Mono', monospace; color: {INK}; }}
    [data-testid="stMetricLabel"] {{ font-family: 'IBM Plex Mono', monospace; color: {MUTED}; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}

    [data-testid="stDataFrame"] {{ font-family: 'IBM Plex Mono', monospace; }}

    div[data-baseweb="tab-list"] {{ border-bottom: 1px solid {PAPER_LINE}; }}

    .eyebrow {{
        display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px;
        padding: 2px 8px; border: 1px solid {MUTED}88; color: {MUTED};
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px;
    }}
    .scorecard {{
        border: 1px solid {MUTED}44; border-left: 4px solid {GRASS};
        background: {CARD}; padding: 14px 18px; margin-bottom: 12px;
    }}
    .scorecard.live {{ border-left-color: {WICKET_RED}; }}
    .scorecard.upcoming {{ border-left-color: {BRASS}; }}
    .scorecard .status-tag {{
        font-family: 'IBM Plex Mono', monospace; font-size: 11px; text-transform: uppercase;
        letter-spacing: 1px; color: {MUTED};
    }}
    .status-tag.live-dot::before {{ content: "\\25CF "; color: {WICKET_RED}; }}
    .rank-badge {{
        display: inline-block; width: 26px; height: 26px; text-align: center; line-height: 26px;
        border-radius: 50%; font-family: 'IBM Plex Mono', monospace; font-weight: 600; font-size: 13px;
        background: {INK}; color: {PAPER}; margin-right: 10px;
    }}
    .rank-badge.gold {{ background: {BRASS}; }}
    hr {{ border-top: 1px solid {PAPER_LINE}; }}
    </style>
    """, unsafe_allow_html=True)


def hero(title: str, eyebrow: str, subtitle: str):
    st.markdown(f"""
    <div style="border-bottom:2px solid {INK}; padding-bottom:16px; margin-bottom:22px;">
        <span class="eyebrow">{eyebrow}</span>
        <h1 style="font-size:40px; margin:6px 0 2px 0;">{title}</h1>
        <p style="font-family:'IBM Plex Mono', monospace; color:{MUTED}; font-size:13px; margin:0;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
