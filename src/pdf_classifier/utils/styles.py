"""UI Custom Styling for Precision Slate Document AI Dashboard."""

import streamlit as st

PRECISION_SLATE_CSS = """
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* Global Typography & Palette Defaults */
    html, body, [class*="css"], .stApp {
        font-family: 'Geist', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #0b141c !important;
        color: #dae3ee !important;
    }

    /* Reduce Streamlit Default Top & Bottom Spacing */
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        max-width: 100% !important;
    }

    /* Hide Default Streamlit Chrome & Headers */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
        display: none !important;
    }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    div[data-testid="stDecoration"] { display: none !important; }

    /* Custom Top Navigation Bar */
    .precision-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: rgba(20, 28, 36, 0.95);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #222f3d;
        padding: 8px 16px;
        margin: -1.0rem -1.25rem 1.0rem -1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .precision-header-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .precision-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #141c24;
        border: 1px solid #222f3d;
        padding: 3px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #dae3ee;
    }

    /* Sidebar Custom Styling */
    [data-testid="stSidebar"] {
        background-color: #0e1620 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }

    /* Cards and Containers */
    .slate-card {
        background-color: #141c24;
        border: 1px solid #222f3d;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }

    .slate-card-sm {
        background-color: #182028;
        border: 1px solid #222f3d;
        border-radius: 6px;
        padding: 10px 12px;
    }

    /* Metric Badges & Confidence Chips */
    .badge-secondary {
        background-color: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.25);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 500;
    }

    .badge-primary {
        background-color: rgba(59, 130, 246, 0.12);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.25);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 500;
    }

    .badge-tertiary {
        background-color: rgba(245, 158, 11, 0.12);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.25);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #2563eb !important;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #141c24;
        padding: 4px;
        border-radius: 6px;
        border: 1px solid #222f3d;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 4px !important;
        padding: 6px 14px !important;
        font-size: 12px !important;
        color: #94a3b8 !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #222b33 !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* Radio Segmented Switcher Styling */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        background-color: #141c24 !important;
        padding: 3px !important;
        border-radius: 6px !important;
        border: 1px solid #222f3d !important;
        gap: 4px !important;
    }

    div[data-testid="stRadio"] label {
        padding: 4px 12px !important;
        border-radius: 4px !important;
        font-size: 12px !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] {
        background-color: #222b33 !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* Monospace Code & Schema Panels */
    pre, code, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #060f16 !important;
        border-radius: 6px !important;
        border: 1px solid #222f3d !important;
    }

    /* Highlight badge for text search */
    .highlight-match {
        background-color: #fef08a;
        color: #854d0e;
        padding: 2px 4px;
        border-radius: 4px;
        font-weight: 600;
    }

    /* Bottom Telemetry Footer Dock */
    .footer-dock {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 28px;
        z-index: 999;
        background-color: #060f16;
        border-top: 1px solid #222f3d;
        padding: 0 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #64748b;
    }

    .online-dot {
        color: #10b981;
        font-weight: 600;
    }
</style>
"""

FAANG_CSS = PRECISION_SLATE_CSS


def apply_custom_styles() -> None:
    """Inject custom Precision Slate styling into Streamlit application."""
    st.markdown(PRECISION_SLATE_CSS, unsafe_allow_html=True)
