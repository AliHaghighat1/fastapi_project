#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Environment file not found: $ENV_FILE"
  exit 1
fi

PROJECT_NAME="$(awk -F= '/^COMPOSE_PROJECT_NAME=/ {
  value = substr($0, index($0, "=") + 1)
  gsub(/^[ \t\x27"]+|[ \t\x27"]+$/, "", value)
  print value
  exit
}' "$ENV_FILE")"
PROJECT_NAME="${PROJECT_NAME:-fastapi_project}"

docker compose --env-file "$ENV_FILE" -p "$PROJECT_NAME" logs -f --tail=100
