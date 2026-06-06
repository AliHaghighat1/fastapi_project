ENV_FILE ?= .env
PROJECT_NAME ?= fastapi_project

up:
	./scripts/deploy.sh $(ENV_FILE)

logs:
	./scripts/logs.sh $(ENV_FILE)

stop:
	./scripts/stop.sh $(ENV_FILE)

prod-up:
	./scripts/deploy.sh .env.production

prod-logs:
	./scripts/logs.sh .env.production

prod-stop:
	./scripts/stop.sh .env.production

test-up:
	./scripts/deploy.sh .env.test

test-logs:
	./scripts/logs.sh .env.test

test-stop:
	./scripts/stop.sh .env.test
