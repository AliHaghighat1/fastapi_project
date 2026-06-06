# FastAPI Backend Project

A Docker-ready FastAPI backend with separate local, test, production and per-developer environments.

The project is designed so one server can run multiple isolated copies at the same time, for example:

- production from the `main` branch on port `8000`
- shared test from a test/development branch on port `8001`
- personal developer branches on ports such as `8011`, `8012`, `8013`

## Project structure

```text
fastapi_project/
├── app/
│   ├── config.py                  # Environment-based settings
│   ├── models/
│   │   └── schemas.py             # Pydantic response/error schemas
│   └── routes/
│       ├── health.py              # /health and /health/ready
│       └── llm_invocation.py      # /get_llm_joke
├── scripts/
│   ├── deploy.sh                  # Build and run one Compose environment
│   ├── logs.sh                    # Follow logs for one Compose environment
│   └── stop.sh                    # Stop one Compose environment
├── Dockerfile                     # Production-style Docker image
├── docker-compose.yml             # Main Compose service
├── docker-compose.dev.yml         # Optional local hot-reload override
├── .env.example                   # Local example environment
├── .env.production.example        # Production example environment
├── .env.test.example              # Shared test example environment
├── .env.dev.example               # Per-developer example environment
├── requirements.txt
├── main.py
└── README.md
```

## API endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Root endpoint with environment info |
| `/health` | Health check for Docker and monitoring |
| `/health/ready` | Readiness check |
| `/docs` | Swagger/OpenAPI documentation |
| `/redoc` | ReDoc documentation |
| `/get_llm_joke` | Test endpoint that calls Cohere when `COHERE_API_TOKEN` is set |

## Run locally with Docker

First create a local env file:

```bash
cp .env.example .env
```

Run the project with one command:

```bash
./scripts/deploy.sh .env
```

Then open:

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

Useful commands:

```bash
./scripts/logs.sh .env
./scripts/stop.sh .env
```

The same commands are available through Make:

```bash
make up
make logs
make stop
```

## Local development with hot reload

For active coding on your own machine:

```bash
cp .env.dev.example .env.dev
```

Edit `.env.dev` and set a unique `COMPOSE_PROJECT_NAME`, `IMAGE_TAG` and `HOST_PORT` if needed.

Run with the dev override:

```bash
docker compose --env-file .env.dev -p fastapi_project_dev -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

This mounts the source code into the container and enables Uvicorn reload.

## Run test and production on the same server

Important: production and test should use separate folders/checkouts if they need to run different branches at the same time.

Recommended server layout:

```text
/srv/fastapi_project/
├── production/       # main branch
├── test/             # shared test branch, for example SMS_dev
└── developers/
    ├── user1/        # user1 branch
    ├── user2/        # user2 branch
    └── user3/        # user3 branch
