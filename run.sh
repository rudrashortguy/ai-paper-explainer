#!/usr/bin/env bash
set -e

PORT_8000=$(lsof -ti:8000)
if [ -n "$PORT_8000" ]; then
  kill -9 "$PORT_8000"
fi

PORT_5173=$(lsof -ti:5173)
if [ -n "$PORT_5173" ]; then
  kill -9 "$PORT_5173"
fi

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

source "$PROJECT_DIR/backend/.venv/bin/activate"

cd "$PROJECT_DIR/backend"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
