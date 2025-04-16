# 🛋 HomestyleMebel — E-commerce Backend for Furniture Store

**HomestyleMebel** is a modular, well-documented Django REST API backend for a furniture e-commerce platform. It supports SEO-friendly product listings, guest and user carts, order processing, and is designed for extensibility.

---

## 📦 Project Structure

```
homestylemebel/
├── apps/               # Modular apps: catalog, cart, orders, users
├── config/             # Django settings and root URLs
├── docs/               # Documentation (API, database, architecture)
├── tests/              # Unit and integration tests
├── requirements/       # Split into base, dev, prod
├── .github/            # GitHub Actions CI config
├── Makefile            # Dev helper commands
└── manage.py
```

---

## 🔍 Key Features

### 📚 Catalog

- Slug-based SEO URLs
- Dynamic actual price calculation (discounts)
- Stock and availability tracking
- Product filtering by category, price range, and availability
- Ordering by price, SKU, and creation date

### 🛒 Cart

- Guest support via `session_key`
- User support via `user` foreign key
- Quantity validation based on stock
- Total price calculation
- Auto-merge logic planned (guest → user)

### 📦 Orders

- Create order from cart (with validation)
- Full stock deduction and rollback logic
- Status tracking: `new`, `processing`, `completed`, `cancelled`
- Atomic transactions to ensure consistency

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone git@github.com:yourusername/homestylemebel.git
cd homestylemebel
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
make install-dev
```

### 4. Configure environment

Create `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit values: `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, etc.

### 5. Apply migrations and run server

```bash
make run
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🧪 Testing

Run all tests:

```bash
make test
```

Generate code coverage report:

```bash
make coverage
```

To view the report:

```bash
open htmlcov/index.html
```

---

## 📄 API Overview

Implemented public endpoints:

| Method | Endpoint                     | Description               |
| ------ | ---------------------------- | ------------------------- |
| GET    | `/api/v1/categories/`        | List all categories       |
| GET    | `/api/v1/categories/{slug}/` | Category details          |
| GET    | `/api/v1/products/`          | Product list with filters |
| GET    | `/api/v1/products/{slug}/`   | Product details           |

More coming soon: cart, orders, auth, and profile.

📚 Full API docs: [docs/api.md](./docs/api.md)

---

## 🛠 Makefile Commands

| Command         | Description                      |
| --------------- | -------------------------------- |
| `make run`      | Run Django dev server            |
| `make test`     | Run tests with Pytest            |
| `make coverage` | Run tests + coverage             |
| `make lint`     | Check formatting and lint errors |
| `make format`   | Auto-format with black, isort    |
| `make graph`    | Generate ER diagram              |
| `make dump`     | Dump DB (compressed)             |
| `make restore`  | Restore DB from dump             |

---

## 🔁 CI/CD

- **GitHub Actions:**
  - Tests on push & PRs
  - PostgreSQL service
- **Planned:**
  - Docker + docker-compose
  - Coverage badge
  - Auto-deploy hooks

Workflow config: `.github/workflows/tests.yml`

---

## 📚 Documentation

- 📄 [API Reference](./docs/api.md)
- 🧱 [Architecture Overview](./docs/architecture.md)
- 🧬 [Database Schema](./docs/database.md)
- 🛠 [Dev Guide](./docs/development.md)
- ✅ [Tasks & Roadmap](./docs/tasks.md)
- 🔬 [Testing Guide](./docs/testing.md)
- 📊 ER Diagram

---

## 🧊 Commit Style

Use Conventional Commits:

Examples:

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
