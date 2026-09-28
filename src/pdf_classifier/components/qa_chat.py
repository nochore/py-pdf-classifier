"""Interactive Document Q&A tab component."""

import streamlit as st

from pdf_classifier.services.ollama_service import query_ollama


def render_qa_chat(model_name: str) -> None:
    """Render chat interface for Q&A on extracted document context.

    Args:
        model_name: The current Ollama model identifier to query.
    """
    st.subheader("Contextual Document Assistant")

    for idx, chat in enumerate(st.session_state.chat_history):
        with st.chat_message(chat["role"]):
            st.markdown(
                f'<div data-testid="chat-message-{idx}">{chat["content"]}</div>',
                unsafe_allow_html=True,
            )

    user_input = st.chat_input(
        "Ask a question about the document context...", key="chat_input_field"
    )
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Processing Context Query..."):
                qa_prompt = (
                    f"Using only the following document context, "
                    f"answer this question: '{user_input}'\n\n"
                    f"Context:\n{st.session_state.extracted_text[:6000]}"
                )
                response = query_ollama(qa_prompt, model=model_name)
                st.markdown(
                    f'<div data-testid="latest-ai-response">{response}</div>',
                    unsafe_allow_html=True,
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response})
