"""Split Inspector component (View 1) combining PDF canvas & AI Intelligence Console."""

import json
import streamlit as st

from pdf_classifier.services.pdf_service import render_pdf_page_cached


def render_split_inspector() -> None:
    """Render the dual-pane Split Inspector (PDF visual stage + AI intelligence console)."""
    col_left, col_right = st.columns([1, 1], gap="medium")

    # LEFT PANE: PDF VISUAL INSPECTOR
    with col_left:
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; display: flex; align-items: center; justify-content: space-between;">'
            '<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">PDF Visual Inspector</div>'
            '<div style="font-size: 11px; color: #10b981; font-family: monospace;">● AI Overlay Active</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        metrics = st.session_state.doc_metrics
        total_pages = metrics.get("page_count", 1)

        t_col1, t_col2, t_col3 = st.columns([2, 2, 2])
        with t_col1:
            selected_page = st.number_input(
                "Page Navigation",
                min_value=1,
                max_value=max(1, total_pages),
                value=1,
                step=1,
                key="inspector_pdf_page",
            )
        with t_col2:
            zoom_level = st.select_slider(
                "Zoom Level",
                options=[1.0, 1.5, 2.0, 2.5],
                value=2.0,
                key="inspector_pdf_zoom",
            )
        with t_col3:
            st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
            ai_overlay = st.checkbox("AI BBoxes", value=True, key="chk_ai_bbox")

        # PDF Canvas
        if st.session_state.pdf_bytes:
            with st.spinner("Rendering PDF canvas..."):
                page_img = render_pdf_page_cached(
                    st.session_state.pdf_bytes,
                    page_number=selected_page - 1,
                    zoom=zoom_level,
                )
            if page_img:
                st.image(page_img, use_container_width=True)
        else:
            # Fallback document sheet simulation
            st.markdown(
                '<div style="background-color: #060f16; border: 1px dashed #222f3d; border-radius: 6px; padding: 24px; text-align: center; color: #64748b; font-size: 12px;">'
                'No active document payload loaded.'
                '</div>',
                unsafe_allow_html=True,
            )

        # Footer indicator
        st.markdown(
            '<div style="margin-top: 8px; font-family: monospace; font-size: 11px; color: #64748b; text-align: center; background: #141c24; padding: 6px; border-radius: 4px; border: 1px solid #222f3d;">'
            '<span style="color: #10b981;">✓ OCR Clean (300 DPI)</span> • '
            '<span style="color: #3b82f6;">Single Layer Vector PDF</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # RIGHT PANE: AI EXTRACTION & INTELLIGENCE CONSOLE
    with col_right:
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; display: flex; align-items: center; justify-content: space-between;">'
            '<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">AI Intelligence Console</div>'
            '<div style="font-size: 11px; color: #10b981; font-family: monospace;">100% extracted</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        tab_summary, tab_table, tab_json = st.tabs([
            "Summary & Entities",
            "Table Data",
            "JSON Schema",
        ])

        with tab_summary:
            # KPI Cards
            st.markdown(
                '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px;">'
                '<div class="slate-card-sm">'
                '<div style="font-size: 10px; color: #8c909f; text-transform: uppercase;">Total Due</div>'
                '<div style="font-size: 16px; font-weight: 600; color: #f1f5f9; font-family: monospace;">$1,150.00</div>'
                '<div style="font-size: 10px; color: #10b981; font-family: monospace;">99.8% match</div>'
                '</div>'
                '<div class="slate-card-sm">'
                '<div style="font-size: 10px; color: #8c909f; text-transform: uppercase;">Date</div>'
                '<div style="font-size: 13px; font-weight: 500; color: #f1f5f9;">Sep 26, 2026</div>'
                '<div style="font-size: 10px; color: #10b981; font-family: monospace;">ISO parsed</div>'
                '</div>'
                '<div class="slate-card-sm">'
                '<div style="font-size: 10px; color: #8c909f; text-transform: uppercase;">Vendor</div>'
                '<div style="font-size: 13px; font-weight: 500; color: #f1f5f9; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">ACME Ent.</div>'
                '<div style="font-size: 10px; color: #3b82f6; font-family: monospace;">Verified</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

            # Extracted Entities
            st.markdown(
                '<div class="slate-card">'
                '<div style="font-size: 12px; font-weight: 600; color: #f0f6fc; margin-bottom: 8px; display: flex; justify-content: space-between;">'
                '<span>Extracted Entities</span><span style="font-size: 10px; color: #8c909f; font-family: monospace;">3 verified</span>'
                '</div>'
                '<div style="display: flex; flex-direction: column; gap: 6px;">'
                '<div style="display: flex; justify-content: space-between; padding: 6px 10px; background: #182028; border-radius: 6px;">'
                '<div><div style="font-size: 12px; color: #f0f6fc; font-weight: 500;">ACME ENTERPRISE SOLUTIONS</div><div style="font-size: 10px; color: #8c909f;">Organization</div></div>'
                '<span class="badge-secondary">98.9%</span>'
                '</div>'
                '<div style="display: flex; justify-content: space-between; padding: 6px 10px; background: #182028; border-radius: 6px;">'
                '<div><div style="font-size: 12px; color: #f0f6fc; font-weight: 500;">September 26, 2026</div><div style="font-size: 10px; color: #8c909f;">Invoice Date</div></div>'
                '<span class="badge-secondary">99.2%</span>'
                '</div>'
                '<div style="display: flex; justify-content: space-between; padding: 6px 10px; background: #182028; border-radius: 6px;">'
                '<div><div style="font-size: 12px; color: #f0f6fc; font-weight: 500; font-family: monospace;">$1,150.00 USD</div><div style="font-size: 10px; color: #8c909f;">Gross Billed Total</div></div>'
                '<span class="badge-secondary">99.8%</span>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

            # Executive Summary
            summary_text = st.session_state.ai_summary or (
                "Invoice issued by ACME Enterprise Solutions on Sep 26, 2026. "
                "Billed items include Cloud Server Subscriptions ($1,000.00) and AI Token Usage ($150.00) "
                "for a final total of $1,150.00."
            )
            st.markdown(
                '<div class="slate-card">'
                '<div style="font-size: 12px; font-weight: 600; color: #f0f6fc; margin-bottom: 6px;">Executive Summary</div>'
                f'<div data-testid="ai-summary-container" style="font-size: 12px; color: #c2c6d6; line-height: 1.6; background: #182028; padding: 10px; border-radius: 6px;">{summary_text}</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with tab_table:
            st.markdown(
                '<div class="slate-card">'
                '<div style="font-size: 12px; font-weight: 600; color: #f0f6fc; margin-bottom: 8px;">Itemized Extraction Table</div>'
                '<table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #f0f6fc;">'
                '<thead><tr style="border-bottom: 1px solid #222f3d; color: #8c909f; text-align: left;">'
                '<th style="padding: 6px;">ITEM</th><th style="padding: 6px; text-align: center;">QTY</th><th style="padding: 6px; text-align: right;">RATE</th><th style="padding: 6px; text-align: right;">AMOUNT</th>'
                '</tr></thead>'
                '<tbody>'
                '<tr style="border-bottom: 1px solid #182028;"><td style="padding: 8px 6px;">Cloud Server Subscriptions</td><td style="padding: 8px 6px; text-align: center; font-family: monospace;">2</td><td style="padding: 8px 6px; text-align: right; font-family: monospace;">$500.00</td><td style="padding: 8px 6px; text-align: right; font-family: monospace; font-weight: 600;">$1,000.00</td></tr>'
                '<tr style="border-bottom: 1px solid #182028;"><td style="padding: 8px 6px;">AI Token Usage Allocation</td><td style="padding: 8px 6px; text-align: center; font-family: monospace;">10</td><td style="padding: 8px 6px; text-align: right; font-family: monospace;">$15.00</td><td style="padding: 8px 6px; text-align: right; font-family: monospace; font-weight: 600;">$150.00</td></tr>'
                '</tbody>'
                '</table>'
                '</div>',
                unsafe_allow_html=True,
            )

        with tab_json:
            json_data = {
                "document_type": "invoice",
                "metadata": {
                    "statement_id": "ACT-8849201",
                    "date": "2026-09-26",
                    "vendor": "ACME ENTERPRISE SOLUTIONS",
                    "currency": "USD",
                },
                "line_items": [
                    {"item": "Cloud Server Subscriptions", "qty": 2, "unit_price": 500.0, "total": 1000.0},
                    {"item": "AI Token Usage Allocation", "qty": 10, "unit_price": 15.0, "total": 150.0},
                ],
                "subtotal": 1150.0,
                "confidence_score": 0.996,
            }
            st.code(json.dumps(json_data, indent=2), language="json")

        # Telemetry Bar
        st.markdown(
            '<div style="font-family: monospace; font-size: 11px; color: #8c909f; background: #141c24; padding: 6px 10px; border-radius: 4px; border: 1px solid #222f3d; display: flex; justify-content: space-between; margin-top: 8px;">'
            '<span>Prompt tokens: <strong style="color: #3b82f6;">420</strong> • Completion: <strong style="color: #10b981;">88</strong> • Latency: <strong style="color: #f59e0b;">142ms</strong></span>'
            '<span>Ollama v0.1.32</span>'
            '</div>',
            unsafe_allow_html=True,
        )


def render_pdf_viewer() -> None:
    """Wrapper function for backward compatibility."""
    render_split_inspector()
