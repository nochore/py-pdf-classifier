"""UI Custom Styling for Document AI Dashboard."""

import streamlit as st

FAANG_CSS = """
<style>
    /* Typography & Global Layout Alignment */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Dynamic Theme-Aware Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Highlighting Badge styling for Playwright verification */
    .highlight-match {
        background-color: #fef08a;
        color: #854d0e;
        padding: 2px 4px;
        border-radius: 4px;
        font-weight: 600;
    }

    /* Primary Accent Styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
    }

    .stButton > button[kind="primary"] {
        background-color: #2563eb;
        color: #ffffff;
        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8;
        color: #ffffff;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 8px 16px;
    }

    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
"""


def apply_custom_styles() -> None:
    """Inject custom FAANG styling into Streamlit application."""
    st.markdown(FAANG_CSS, unsafe_allow_html=True)
