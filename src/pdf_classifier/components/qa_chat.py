"""Interactive Document Q&A workspace component (View 2)."""

import time

import streamlit as st

from pdf_classifier.components.pdf_viewer import render_pdf_stage
from pdf_classifier.services.ollama_service import query_ollama
from pdf_classifier.utils.styles import empty_state, panel_title

SUGGESTIONS = {
    "What is the total due?": "What is the total amount due on this document?",
    "Verify tax & breakdown": "Verify tax rates and breakdown of line items.",
    "List line items": "List all itemized line items with quantities and unit prices.",
}


def _queue_suggestion() -> None:
    """Pill callback: queue the chosen prompt and reset the pill (allowed in callbacks)."""
    picked = st.session_state.chat_suggestion
    if picked:
        st.session_state.pending_query = SUGGESTIONS[picked]
        st.session_state.chat_suggestion = None


def _render_message(chat: dict, idx: int) -> None:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        if chat["role"] == "assistant" and chat.get("latency_ms") is not None:
            st.caption(f"📍 Document context • {chat['latency_ms']} ms")


def render_qa_chat(model_name: str) -> None:
    """Render the Q&A workspace: PDF context anchor plus chat stream."""
    col_pdf, col_chat = st.columns([0.45, 0.55], gap="medium")

    with col_pdf, st.container(border=True):
        panel_title("Context anchor", "grounded in document")
        render_pdf_stage("chat_pdf_page", "chat_pdf_zoom", default_zoom=1.5)

    with col_chat, st.container(border=True):
        panel_title("Q&A assistant", model_name)
        history = st.container(height=520, border=False)
        with history:
            if not st.session_state.chat_history:
                empty_state("Ask a question below. Answers use only the extracted document text.")
            for idx, chat in enumerate(st.session_state.chat_history):
                _render_message(chat, idx)

        st.pills(
            "Suggestions",
            list(SUGGESTIONS),
            key="chat_suggestion",
            on_change=_queue_suggestion,
            label_visibility="collapsed",
        )
        user_input = st.chat_input(
            "Ask a question about the document context...", key="chat_input_field"
        )
        query = st.session_state.pop("pending_query", None) or user_input

        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with history:
                with st.chat_message("user"):
                    st.markdown(query)
                with st.chat_message("assistant"):
                    with st.spinner("Processing context query..."):
                        started = time.perf_counter()
                        response = query_ollama(
                            f"Using only the following document context, "
                            f"answer this question: '{query}'\n\n"
                            f"Context:\n{st.session_state.extracted_text[:6000]}",
                            model=model_name,
                            temperature=st.session_state.get("input_temperature"),
                        )
                        latency = int((time.perf_counter() - started) * 1000)
                    st.markdown(response)
                    st.caption(f"📍 Document context • {latency} ms")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": response, "latency_ms": latency}
            )
            st.session_state.latency_ms = latency


def render_chat_workspace(model_name: str) -> None:
    """Alias for render_qa_chat."""
    render_qa_chat(model_name)
