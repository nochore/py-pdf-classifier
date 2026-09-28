"""PDF extraction and page rendering services."""

from typing import Tuple

import fitz  # PyMuPDF
import streamlit as st


def extract_pdf_data(pdf_bytes: bytes) -> Tuple[str, int]:
    """Extract plain text and page count from raw PDF bytes."""
    if not pdf_bytes:
        return "", 0

    extracted_text = ""
    page_count = 0

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = len(doc)
        for page in doc:
            extracted_text += page.get_text() + "\n"

    return extracted_text, page_count


@st.cache_data(show_spinner=False)
def render_pdf_page_cached(pdf_bytes: bytes, page_number: int, zoom: float) -> bytes:
    """Lazy-rendered PDF page cache helper returning PNG image bytes."""
    if not pdf_bytes:
        return b""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        if 0 <= page_number < len(doc):
            page = doc[page_number]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            return bytes(pix.tobytes("png"))

    return b""
