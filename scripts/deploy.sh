#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Environment file not found: $ENV_FILE"
  echo "Create it from one of the examples first, for example: cp .env.production.example .env.production"
  exit 1
fi

set -a
# shellcheck source=/dev/null
source "$ENV_FILE"
set +a

PROJECT_NAME="${COMPOSE_PROJECT_NAME:-fastapi_project}"

docker compose --env-file "$ENV_FILE" -p "$PROJECT_NAME" up -d --build
docker compose --env-file "$ENV_FILE" -p "$PROJECT_NAME" ps
