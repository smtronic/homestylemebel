.PHONY: install install-dev test coverage lint run

install:
	pip install -r requirements/prod.txt

install-dev:
	pip install -r requirements/dev.txt

test:
	pytest -v

coverage:
	pytest --cov=apps --cov-report=term-missing

lint:
	flake8 apps tests

run:
	python manage.py runserver
