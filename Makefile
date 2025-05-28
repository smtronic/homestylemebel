include .env
export

.PHONY: install install-dev test coverage lint format run graph dump-sql restore-sql dump restore spectacular_upgrade

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
	flake8 apps tests
	black --check apps tests
	isort --check-only apps tests

# 🧼 Auto-format the code using black and isort
format:
	black apps tests
	isort apps tests

# 🚀 Run the development server
run:
	python manage.py runserver

# 🧠 Generate ER diagram of the models
graph:
	python manage.py graph_models catalog cart orders users \
		--theme=django2018 \
		--group-models \
		--output docs/image/er_diagram.png

# 🛢 PostgreSQL database operations

# SQL dump
dump-sql:
	pg_dump -U $(DB_USER) -d $(DB_NAME) > backup.sql

# Restore from SQL dump
restore-sql:
	psql -U $(DB_USER) -d $(DB_NAME) < backup.sql

# Compressed custom-format dump
dump:
	pg_dump -U $(DB_USER) -d $(DB_NAME) -Fc | gzip > backup.dump.gz

# Restore from compressed custom-format dump
restore:
	gunzip -c backup.dump.gz | pg_restore -U $(DB_USER) -d $(DB_NAME)

spectacular_upgrade:
	python manage.py spectacular --file schema.yaml
