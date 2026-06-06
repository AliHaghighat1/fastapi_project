# CI/CD and Deployment

This project is Docker-ready. The recommended deployment method is Docker Compose with separate env files for production, shared test and personal developer environments.

## GitHub Actions

The workflow is located at:

```text
.github/workflows/ci-cd.yml
```

It currently does three things:

1. installs Python dependencies
2. runs flake8 lint checks
3. builds and starts the Docker service, then checks `/health`, `/health/ready` and `/get_llm_joke`

The workflow runs on pushes and pull requests for:

- `main`
- `SMS_dev`
- `develop`

## Deployment environments

| Environment | Branch | Env file | Default port | Command |
|---|---|---|---|---|
| Local | any | `.env` | `8000` | `./scripts/deploy.sh .env` |
| Production | `main` | `.env.production` | `8000` | `./scripts/deploy.sh .env.production` |
| Shared test | `SMS_dev` | `.env.test` | `8001` | `./scripts/deploy.sh .env.test` |
| Personal dev | personal branch | `.env.dev` | `8011+` | `./scripts/deploy.sh .env.dev` |

## Production deployment

In the production checkout:

```bash
git checkout main
git pull origin main
cp .env.production.example .env.production
nano .env.production
./scripts/deploy.sh .env.production
```

## Test deployment

In the test checkout:

```bash
git checkout SMS_dev
git pull origin SMS_dev
cp .env.test.example .env.test
nano .env.test
./scripts/deploy.sh .env.test
```

## Personal developer deployment

Each developer should run their branch in a separate checkout and use a unique port and Compose project name.

Example:

```bash
git checkout your_branch
cp .env.dev.example .env.dev
nano .env.dev
./scripts/deploy.sh .env.dev
```

Change these values in `.env.dev`:

```env
COMPOSE_PROJECT_NAME=fastapi_project_dev_yourname
IMAGE_TAG=dev-yourname
HOST_PORT=8011
```

## Logs and stop commands

```bash
./scripts/logs.sh .env.production
./scripts/stop.sh .env.production
```

```bash
./scripts/logs.sh .env.test
./scripts/stop.sh .env.test
```

## Health checks

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

If a health check fails, check logs first:

```bash
./scripts/logs.sh .env.production
```
