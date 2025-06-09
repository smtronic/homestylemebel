# 🛋 HomestyleMebel — E-commerce Backend for Furniture Store

**HomestyleMebel** is a modular, well-documented Django REST API backend for a furniture e-commerce platform. It supports SEO-friendly product listings, guest and user carts, order processing, JWT authentication, Dockerized dev/prod environments, and is designed for extensibility.

---

## 📦 Project Structure

```
homestylemebel/
├── apps/               # Modular apps: catalog, cart, orders, users
├── config/             # Django settings, root URLs, nginx config
├── docs/               # Documentation (API, database, architecture)
├── tests/              # Unit and integration tests
├── requirements/       # Split into base, dev, prod
├── .github/            # GitHub Actions CI config
├── Makefile            # Dev & Docker helper commands
├── docker-compose.*.yml# Docker Compose for dev/prod
├── Dockerfile.*        # Dockerfiles for dev/prod
└── manage.py
```

---

## 🔍 Key Features

### 📚 Catalog
- SEO-friendly slug URLs
- Dynamic price calculation (discounts)
- Stock and availability tracking
- Filtering by category, price, availability
- Ordering by price, SKU, creation date
- Admin: category & product management

### 🛒 Cart
- Guest cart via `session_key`, user cart via FK
- Quantity validation by stock
- Total price calculation
- Add, update, remove items
- Auto-merge logic (planned)

### 📦 Orders
- Create order from cart (with validation)
- Full stock deduction and rollback
- Statuses: `new`, `processing`, `completed`, `cancelled`
- Atomic transactions for consistency
- Admin: order management, cancel, edit

### 🔐 Authentication & Security
- JWT auth (register, login, refresh, verify)
- User profile endpoints
- Permissions for admin/user actions
- Security hardening: password policy, rate limiting, 2FA (roadmap)

### 🐳 Docker & DevOps
- Docker Compose for dev/prod
- Separate Dockerfiles for dev/prod
- .env.dev / .env.prod for environment separation
- Makefile for all routine commands
- Nginx as static/media proxy in prod

### 🧪 Testing & CI
- Pytest, pytest-django, coverage
- GitHub Actions: tests, lint, coverage on every push
- Factory Boy for fixtures

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone git@github.com:yourusername/homestylemebel.git
cd homestylemebel
```

### 2. Local development (venv)
```bash
python3 -m venv venv
source venv/bin/activate
make install-dev
cp .env.example .env
django-admin migrate
make run
```
Visit: [http://localhost:8000](http://localhost:8000)

### 3. Dockerized development
```bash
make docker-build-dev   # Build dev images
make docker-up-dev      # Run dev containers
make docker-down-dev    # Stop dev containers
```

### 4. Dockerized production
```bash
make docker-build-prod  # Build prod images
make docker-up-prod     # Run prod containers
make docker-down-prod   # Stop prod containers
```

- Dev: uses `.env.dev`, `docker-compose.dev.yml`, auto-creates superuser
- Prod: uses `.env.prod`, `docker-compose.prod.yml`, nginx for static/media

---

## 🧪 Testing

```bash
make test        # Run all tests
make coverage    # Run tests with coverage
open htmlcov/index.html  # View coverage report
```

---

## 📄 API Overview

Implemented endpoints (see [docs/api.md](./docs/api.md) for full details):

| Method | Endpoint                        | Description               |
| ------ | ------------------------------- | ------------------------- |
| GET    | `/api/v1/catalog/categories/`   | List all categories       |
| GET    | `/api/v1/catalog/products/`     | Product list with filters |
| POST   | `/api/v1/carts/add/`            | Add item to cart          |
| PATCH  | `/api/v1/carts/{id}/update/`    | Update cart item qty      |
| DELETE | `/api/v1/carts/{id}/remove/`    | Remove item from cart     |
| GET    | `/api/v1/orders/`               | List user orders          |
| POST   | `/api/v1/orders/`               | Create order from cart    |
| ...    | ...                             | ...                       |

- Full OpenAPI docs: `/api/v1/schema/swagger-ui/` and `/api/v1/schema/redoc/`

---

## 🛠 Makefile & Docker Commands

| Command                | Description                      |
|------------------------|----------------------------------|
| `make run`             | Run Django dev server            |
| `make test`            | Run tests with Pytest            |
| `make coverage`        | Run tests + coverage             |
| `make lint`            | Check formatting and lint errors |
| `make format`          | Auto-format with black, isort    |
| `make graph`           | Generate ER diagram              |
| `make dump`            | Dump DB (compressed)             |
| `make restore`         | Restore DB from dump             |
| `make docker-build-dev`| Build dev Docker images          |
| `make docker-up-dev`   | Run dev Docker containers        |
| `make docker-down-dev` | Stop dev Docker containers       |
| `make docker-build-prod`| Build prod Docker images         |
| `make docker-up-prod`  | Run prod Docker containers       |
| `make docker-down-prod`| Stop prod Docker containers      |

---

## 🔁 CI/CD
- **GitHub Actions:** tests, lint, coverage on push/PR
- PostgreSQL service in pipeline
- Planned: Docker build, coverage badge, auto-deploy

---

## 📚 Documentation
- [API Reference](./docs/api.md)
- [Architecture Overview](./docs/architecture.md)
- [Database Schema](./docs/database.md)
- [Dev Guide](./docs/development.md)
- [Tasks & Roadmap](./docs/tasks.md)
- [Testing Guide](./docs/testing.md)
- ER Diagram: `docs/image/er_diagram.png`

---

## 🧊 Commit Style
Use Conventional Commits:
- `feat(catalog): add product filtering by price`
- `fix(cart): fix bug with quantity validation`
- `chore: add Makefile commands for backup`

---

## 🤝 Contributing
- Branch naming: `feature/*`, `fix/*`, `chore/*`
- Base branch for PRs: `develop`
- Write tests and docs for your changes
- Run `make lint` and `make test` before pushing

---

## 📧 Contact
- Email: aasmolnikov@gmail.com
- GitHub: [@smtronic](https://github.com/smtronic)
- Telegram: [@smtronic](https://t.me/smtronic)
