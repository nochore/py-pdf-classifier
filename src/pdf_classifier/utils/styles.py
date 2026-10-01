"""Precision Slate styling: compact CSS layer plus small HTML helpers."""

from html import escape

import streamlit as st

PRECISION_SLATE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --canvas:#0b141c; --surface:#141c24; --surface-hi:#1a2430; --line:#222f3d;
    --text:#f1f5f9; --text-2:#94a3b8; --text-3:#64748b;
    --accent:#3b82f6; --ok:#10b981; --warn:#f59e0b;
    --mono:'JetBrains Mono',ui-monospace,monospace;
}
html, body, .stApp { font-family:'Geist',system-ui,sans-serif; background:var(--canvas); color:#dae3ee; }
.block-container { padding:3.25rem 1.5rem 3.5rem !important; max-width:100% !important; }
header[data-testid="stHeader"] { background:transparent; }
#MainMenu, footer, div[data-testid="stDecoration"] { visibility:hidden; display:none; }

/* Sidebar */
[data-testid="stSidebar"] { background:#0e1620; border-right:1px solid rgba(255,255,255,.07); }
[data-testid="stSidebar"] .block-container, [data-testid="stSidebarUserContent"] { padding-top:1.25rem !important; }
[data-testid="stFileUploader"] section { padding:.75rem; border:1px dashed var(--line); background:var(--surface); border-radius:8px; }
[data-testid="stFileUploader"] small { display:none; }

/* Bordered containers become slate cards */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) {
    border-color:var(--line) !important; border-radius:8px !important; background:var(--surface);
}

/* Type helpers */
.eyebrow { font:500 10px var(--mono); letter-spacing:.06em; text-transform:uppercase; color:var(--text-3); margin:.25rem 0 .4rem; }
.mono { font-family:var(--mono); }
.brand { display:flex; align-items:center; gap:10px; height:38px; font-weight:700; font-size:15px; color:var(--text); }
.brand-mark { background:rgba(59,130,246,.18); color:var(--accent); border-radius:6px; padding:3px 7px; font-size:13px; }
.pill { display:inline-flex; align-items:center; gap:6px; font:400 11px var(--mono); color:var(--text-2);
    background:var(--surface); border:1px solid var(--line); border-radius:999px; padding:3px 10px; max-width:100%;
    overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.dot { width:7px; height:7px; border-radius:50%; background:var(--ok); display:inline-block; }
.dot.off { background:var(--text-3); }
.panel-title { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.5rem; }
.panel-title b { font-size:14px; color:var(--text); font-weight:600; }
.panel-title span { font:400 11px var(--mono); color:var(--text-3); }
.kpi { background:var(--surface-hi); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }
.kpi .l { font:500 10px var(--mono); letter-spacing:.05em; text-transform:uppercase; color:var(--text-3); }
.kpi .v { font:600 20px var(--mono); color:var(--text); margin:2px 0; }
.kpi .s { font:400 11px var(--mono); color:var(--text-2); }
.kpi .s.ok { color:var(--ok); }
.row { display:flex; justify-content:space-between; align-items:center; gap:8px; padding:7px 10px;
    background:var(--surface-hi); border-radius:6px; margin-bottom:6px; font-size:13px; color:var(--text); }
.row small { font-size:11px; color:var(--text-3); display:block; }
.row .mono { font-size:12px; }
.chip { background:rgba(16,185,129,.12); color:var(--ok); border:1px solid rgba(16,185,129,.25);
    border-radius:4px; padding:1px 6px; font:500 10px var(--mono); }
.summary { font-size:13px; line-height:1.65; color:#c2c6d6; background:var(--surface-hi); padding:12px; border-radius:6px; }
.empty { text-align:center; color:var(--text-3); font-size:12px; padding:28px 12px;
    border:1px dashed var(--line); border-radius:8px; }
.bubble-cite { margin-top:6px; font:400 10px var(--mono); color:var(--accent); }
.highlight-match { background:#fef08a; color:#854d0e; padding:1px 4px; border-radius:4px; font-weight:600; }

/* Buttons & segmented control */
.stButton > button, .stDownloadButton > button { border-radius:6px; font-size:12px; font-weight:500; min-height:2.1rem; }
.stButton > button[kind="primary"] { background:var(--accent); border:none; color:#fff; }
.stButton > button[kind="primary"]:hover { background:#2563eb; }
[data-testid="stSegmentedControl"] { justify-content:center; }
.stTabs [data-baseweb="tab-list"] { gap:4px; }
.stTabs [data-baseweb="tab"] { font-size:12px; padding:6px 12px; }
pre, code { font-family:var(--mono) !important; font-size:12px !important; }

/* Footer dock */
.footer-dock { position:fixed; left:0; right:0; bottom:0; height:28px; z-index:999; padding:0 16px;
    display:flex; align-items:center; justify-content:space-between; background:#060f16;
    border-top:1px solid var(--line); font:400 11px var(--mono); color:var(--text-3); }
.footer-dock b { color:var(--text); font-weight:500; }
.online-dot { color:var(--ok); font-weight:600; }
</style>
"""

FAANG_CSS = PRECISION_SLATE_CSS


def apply_custom_styles() -> None:
    """Inject the Precision Slate CSS layer."""
    st.markdown(PRECISION_SLATE_CSS, unsafe_allow_html=True)


def html(markup: str) -> None:
    """Render trusted HTML markup."""
    st.markdown(markup, unsafe_allow_html=True)


def panel_title(title: str, meta: str = "") -> None:
    """Render a card heading with optional right-aligned meta text."""
    html(f'<div class="panel-title"><b>{escape(title)}</b><span>{escape(meta)}</span></div>')


def kpi(label: str, value: str, sub: str = "", ok: bool = False) -> str:
    """Return HTML for a single KPI tile."""
    cls = "s ok" if ok else "s"
    return (
        f'<div class="kpi"><div class="l">{escape(label)}</div>'
        f'<div class="v">{escape(value)}</div><div class="{cls}">{escape(sub)}</div></div>'
    )


def kpi_row(items: list[tuple[str, str, str, bool]]) -> None:
    """Render KPI tiles evenly across a row."""
    cols = st.columns(len(items), gap="small")
    for col, (label, value, sub, ok) in zip(cols, items, strict=True):
        with col:
            html(kpi(label, value, sub, ok))


def empty_state(message: str) -> None:
    """Render a muted placeholder block."""
    html(f'<div class="empty">{escape(message)}</div>')
