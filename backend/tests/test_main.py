from typing import Any

import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response

from config import settings
from main import app


def _make_pdf(text: str = "Hello") -> bytes:
    content = f"BT /F1 12 Tf 100 700 Td ({text}) Tj ET".encode()
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = (
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"/Contents 4 0 R\n/Resources << /Font << /F1 5 0 R >> >>\n>>\nendobj\n"
    )
    obj4 = (
        b"4 0 obj\n<< /Length " + str(len(content)).encode() + b" >>\nstream\n"
        + content + b"\nendstream\nendobj\n"
    )
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    objs = [obj1, obj2, obj3, obj4, obj5]
    header = b"%PDF-1.4\n"
    offsets = [0] * len(objs)
    offset = len(header)
    for i, obj in enumerate(objs):
        offsets[i] = offset
        offset += len(obj)
    body = b"".join(objs)
    n = len(objs) + 1
    xref_entries = [b"0000000000 65535 f \n"]
    for o in offsets:
        xref_entries.append(f"{o:010d} 00000 n \n".encode())
    xref = b"xref\n0 " + str(n).encode() + b"\n" + b"".join(xref_entries)
    trailer = b"trailer\n<< /Size " + str(n).encode() + b" /Root 1 0 R >>\n"
    eof = b"startxref\n" + str(len(header) + len(body)).encode() + b"\n%%EOF\n"
    return header + body + xref + trailer + eof


@pytest.fixture
def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_upload_pdf_success(client: AsyncClient) -> None:
    pdf_bytes = _make_pdf("Hello World")

    fake_ollama: dict[str, Any] = {
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
        respx.post(url).mock(Response(200, json=fake_ollama))
        resp = await client.post("/upload", files={"file": ("test.pdf", pdf_bytes, "application/pdf")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["tldr"] == "TL;DR"


@pytest.mark.asyncio
async def test_upload_invalid_file(client: AsyncClient) -> None:
    with pytest.raises(Exception):
        await client.post("/upload", files={"file": ("f.txt", b"not a pdf", "text/plain")})
