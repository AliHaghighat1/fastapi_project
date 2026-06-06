# Security and Deployment Notes

## Secrets

Do not commit real environment files.

These files are ignored by Git:

- `.env`
- `.env.production`
- `.env.test`
- `.env.dev`
- any other `.env.*` file except `.example` files

Commit only example files:

- `.env.example`
- `.env.production.example`
- `.env.test.example`
- `.env.dev.example`

Store real values such as `COHERE_API_TOKEN` only on the server or in GitHub Actions secrets.

## Production settings

For production, use:

```env
APP_ENV=production
DEBUG=false
CORS_ORIGINS=https://your-production-domain.com
```

Avoid `CORS_ORIGINS=*` in production unless the API is intentionally public.

## Docker user

The Docker image runs the app as a non-root Linux user named `app`.

## Network exposure

The app listens on port `8000` inside the container. The host port is controlled by `HOST_PORT` in each env file.

Recommended defaults:

- production: `8000`
- shared test: `8001`
- developer environments: `8011`, `8012`, `8013`

For a real public production deployment, put a reverse proxy such as Nginx, Caddy or Traefik in front of the app and terminate HTTPS there.

## Team server access

A three-person team can use separate Linux users and a shared project group.

Example:

```bash
sudo groupadd -f fastapi
sudo usermod -aG fastapi,docker user1
sudo usermod -aG fastapi,docker user2
sudo usermod -aG fastapi,docker user3
sudo mkdir -p /srv/fastapi_project/{production,test,developers}
sudo chgrp -R fastapi /srv/fastapi_project
sudo chmod -R 2775 /srv/fastapi_project
```

Important: the `docker` group is powerful. Only trusted users should be added to it.

## Deployment isolation

Every environment must have a unique `COMPOSE_PROJECT_NAME` and `HOST_PORT`.

Example:

```env
COMPOSE_PROJECT_NAME=fastapi_project_prod
HOST_PORT=8000
```

```env
COMPOSE_PROJECT_NAME=fastapi_project_test
HOST_PORT=8001
```

This allows production and test to run at the same time on the same server.

## Operational checks

Check containers:

```bash
docker ps
```

Check logs:

```bash
./scripts/logs.sh .env.production
```

Check health:

```bash
curl http://localhost:8000/health
```

Restart after code update:

```bash
git pull
./scripts/deploy.sh .env.production
```