```

### Production

In `/srv/fastapi_project/production`:

```bash
git checkout main
git pull origin main
cp .env.production.example .env.production
nano .env.production
./scripts/deploy.sh .env.production
```

Default production port: `8000`.

### Shared test

In `/srv/fastapi_project/test`:

```bash
git checkout SMS_dev
git pull origin SMS_dev
cp .env.test.example .env.test
nano .env.test
./scripts/deploy.sh .env.test
```

Default test port: `8001`.

### Run production and test together

Run production from the production folder and test from the test folder. They will not conflict because the example env files use different Compose project names, image tags and host ports.

Check both:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## Per-developer environments on the server

Each developer can have their own Linux user and their own checkout. Example for developer `ali`:

```bash
mkdir -p /srv/fastapi_project/developers/ali
cd /srv/fastapi_project/developers/ali
git clone <YOUR_REPO_URL> .
git checkout ali_branch
cp .env.dev.example .env.dev
nano .env.dev
./scripts/deploy.sh .env.dev
```

In `.env.dev`, change at least these values so every developer has an isolated environment:

```env
COMPOSE_PROJECT_NAME=fastapi_project_dev_ali
IMAGE_TAG=dev-ali
HOST_PORT=8011
API_TITLE="FastAPI Backend Dev Ali"
```

Suggested ports:

| Environment | Branch | Port |
|---|---|---|
| production | `main` | `8000` |
| shared test | `SMS_dev` or another QA branch | `8001` |
| developer 1 | personal branch | `8011` |
| developer 2 | personal branch | `8012` |
| developer 3 | personal branch | `8013` |

## Server user setup for a 3-person team

One admin can prepare the server like this. Replace the usernames with the real Linux usernames:

```bash
sudo groupadd -f fastapi
sudo usermod -aG fastapi,docker user1
sudo usermod -aG fastapi,docker user2
sudo usermod -aG fastapi,docker user3
sudo mkdir -p /srv/fastapi_project/{production,test,developers}
sudo chgrp -R fastapi /srv/fastapi_project
sudo chmod -R 2775 /srv/fastapi_project
sudo apt-get update
sudo apt-get install -y acl
sudo setfacl -R -m g:fastapi:rwx /srv/fastapi_project
sudo setfacl -R -d -m g:fastapi:rwx /srv/fastapi_project
```

Users must log out and log in again after being added to the `docker` group.

Security note: membership in the `docker` group is powerful and should only be given to trusted users. If you do not want that, require developers to use `sudo docker compose ...` instead.

## Environment variables

| Variable | Example | Purpose |
|---|---|---|
| `COMPOSE_PROJECT_NAME` | `fastapi_project_prod` | Isolates Docker Compose resources |
| `IMAGE_NAME` | `fastapi_project` | Docker image name |
| `IMAGE_TAG` | `production` | Docker image tag |
| `HOST_PORT` | `8000` | Server port exposed to the host |
| `APP_ENV` | `production` | Runtime environment name |
| `DEBUG` | `false` | FastAPI debug mode |
| `WORKERS` | `2` | Uvicorn worker count |
| `API_TITLE` | `FastAPI Backend Production` | API title in docs |
| `API_DESCRIPTION` | `FastAPI backend production environment` | API description in docs |
| `API_VERSION` | `1.0.0` | API version |
| `CORS_ORIGINS` | `https://example.com` | Allowed CORS origins; use comma-separated values or `*` |
| `COHERE_API_TOKEN` | empty or real token | Required only for `/get_llm_joke` |

Never commit real `.env`, `.env.production`, `.env.test` or `.env.dev` files. Only commit the `.example` files.

## Git workflow for the team

Recommended branch model:

- `main`: stable production branch only
- `SMS_dev` or `develop`: shared test branch
- one personal branch per developer, for example `ali_branch`, `sara_branch`, `sms_branch`

Typical workflow:

```bash
git checkout main
git pull origin main
git checkout -b your_branch
```

After changes:

```bash
git status
git add .
git commit -m "Describe the change"
git push origin your_branch
```

Then open a pull request from your branch into the shared test branch. After testing, merge the shared test branch into `main` for production.

Production deployment should only pull from `main`.

Test deployment can pull from the shared test branch.

Personal deployments can pull from each developer's own branch.

## Manual Python run without Docker

Docker is recommended for the server, but local Python is still possible:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Docker troubleshooting

Show running containers:

```bash
docker ps
```

Show logs for one environment:

```bash
./scripts/logs.sh .env.production
./scripts/logs.sh .env.test
```

Restart one environment:

```bash
./scripts/deploy.sh .env.production
```

Stop one environment:

```bash
./scripts/stop.sh .env.production
```

Check health:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

If a port is already used, change `HOST_PORT` in that environment file.

## Production notes

For real production use:

- keep `DEBUG=false`
- set exact `CORS_ORIGINS` instead of `*`
- keep secrets only in env files or server secret storage
- put Nginx, Caddy, Traefik or another reverse proxy in front of the app for HTTPS
- deploy production only from `main`
- keep test and production on separate ports, separate Compose project names and preferably separate folders
