"""Main Streamlit application entry point for Document AI Enterprise Parser."""

from html import escape

import streamlit as st

from pdf_classifier.components import (
    render_chat_workspace,
    render_raw_schema,
    render_sidebar,
    render_split_inspector,
)
from pdf_classifier.utils import apply_custom_styles, init_session_state
from pdf_classifier.utils.styles import empty_state, html

VIEWS = ["Split Inspector", "Q&A Chat", "Raw Schema"]


def render_header(model_name: str) -> None:
    """Render the top bar: brand + file badge, view switcher, engine status."""
    doc = st.session_state.uploaded_file_name
    left, center, right = st.columns([3, 4, 3], gap="small", vertical_alignment="center")

    with left:
        badge = (
            f'<span class="pill"><span class="dot"></span>{escape(doc)}</span>'
            if doc
            else '<span class="pill"><span class="dot off"></span>no document</span>'
        )
        html(
            '<div class="brand"><span class="brand-mark">▤</span>Document AI'
            f"<span style='width:1px;height:16px;background:var(--line)'></span>{badge}</div>"
        )

    with center:
        selected = st.segmented_control(
            "View",
            VIEWS,
            default=st.session_state.active_view,
            label_visibility="collapsed",
            key="view_switcher",
        )
        if selected:
            st.session_state.active_view = selected

    with right:
        html(
            '<div style="display:flex;justify-content:flex-end">'
            f'<span class="pill"><span class="dot"></span>Ollama: {escape(model_name)}</span></div>'
        )


def render_status_bar(model_name: str) -> None:
    """Render the bottom status dock using real session telemetry."""
    metrics = st.session_state.doc_metrics
    latency = st.session_state.latency_ms
    parts = [f"Model: <b>{escape(model_name)}</b>"]
    if metrics:
        parts.append(f"Pages: <b>{metrics.get('page_count', 0)}</b>")
        parts.append(f"Words: <b>{metrics.get('word_count', 0):,}</b>")
    if latency is not None:
        parts.append(f"Last inference: <b>{latency} ms</b>")
    html(
        f'<div class="footer-dock"><div>{" • ".join(parts)}</div>'
        '<div class="online-dot">● Local offline engine</div></div>'
    )


def main() -> None:
    """Initialize and run the Streamlit Document AI application."""
    st.set_page_config(
        page_title="Document AI Enterprise Parser",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_custom_styles()
    init_session_state()

    model_name = render_sidebar()
    render_header(model_name)

    if st.session_state.extracted_text:
        view = st.session_state.active_view
        if view == "Q&A Chat":
            render_chat_workspace(model_name)
        elif view == "Raw Schema":
            render_raw_schema()
        else:
            render_split_inspector()
    else:
        empty_state(
            "System Ready. Please upload a PDF document in the sidebar "
            "configuration panel to initialize analysis."
        )

    render_status_bar(model_name)


if __name__ == "__main__":
    main()
