from typing import Any, Dict, List

from pydantic import BaseModel


class PaperSummary(BaseModel):
    tldr: str
    beginner_explanation: str
    key_equations: List[str]
    flashcards: List[Dict[str, str]]
    quiz: List[Dict[str, Any]]
    research_gaps: List[str]
    future_work: List[str]
