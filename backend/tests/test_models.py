from typing import Any

import pytest
from pydantic import ValidationError

from models import PaperSummary


def test_valid_paper_summary() -> None:
    data: dict[str, Any] = {
        "tldr": "A test paper",
        "beginner_explanation": "Simple version",
        "key_equations": ["E=mc^2"],
        "flashcards": [{"q": "Q?", "a": "A!"}],
        "quiz": [{"question": "Q?", "options": ["a", "b"], "correct_index": 0}],
        "research_gaps": ["gap"],
        "future_work": ["work"],
    }
    s = PaperSummary(**data)
    assert s.tldr == "A test paper"


def test_invalid_missing_field() -> None:
    with pytest.raises(ValidationError):
        PaperSummary()  # type: ignore[call-arg]
