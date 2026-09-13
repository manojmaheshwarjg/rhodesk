#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PY=$(command -v python3.13 || command -v python3.12 || command -v python3.11 || command -v python3)
[ -d .venv ] || "$PY" -m venv .venv
./.venv/bin/pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
PORT="${PORT:-3000}"
echo "Rho Desk on http://localhost:$PORT"
exec ./.venv/bin/uvicorn rhodesk.api:app --reload \
  --reload-exclude "*.db" --reload-exclude "*.db-wal" --reload-exclude "*.db-shm" \
  --port "$PORT"
