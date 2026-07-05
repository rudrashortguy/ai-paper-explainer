import hashlib
import logging
import tempfile
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from aiocache import Cache
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from models import PaperSummary
from parser import extract_text_from_pdf
from llm import query_ollama

cache = Cache(Cache.MEMORY)

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    handler = RotatingFileHandler(
        "app.log", maxBytes=1_048_576, backupCount=3
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()
    yield


app = FastAPI(title="AI Paper Explainer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.max_chunk_size,
    chunk_overlap=settings.chunk_overlap,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception for %s", request.url)
    return JSONResponse(
        status_code=500,
        content={
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": str(exc),
            "instance": str(request.url),
        },
        media_type="application/problem+json",
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload", response_model=PaperSummary)
async def upload_pdf(file: UploadFile = File(...)) -> PaperSummary:
    logger.info("Received upload: %s", file.filename)
    file_bytes = await file.read()
    content_hash = hashlib.md5(file_bytes, usedforsecurity=False).hexdigest()
    cache_key = f"paper:{content_hash}"

    cached = await cache.get(cache_key)
    if cached is not None:
        logger.info("Cache hit for %s", cache_key)
        return PaperSummary(**cached)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        raw = extract_text_from_pdf(tmp_path)
    except Exception as exc:
        logger.exception("Failed to parse PDF")
        raise exc
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    chunks = text_splitter.split_text(raw)
    combined = "\n\n---\n\n".join(chunks[:5])
    result = await query_ollama(combined)

    await cache.set(cache_key, result.model_dump(), ttl=3600)
    return result
