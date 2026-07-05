from typing import Any

import pytest
import respx
from httpx import Response

from config import settings
from llm import query_ollama
from models import PaperSummary


@pytest.mark.asyncio
async def test_query_ollama_success() -> None:
    fake_response: dict[str, Any] = {
        "model": "gemma2:latest",
        "response": (
            '{"tldr":"TL;DR","beginner_explanation":"Simple",'
            '"key_equations":["eq"],"flashcards":[{"q":"Q","a":"A"}],'
            '"quiz":[{"question":"Q","options":["a"],"correct_index":0}],'
            '"research_gaps":["g"],"future_work":["f"]}'
        ),
    }
    url = f"{settings.ollama_base_url}/api/generate"
    with respx.mock:
        respx.post(url).mock(Response(200, json=fake_response))
        result: PaperSummary = await query_ollama("some paper text")
    assert isinstance(result, PaperSummary)
    assert result.tldr == "TL;DR"


@pytest.mark.asyncio
async def test_query_ollama_http_error() -> None:
    url = f"{settings.ollama_base_url}/api/generate"
    with respx.mock:
        respx.post(url).mock(Response(503))
        with pytest.raises(Exception):
            await query_ollama("any text")
