"""Interactive Document Q&A workspace component (View 2)."""

import streamlit as st

from pdf_classifier.services.ollama_service import query_ollama
from pdf_classifier.services.pdf_service import render_pdf_page_cached


def render_qa_chat(model_name: str) -> None:
    """Render dual-column Document Q&A workspace (PDF context anchor + chat stream).

    Args:
        model_name: The current Ollama model identifier to query.
    """
    col_pdf, col_chat = st.columns([1, 1], gap="medium")

    # LEFT PANE: PDF CONTEXT ANCHOR
    with col_pdf:
        st.markdown(
            '<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; '
            'display: flex; align-items: center; justify-content: space-between;">'
            '<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">'
            "Context Anchor (PDF)</div>"
            '<div style="font-size: 11px; color: #10b981; font-family: monospace;">'
            "● Grounded in context</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        metrics = st.session_state.doc_metrics
        total_pages = metrics.get("page_count", 1)

        c_col1, c_col2 = st.columns([2, 2])
        with c_col1:
            chat_page = st.number_input(
                "Context Page",
                min_value=1,
                max_value=max(1, total_pages),
                value=1,
                step=1,
                key="chat_pdf_page",
            )
        with c_col2:
            chat_zoom = st.select_slider(
                "Preview Scale",
                options=[1.0, 1.5, 2.0],
                value=1.5,
                key="chat_pdf_zoom",
            )

        if st.session_state.pdf_bytes:
            with st.spinner("Loading document anchor..."):
                page_img = render_pdf_page_cached(
                    st.session_state.pdf_bytes,
                    page_number=chat_page - 1,
                    zoom=chat_zoom,
                )
            if page_img:
                st.image(page_img, use_container_width=True)
        else:
            st.markdown(
                '<div style="background-color: #060f16; border: 1px dashed #222f3d; '
                "border-radius: 6px; padding: 24px; text-align: center; "
                'color: #64748b; font-size: 12px;">'
                "No active document preview available."
                "</div>",
                unsafe_allow_html=True,
            )

    # RIGHT PANE: CONTEXTUAL CHAT STREAM
    with col_chat:
        st.markdown(
            f'<div class="slate-card" style="margin-bottom: 8px; padding: 8px 12px; '
            f'display: flex; align-items: center; justify-content: space-between;">'
            f'<div style="font-size: 13px; font-weight: 600; color: #f0f6fc;">'
            f"Q&A Assistant ({model_name})</div>"
            f'<div style="font-size: 11px; color: #10b981; '
            f'font-family: monospace;">● Ready</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Chat history container
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown(
                    '<div style="font-size: 12px; color: #8c909f; text-align: center; '
                    'padding: 16px 0;">'
                    "Ask any question below about this document. "
                    "Grounded local inference will inspect exact extracted context."
                    "</div>",
                    unsafe_allow_html=True,
                )

            for idx, chat in enumerate(st.session_state.chat_history):
                with st.chat_message(chat["role"]):
                    citation_html = ""
                    if chat["role"] == "assistant":
                        citation_html = (
                            '<div style="margin-top: 6px; font-size: 10px; '
                            'color: #3b82f6; font-family: monospace;">'
                            "📍 Page 1, Document Context"
                            "</div>"
                        )
                    st.markdown(
                        f'<div data-testid="chat-message-{idx}">'
                        f'{chat["content"]}{citation_html}</div>',
                        unsafe_allow_html=True,
                    )

        # Quick Suggestion Chips
        st.markdown(
            '<div style="font-size: 10px; text-transform: uppercase; color: #8c909f; '
            'margin-top: 8px; margin-bottom: 4px;">Quick Suggestions</div>',
            unsafe_allow_html=True,
        )
        s_col1, s_col2, s_col3 = st.columns(3)
        prompt_to_submit = None

        with s_col1:
            if st.button("What is total due?", key="btn_sug1", use_container_width=True):
                prompt_to_submit = "What is the total amount due on this document?"
        with s_col2:
            if st.button("Verify tax & breakdown", key="btn_sug2", use_container_width=True):
                prompt_to_submit = "Verify tax rates and breakdown of line items."
        with s_col3:
            if st.button("List line items", key="btn_sug3", use_container_width=True):
                prompt_to_submit = "List all itemized line items with quantities and unit prices."

        # Input field
        user_input = st.chat_input(
            "Ask a question about the document context...", key="chat_input_field"
        )

        query = prompt_to_submit or user_input

        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(query)

                with st.chat_message("assistant"):
                    with st.spinner("Processing Context Query..."):
                        qa_prompt = (
                            f"Using only the following document context, "
                            f"answer this question: '{query}'\n\n"
                            f"Context:\n{st.session_state.extracted_text[:6000]}"
                        )
                        response = query_ollama(qa_prompt, model=model_name)
                        st.markdown(
                            f'<div data-testid="latest-ai-response">{response}'
                            f'<div style="margin-top: 6px; font-size: 10px; color: #3b82f6; '
                            f'font-family: monospace;">📍 Page 1, Document Context</div>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response}
                        )


def render_chat_workspace(model_name: str) -> None:
    """Alias for render_qa_chat."""
    render_qa_chat(model_name)
