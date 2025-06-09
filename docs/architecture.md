# 🏗 Project Architecture – _homestylemebel_

This document describes the structure and core architectural decisions of the **homestylemebel** e-commerce backend project.

---

## 📁 Project Layout

```
homestylemebel/
├── apps/
│   ├── catalog/       # Products, categories, and catalog logic
│   ├── cart/          # Shopping cart (session/user-based)
│   ├── orders/        # Order creation and management
│   └── users/         # Custom user model and authentication
├── config/            # Django settings and configuration
├── tests/             # Pytest tests (unit + integration)
├── docs/              # Developer documentation (API, DB, guides)
├── requirements/      # Split requirements: base, dev, prod
├── .github/           # GitHub Actions CI configs
├── Makefile           # CLI shortcuts for development
├── .coveragerc        # Coverage configuration
├── pytest.ini         # Pytest configuration
└── manage.py
```

---

## 🧱 Key Architectural Concepts

### 1. Modular App Structure

Each domain is isolated in a Django app:

- `catalog`: Products, categories, filtering, images.
- `cart`: Anonymous and authenticated cart logic.
- `orders`: Order processing and validation.
- `users`: Custom user model, registration, and authentication.

> Apps follow Clean Architecture: models, services, serializers, permissions, filters.

---

### 2. Service Layer

Each app includes a `services/` folder:

- Handles business logic and calculations.
- Keeps models and views clean.

🔍 Example: `ProductServices.prepare_for_save()` handles:

- normalization
- slug creation
- actual price
- availability logic

---

### 3. Custom User Model

- Based on `AbstractBaseUser`
- Email-based login (`USERNAME_FIELD = "email"`)
- Includes `first_name`, `last_name`, `phone`, and standard flags (`is_staff`, etc.)

---

### 4. DRF Viewsets + Serializers

- `ModelViewSet` used for `/products/`, `/categories/`
- Supports:
  - Pagination
  - Filtering
  - Searching
  - Ordering

---

### 5. Slug-based Routing

- URLs use `slug` instead of `id` (SEO-friendly)
- Auto-generated from `name` + `sku` using `pytils.translit.slugify`

---

### 6. Permissions

Custom permission: `IsAdminOrReadOnly`

- Safe methods (`GET`, `HEAD`) — allowed for all
- Write methods — only for staff/admins

---

### 7. Testing

- Uses `pytest` and `pytest-django`
- Factories via `factory_boy`
- `tests/` mirrors app structure (`models`, `serializers`, `views`, `services`)

---

### 8. Environment & Config

- `.env` file + `python-dotenv`
- DB creds, debug flags, secret key

---

### 9. Makefile Automation

```bash
make install         # Install production requirements
make install-dev     # Install development requirements
make test            # Run tests
make coverage        # Run tests with coverage
make lint            # Run all linters
make format          # Auto-format code
make graph           # Generate ER diagram
```

---

### 10. CI/CD (GitHub Actions)

- Automatically runs tests and lints on every push
- Postgres 13+ configured in pipeline
- Easy integration with `coverage.py` and report tools

---

### 11. ER Diagrams

Generated via:

```bash
make graph
```

Uses `django-extensions` + `pygraphviz`.

---

## 🐳 Docker Workflow

For local development and production, use the provided Makefile commands:

- **Development:**
  - `make docker-build-dev` — Build dev images
  - `make docker-up-dev` — Run dev containers
  - `make docker-down-dev` — Stop dev containers
- **Production:**

  - `make docker-build-prod` — Build prod images
  - `make docker-up-prod` — Run prod containers
  - `make docker-down-prod` — Stop prod containers

- Uses `.env.dev` and `.env.prod` for environment variables
- See `docker-compose.dev.yml` and `docker-compose.prod.yml` for details

---
