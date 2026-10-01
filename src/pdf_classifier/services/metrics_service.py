"""Document text metrics and analysis calculations."""

import re
from typing import Any, Dict, Tuple


def compute_text_metrics(text: str, page_count: int) -> Dict[str, Any]:
    """Calculate quantitative text metrics for a document."""
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    avg_word_length = round(char_count / word_count, 1) if word_count > 0 else 0.0
    reading_time_min = round(word_count / 200, 1)

    return {
        "page_count": page_count,
        "word_count": word_count,
        "char_count": char_count,
        "avg_word_length": avg_word_length,
        "reading_time_min": reading_time_min,
    }


def highlight_keywords(text: str, keyword: str) -> Tuple[str, int]:
    """Search for keyword occurrences in text and return HTML marked up text and match count."""
    if not keyword.strip():
        return text, 0
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    matches = len(pattern.findall(text))
    highlighted_text = pattern.sub(
        lambda m: f'<mark class="highlight-match" data-testid="search-match">{m.group(0)}</mark>',
        text,
    )
    return highlighted_text, matches


_AMOUNT_RE = re.compile(r"(?:[$€£]\s?\d[\d,]*(?:\.\d{2})?|\d[\d,]*\.\d{2}\s?(?:USD|EUR|GBP))")
_DATE_RE = re.compile(
    r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? \d{4})\b"
)


def extract_entities(text: str, limit: int = 200) -> Dict[str, list[str]]:
    """Detect unique currency amounts and dates in text (order preserved)."""
    amounts = list(dict.fromkeys(m.strip() for m in _AMOUNT_RE.findall(text)))
    dates = list(dict.fromkeys(_DATE_RE.findall(text)))
    return {"amounts": amounts[:limit], "dates": dates[:limit]}
