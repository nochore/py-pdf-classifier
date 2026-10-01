"""PDF extraction and page rendering services."""

from typing import Tuple

import pymupdf
import streamlit as st


def extract_pdf_data(pdf_bytes: bytes) -> Tuple[str, int]:
    """Extract plain text and page count from raw PDF bytes."""
    if not pdf_bytes:
        return "", 0

    extracted_text = ""
    page_count = 0

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = len(doc)
        for page in doc:
            extracted_text += page.get_text() + "\n"

    return extracted_text, page_count


OVERLAY_COLORS = {"amount": (0.06, 0.73, 0.51), "date": (0.23, 0.51, 0.96)}


def _draw_overlay(page: "pymupdf.Page", highlights: Tuple[Tuple[str, str], ...]) -> None:
    """Draw bounding boxes around each highlighted term on a page."""
    for term, kind in highlights:
        color = OVERLAY_COLORS.get(kind, (0.96, 0.62, 0.04))
        for rect in page.search_for(term):
            box = rect + (-2, -2, 2, 2)
            page.draw_rect(box, color=color, fill=color, fill_opacity=0.12, width=1)


@st.cache_data(show_spinner=False)
def render_pdf_page_cached(
    pdf_bytes: bytes,
    page_number: int,
    zoom: float,
    highlights: Tuple[Tuple[str, str], ...] = (),
) -> bytes:
    """Lazy-rendered PDF page cache helper returning PNG image bytes.

    Args:
        highlights: Optional ``(term, kind)`` pairs to box on the rendered page.
    """
    if not pdf_bytes:
        return b""

    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if 0 <= page_number < len(doc):
            page = doc[page_number]
            if highlights:
                _draw_overlay(page, highlights)
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            return bytes(pix.tobytes("png"))

    return b""
