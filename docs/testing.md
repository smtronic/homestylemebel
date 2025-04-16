# 🔪 Testing Guide

Documentation for running, organizing, and configuring tests in the **homestylemebel** project.

---

## 📁 Structure

```
tests/
├── conftest.py               # Project-wide fixtures
├── catalog/                  # Tests for the catalog module
│   ├── models/
│   ├── serializers/
│   ├── services/
│   ├── test_views.py
│   └── test_urls.py
...
```

---

## 🚀 Quick Start

✅ Run all tests:

```bash
make test
```

Or manually:

```bash
pytest -v
```

📈 Generate code coverage report:

```bash
make coverage
```

To view the report:

```bash
open htmlcov/index.html
```

---

## 🔪 Pytest + Django Integration

We use the following plugins:

- [`pytest`](https://docs.pytest.org/)
- [`pytest-django`](https://pytest-django.readthedocs.io/)
- [`pytest-factoryboy`](https://pytest-factoryboy.readthedocs.io/)
- [`pytest-cov`](https://pytest-cov.readthedocs.io/)
- [`pytest-mock`](https://pytest-mock.readthedocs.io/)

---

## ⚙️ Makefile Commands

| Command         | Description                             |
|----------------|-----------------------------------------|
| `make install`  | Install production dependencies         |
| `make install-dev` | Install development/testing tools   |
| `make test`     | Run all tests                           |
| `make coverage` | Run tests with code coverage report     |
| `make lint`     | Check code formatting with `black`      |
| `make format`   | Auto-format code using `black` + `isort`|

---

## 🔧 Configuration

### `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_test.py
testpaths = tests
addopts = --reuse-db
```

### `.coveragerc`

```ini
[run]
omit =
    */migrations/*
    */__init__.py
    */admin.py
    */apps.py
    */wsgi.py
    */asgi.py
    manage.py

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    def __str__
```

---

## 📌 Best Practices

- Write **unit tests** for models, serializers, and services.
- Use **integration tests** for API views and permissions.
- Use **fixtures** and **mocking** to isolate dependencies.
- Aim for **>90% coverage** for business logic and critical paths.

---
