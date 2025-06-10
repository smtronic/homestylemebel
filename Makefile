-include .env
export

.PHONY: install install-dev test coverage lint format graph dump-sql restore-sql dump restore spectacular_upgrade docker-build-dev docker-up-dev docker-down-dev docker-build-prod docker-up-prod docker-down-prod

# 📦 Install production dependencies
install:
	pip install -r requirements/prod.txt

# 📦 Install development dependencies
install-dev:
	pip install -r requirements/dev.txt

# 🧪 Run tests
test:
	pytest -v

# 📈 Run tests with code coverage report
coverage:
	pytest --cov=apps --cov-report=term-missing

# 🧹 Lint the codebase with flake8, black, and isort
lint:
	flake8 --max-line-length=120 --exclude=*/migrations/* apps tests
	isort --check-only apps tests
	black --check apps tests

# 🧼 Auto-format the code using black and isort
format:
	isort apps tests
	black apps tests

# 🧠 Generate ER diagram of the models
# graph:
# 	python manage.py graph_models catalog cart orders users \
# 		--theme=django2018 \
# 		--group-models \
# 		--output docs/image/er_diagram.png

# 🛢 PostgreSQL database operations

# Create backup directory
backup-dir:
	mkdir -p backup

# SQL dump
dump-sql: backup-dir
	pg_dump -U $(DB_USER) -d $(DB_NAME) > backup/backup.sql

# Restore from SQL dump
restore-sql:
	psql -U $(DB_USER) -d $(DB_NAME) < backup/backup.sql

# Compressed custom-format dump
dump: backup-dir
	pg_dump -U $(DB_USER) -d $(DB_NAME) -Fc | gzip > backup/backup.dump.gz

# Restore from compressed custom-format dump
restore:
	gunzip -c backup/backup.dump.gz | pg_restore -U $(DB_USER) -d $(DB_NAME)

spectacular_upgrade:
	python manage.py spectacular --file schema.yaml

# Docker Compose commands for development

docker-build-dev:
	docker compose -f docker-compose.dev.yml build

docker-up-dev:
	docker compose -f docker-compose.dev.yml up

docker-down-dev:
	docker compose -f docker-compose.dev.yml down

# Docker Compose commands for production

docker-build-prod:
	docker compose -f docker-compose.prod.yml build

docker-up-prod:
	docker compose -f docker-compose.prod.yml up

docker-down-prod:
	docker compose -f docker-compose.prod.yml down
