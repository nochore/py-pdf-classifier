"""Playwright End-to-End UI Automation Test Suite for Streamlit Dashboard."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_dashboard_initial_state(page: Page):
    """Test initial landing state of the Document AI Enterprise Dashboard."""
    # Navigate to running Streamlit instance
    page.goto("http://localhost:8501", timeout=10000)

    # Verify document title / main title header
    expect(page).to_have_title("Document AI Enterprise Parser")

    # Verify presence of main ready indicator
    info_box = page.get_by_text("System Ready. Please upload a PDF document")
    expect(info_box).to_be_visible()

    # Verify sidebar inputs
    model_input = page.get_by_role("textbox", name="Ollama Model Identifier")
    expect(model_input).to_be_visible()

    file_uploader = page.get_by_text("Select Target Document (PDF)")
    expect(file_uploader).to_be_visible()


@pytest.mark.e2e
def test_sidebar_model_input_interaction(page: Page):
    """Test sidebar model input widget interaction."""
    page.goto("http://localhost:8501", timeout=10000)

    model_input = page.get_by_role("textbox", name="Ollama Model Identifier")
    model_input.clear()
    model_input.fill("mistral")
    expect(model_input).to_have_value("mistral")
