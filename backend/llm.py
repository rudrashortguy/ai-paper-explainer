import logging

import httpx

from config import settings
from models import PaperSummary

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an AI research paper analyzer. Analyze the given paper text "
    "and return STRICT JSON matching this schema:\n"
    "{\n"
    '  "tldr": "one-sentence summary",\n'
    '  "beginner_explanation": "accessible explanation",\n'
    '  "key_equations": ["equation 1"],\n'
    '  "flashcards": [{"q": "question", "a": "answer"}],\n'
    '  "quiz": [{"question": "...", "options": ["a","b","c","d"], "correct_index": 0}],\n'
    '  "research_gaps": ["gap 1"],\n'
    '  "future_work": ["direction 1"]\n'
    "}\n"
    "Respond ONLY with valid JSON, no other text."
)


async def query_ollama(text: str) -> PaperSummary:
    url = f"{settings.ollama_base_url}/api/generate"
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            url,
            json={
                "model": "gemma2:latest",
                "prompt": f"{SYSTEM_PROMPT}\n\nPaper text:\n{text}",
                "format": "json",
                "stream": False,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return PaperSummary.model_validate_json(data["response"])
