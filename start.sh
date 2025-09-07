#!/usr/bin/env sh
set -e

PORT="${PORT:-8000}"

exec fastapi run src/api/main.py \
  --host 0.0.0.0 \
  --port "${PORT}" \
  --proxy-headers \
  --forwarded-allow-ips="*"
