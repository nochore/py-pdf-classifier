"""Summary report component."""

import streamlit as st


def render_summary_view() -> None:
    """Render the AI summary analysis tab content."""
    st.subheader("Automated AI Intelligence Report")
    st.markdown(
        f'<div data-testid="ai-summary-container">{st.session_state.ai_summary}</div>',
        unsafe_allow_html=True,
    )
