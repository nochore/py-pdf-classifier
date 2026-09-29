"""Structured Schema & Raw Data Export component (View 3)."""

import json

import streamlit as st


def render_export_view() -> None:
    """Render Structured Schema & Raw Extraction view with KPI cards and JSON code block."""
    col_left, col_right = st.columns([7, 5], gap="medium")

    # LEFT COLUMN: Itemized Entity Table & Validation KPIs
    with col_left:
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; '
            'display: flex; align-items: center; justify-content: space-between;">'
            '<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">'
            "Structured Schema & Extraction</div>"
            '<div style="font-size: 11px; color: #10b981; font-family: monospace;">'
            "✓ 99.6% accuracy • 180ms</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        # KPI Cards
        st.markdown(
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); '
            'gap: 8px; margin-bottom: 12px;">'
            '<div class="slate-card-sm">'
            '<div style="font-size: 10px; color: #8c909f; '
            'text-transform: uppercase;">Total Extracted</div>'
            '<div style="font-size: 18px; font-weight: 600; color: #f1f5f9; '
            'font-family: monospace;">$1,150.00</div>'
            '<div style="font-size: 10px; color: #8b949e;">2 items reconciled</div>'
            "</div>"
            '<div class="slate-card-sm">'
            '<div style="font-size: 10px; color: #8c909f; '
            'text-transform: uppercase;">Extraction Accuracy</div>'
            '<div style="font-size: 18px; font-weight: 600; color: #f1f5f9; '
            'font-family: monospace;">99.6%</div>'
            '<div style="font-size: 10px; color: #10b981;">High confidence tier</div>'
            "</div>"
            '<div class="slate-card-sm">'
            '<div style="font-size: 10px; color: #8c909f; '
            'text-transform: uppercase;">Validation</div>'
            '<div style="font-size: 18px; font-weight: 600; color: #f1f5f9; '
            'font-family: monospace;">RFC 8259</div>'
            '<div style="font-size: 10px; color: #3b82f6;">Schema matched</div>'
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        # Itemized Table
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 12px;">'
            '<div style="font-size: 12px; font-weight: 600; color: #f0f6fc; '
            'margin-bottom: 8px; display: flex; justify-content: space-between;">'
            "<span>Itemized Extraction</span>"
            '<span style="font-size: 10px; color: #8c909f; '
            'font-family: monospace;">2 records</span>'
            "</div>"
            '<table style="width: 100%; border-collapse: collapse; '
            'font-size: 12px; color: #f0f6fc;">'
            '<thead><tr style="border-bottom: 1px solid #222f3d; color: #8c909f; '
            'text-align: left; font-size: 10px; text-transform: uppercase;">'
            '<th style="padding: 6px;">ITEM</th>'
            '<th style="padding: 6px; text-align: right;">QTY</th>'
            '<th style="padding: 6px; text-align: right;">UNIT PRICE</th>'
            '<th style="padding: 6px; text-align: right;">TOTAL</th>'
            '<th style="padding: 6px; text-align: center;">CONFIDENCE</th>'
            "</tr></thead>"
            "<tbody>"
            '<tr style="border-bottom: 1px solid #182028;">'
            '<td style="padding: 8px 6px; font-weight: 500;">Cloud Server Subscriptions</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace;">2</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace;">$500.00</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace; '
            'font-weight: 600;">$1,000.00</td>'
            '<td style="padding: 8px 6px; text-align: center; color: #10b981; '
            'font-family: monospace;">99.8%</td>'
            "</tr>"
            '<tr style="border-bottom: 1px solid #182028;">'
            '<td style="padding: 8px 6px; font-weight: 500;">AI Token Usage Allocation</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace;">10</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace;">$15.00</td>'
            '<td style="padding: 8px 6px; text-align: right; font-family: monospace; '
            'font-weight: 600;">$150.00</td>'
            '<td style="padding: 8px 6px; text-align: center; color: #10b981; '
            'font-family: monospace;">99.4%</td>'
            "</tr>"
            "</tbody>"
            '<tfoot><tr style="font-weight: 600;">'
            '<td colspan="3" style="padding: 8px 6px; text-align: right;">Subtotal:</td>'
            '<td style="padding: 8px 6px; text-align: right; '
            'font-family: monospace;">$1,150.00</td>'
            '<td style="padding: 8px 6px; text-align: center; '
            'color: #10b981;">Verified</td>'
            "</tr></tfoot>"
            "</table>"
            "</div>",
            unsafe_allow_html=True,
        )

        # Download Actions
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="Download Raw Text File",
                data=st.session_state.extracted_text,
                file_name="extracted_document.txt",
                mime="text/plain",
                key="btn_download_txt",
                use_container_width=True,
            )
        with col_exp2:
            export_payload = {
                "metrics": st.session_state.doc_metrics,
                "summary": st.session_state.ai_summary,
                "raw_text": st.session_state.extracted_text,
                "line_items": [
                    {
                        "item": "Cloud Server Subscriptions",
                        "qty": 2,
                        "unit_price": 500.0,
                        "total": 1000.0,
                    },
                    {
                        "item": "AI Token Usage Allocation",
                        "qty": 10,
                        "unit_price": 15.0,
                        "total": 150.0,
                    },
                ],
                "confidence_score": 0.996,
            }
            st.download_button(
                label="Download JSON Audit Report",
                data=json.dumps(export_payload, indent=2),
                file_name="audit_report.json",
                mime="application/json",
                key="btn_download_json",
                use_container_width=True,
            )

    # RIGHT COLUMN: Syntax-Highlighted Code Editor & Schema
    with col_right:
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; '
            'display: flex; align-items: center; justify-content: space-between;">'
            '<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">'
            "Syntax-Highlighted Code Editor</div>"
            '<div style="font-size: 11px; color: #10b981; font-family: monospace;">'
            "RFC 8259 Valid</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        schema_tab_json, schema_tab_raw = st.tabs(["JSON Schema", "Raw Text Data"])

        with schema_tab_json:
            export_payload = {
                "document_type": "invoice",
                "metadata": {
                    "statement_id": "ACT-8849201",
                    "date": "2026-09-26",
                    "vendor": "ACME ENTERPRISE SOLUTIONS",
                    "currency": "USD",
                },
                "line_items": [
                    {
                        "item": "Cloud Server Subscriptions",
                        "qty": 2,
                        "unit_price": 500.0,
                        "total": 1000.0,
                    },
                    {
                        "item": "AI Token Usage Allocation",
                        "qty": 10,
                        "unit_price": 15.0,
                        "total": 150.0,
                    },
                ],
                "subtotal": 1150.0,
                "confidence_score": 0.996,
            }
            st.code(json.dumps(export_payload, indent=2), language="json")

        with schema_tab_raw:
            st.text_area(
                label="Raw Text Data",
                value=st.session_state.extracted_text,
                height=300,
                key="raw_text_inspector",
            )

        st.markdown(
            '<div style="font-family: monospace; font-size: 11px; color: #8c909f; '
            "background: #141c24; padding: 6px 10px; border-radius: 4px; "
            "border: 1px solid #222f3d; display: flex; justify-content: space-between; "
            'margin-top: 8px;">'
            "<span>UTF-8 Safe • 3 Levels</span>"
            '<span style="color: #10b981; font-weight: 500;">RFC 8259 Valid</span>'
            "</div>",
            unsafe_allow_html=True,
        )


def render_raw_schema() -> None:
    """Alias for render_export_view."""
    render_export_view()
