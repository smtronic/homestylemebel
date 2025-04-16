# 🛠 Development Guide

This document describes how to set up the development environment, run the project, and follow best practices for contributing to `homestylemebel`.

---

## 📦 Project Structure

```
homestylemebel/
├── apps/
│   ├── catalog/          # Product catalog (models, views, serializers, services)
│   ├── cart/             # Shopping cart logic (anonymous and user-based)
│   ├── orders/           # Order system (creation, validation, processing)
│   └── users/            # Custom user model and auth logic
├── config/               # Django settings and root URLs
├── docs/                 # Project documentation (API, DB, architecture)
├── requirements/         # Requirements split by env (base, dev, prod)
├── tests/                # Unit and integration tests
├── .github/              # GitHub Actions CI/CD
├── .coveragerc           # Coverage config
├── Makefile              # Helper commands for development
├── manage.py             # Django entry point
└── pytest.ini            # Pytest config
```

---

## ⚙️ Setup

1. **Clone project**

```bash
git clone git@github.com:yourusername/homestylemebel.git
cd homestylemebel
```

2. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
make install-dev
```

4. **Configure environment**

Create `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit values: `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, etc.

5. **Run PostgreSQL** (optional via Docker)

```bash
docker run --name pg-homestyle -e POSTGRES_DB=homestyle -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -p 5432:5432 -d postgres:15
```

6. **Run migrations and server**

```bash
make run
```

Visit [http://localhost:8000](http://localhost:8000)

---

## 🚀 Useful Make Commands

```bash
make install         # Install prod dependencies
make install-dev     # Install dev dependencies (linters, tests)
make run             # Run local Django server
make test            # Run tests with pytest
make coverage        # Run tests + coverage report
make lint            # Run flake8, black --check, isort --check
make format          # Format code with black and isort
make graph           # Generate ER diagram (requires pygraphviz)
make dump            # Dump DB to compressed file
make restore         # Restore DB from compressed dump
```

---

## 🔍 Testing

- `pytest` used as test runner
- Tests live under `tests/` organized by app and layer
- Use `make coverage` to view coverage
- Docs: [docs/testing.md](./testing.md)

---

## 🧹 Code Style

- Python formatting: `black`
- Imports: `isort`
- Linting: `flake8`

Run checks:

```bash
make lint
```

Auto-fix formatting:

```bash
make format
```

---

## 🧪 Continuous Integration (CI)

GitHub Actions is used to run tests and linting on each pull request. Config: `.github/workflows/test.yml`.

---

## 🧊 Commit Style

Follow **Conventional Commits**:

Examples:

- `feat(catalog): add product filtering by price`
- `fix(cart): fix bug with quantity validation`
- `chore: add Makefile commands for backup`

---

## 🤝 Contributing

- Use branches: `feature/*`, `fix/*`, `chore/*`
- Make pull requests to `develop`
- Include tests and docs in your PR

---
