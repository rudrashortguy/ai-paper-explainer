# AI Paper Explainer — Agent Guide

## Quick start
```bash
./run.sh                    # starts both services (port 8000 + 5173)
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

## Stack

| Layer | Tool | Notes |
|-------|------|-------|
| API | FastAPI + uvicorn | `main.py` only — single-file app |
| PDF parsing | pypdfium2 | NOT PyPDF2. `pypdfium2.PdfDocument` + `get_text_bounded()` |
| Text splitting | langchain `RecursiveCharacterTextSplitter` | chunk_size=2000, overlap=200 |
| LLM | Ollama (`gemma2:latest`) via httpx | POST `http://localhost:11434/api/generate`, `"format": "json"`, timeout=120s |
| Caching | aiocache `Cache.MEMORY` | TTL=3600s, keyed by md5(file_content) |
| Frontend | Vite + React 18 | `npm run dev` on port 5173 |
| Upload | react-dropzone | PDF-only, single file |
| State | Zustand | `useStore` for darkMode toggle |
| API client | TanStack Query | `useMutation` for `/upload` |
| Styling | TailwindCSS v3 | `darkMode: 'class'`, navy base `#0A2463` |
| Docker | Compose | nginx → backend proxy, healthcheck |

## Backend structure
```
backend/
  main.py       — FastAPI app, /upload (cached), /health, CORS
  models.py     — PaperSummary Pydantic model (strict JSON shape)
  parser.py     — extract_text_from_pdf(path) via pypdfium2
  llm.py        — query_ollama(text) -> PaperSummary
  config.py     — BaseSettings (ollama_base_url, chunk params)
  tests/
    conftest.py       — env overrides, sys.path
    test_main.py      — health, upload (with respx mock)
    test_parser.py    — real PDF + encrypted error path
    test_llm.py       — success + HTTP error (respx)
    test_models.py    — validation
```

## Frontend structure
```
frontend/
  src/
    main.jsx           — ReactDOM + QueryClientProvider
    App.jsx            — upload flow, dark mode toggle
    Uploader.jsx       — react-dropzone wrapper
    SummaryDisplay.jsx — renders all PaperSummary sections
    store.js           — Zustand store (darkMode)
```

## Docker
```bash
OLLAMA_BASE_URL=http://host.docker.internal:11434 docker compose up --build -d
```

## Key constraints / gotchas

- Ollama **must** be running locally on port 11434 with `gemma2:latest` pulled.
- Only first 5 chunks (~10K tokens) sent to LLM to avoid context overflow.
- `format: "json"` is passed to Ollama; model must support it (Gemma 2 does).
- CORS only allows `http://localhost:5173` — update for prod (nginx handles proxy).
- run.sh kills existing processes on 8000/5173 before starting.
- Caching: md5 hash of file bytes → `aiocache.MEMORY` with 3600s TTL.
- Tests mock Ollama via `respx`; run with `pytest backend/`.

## Required workflow (execute in order)

```bash
# Backend
ruff check backend/ --fix
mypy backend/
pytest backend/ --cov=backend/ --cov-report=term-missing
bandit -r backend/

# Frontend
cd frontend && npm run lint && npm run format
```

## Config files to check first

- `backend/requirements.txt` — pinned deps (including aiocache, pytest, respx)
- `frontend/package.json` — scripts: dev/build/lint/format
- `frontend/vite.config.js` — port, plugins
- `frontend/tailwind.config.js` — content paths, darkMode
- `frontend/.eslintrc.cjs` — JSX rules
- `docker-compose.yml` — service definitions, healthcheck
- `backend/Dockerfile` — python:3.12-slim
- `frontend/Dockerfile` — node:20-alpine → nginx:alpine
