# Deployment

## Docker Compose

```bash
# Build and start
OLLAMA_BASE_URL=http://host.docker.internal:11434 docker compose up --build -d

# Stop
docker compose down
```

The backend connects to Ollama running on the host via `host.docker.internal`.
Set `OLLAMA_BASE_URL` to your Ollama server address.

## Production Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server address |
| `MAX_CHUNK_SIZE` | `2000` | Text chunk size for splitting |
| `CHUNK_OVERLAP` | `200` | Chunk overlap size |

## Performance

- `GUNICORN_WORKERS=4` for production (behind gunicorn with uvicorn workers)
- `UVICORN_LOOP=uvloop` for async performance on Linux
- Redis backend for aiocache (set `AIOCACHE_REDIS_URL` env var)

## Architecture

```
frontend (nginx:80)
  └── /api/* → backend:8000
backend (uvicorn:8000)
  └── POST /upload → parse PDF → chunk → Ollama → response
```

## Health Checks

```bash
curl http://localhost:8000/health
```
