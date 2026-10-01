"""Split Inspector component (View 1): PDF canvas and AI intelligence console."""

import json
from html import escape

import streamlit as st

from pdf_classifier.components.export_view import build_extraction_payload, detect_entities
from pdf_classifier.services.pdf_service import render_pdf_page_cached
from pdf_classifier.utils.styles import empty_state, html, kpi_row, panel_title


def render_pdf_stage(page_key: str, zoom_key: str, default_zoom: float = 2.0) -> None:
    """Render the PDF toolbar and page canvas (shared by inspector and chat views)."""
    total_pages = max(1, st.session_state.doc_metrics.get("page_count", 1))
    with st.container(horizontal=True, vertical_alignment="bottom"):
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
            key=page_key,
            width=110,
        )
        zoom = st.select_slider(
            "Zoom",
            options=[1.0, 1.5, 2.0, 2.5],
            value=default_zoom,
            key=zoom_key,
        )
        overlay = st.toggle("AI overlay", value=True, key=f"{page_key}_overlay")
        html(
            f'<span class="pill">of {total_pages} pg</span>'
            '<span class="pill"><span class="dot"></span>amount</span>'
            '<span class="pill"><span class="dot" style="background:var(--accent)"></span>'
            "date</span>"
        )

    if not st.session_state.pdf_bytes:
        empty_state("No active document loaded.")
        return
    highlights: tuple[tuple[str, str], ...] = ()
    if overlay:
        found = detect_entities()
        highlights = tuple(
            [(v, "amount") for v in found["amounts"]] + [(v, "date") for v in found["dates"]]
        )
    img = render_pdf_page_cached(
        st.session_state.pdf_bytes, page_number=page - 1, zoom=zoom, highlights=highlights
    )
    if img:
        st.image(img, width="stretch")
    else:
        empty_state("This page could not be rendered.")


def render_split_inspector() -> None:
    """Render the dual-pane Split Inspector."""
    col_left, col_right = st.columns(2, gap="medium")

    with col_left, st.container(border=True):
        panel_title("PDF inspector", st.session_state.uploaded_file_name)
        render_pdf_stage("inspector_pdf_page", "inspector_pdf_zoom")

    with col_right, st.container(border=True):
        metrics = st.session_state.doc_metrics
        panel_title("AI intelligence console", "local inference")
        tab_summary, tab_entities, tab_json = st.tabs(
            ["Summary", "Detected entities", "JSON schema"]
        )
        entities = detect_entities()

        with tab_summary:
            kpi_row(
                [
                    ("Pages", str(metrics.get("page_count", 0)), "in document", False),
                    ("Words", f"{metrics.get('word_count', 0):,}", "extracted", False),
                    ("Reading", f"{metrics.get('reading_time_min', 0)} min", "at 200 wpm", False),
                ]
            )
            panel_title("Executive summary")
            summary = st.session_state.ai_summary
            if summary:
                st.markdown(
                    f'<div data-testid="ai-summary-container" class="summary" '
                    f'style="white-space:pre-wrap">{escape(summary)}</div>',
                    unsafe_allow_html=True,
                )
            else:
                empty_state("Run extraction to generate the AI summary.")

        with tab_entities:
            for label, values in (("Amounts", entities["amounts"]), ("Dates", entities["dates"])):
                panel_title(label, f"{len(values)} found")
                if values:
                    html(
                        "".join(
                            f'<div class="row"><span class="mono">{escape(v)}</span>'
                            f'<span class="chip">{label[:-1].lower()}</span></div>'
                            for v in values
                        )
                    )
                else:
                    empty_state(f"No {label.lower()} detected.")

        with tab_json:
            st.code(
                json.dumps(build_extraction_payload(), indent=2), language="json", line_numbers=True
            )


def render_pdf_viewer() -> None:
    """Wrapper function for backward compatibility."""
    render_split_inspector()
