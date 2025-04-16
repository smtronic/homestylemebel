# ✅ Project Roadmap — homestylemebel

Last updated: 2025-04-16

---

## ✅ Phase 1: Initial Setup & Architecture (COMPLETED)

**Goal:** Prepare project structure and core components.

- [x] Initialize Django project & Git repository
- [x] App-based project structure (`apps/`, `tests/`, `docs/`)
- [x] Custom user model (`users.User`)
- [x] Base models: `Category`, `Product`, `ProductExtraImage`
- [x] Requirements split: `base`, `dev`, `prod`
- [x] Makefile with common dev commands
- [x] Linters setup: `black`, `flake8`, `isort`
- [x] Code coverage and test structure
- [x] ER diagram with `django-extensions`

---

## 🚧 Phase 2: Public API (Catalog)

**Goal:** Provide product and category data to unauthenticated users.

### Categories

- [x] `GET /api/v1/categories/` — List
- [x] `GET /api/v1/categories/{slug}/` — Detail
- [x] Slug auto-generation
- [x] Capitalization of names

### Products

- [x] `GET /api/v1/products/` — List with search, filters and ordering
- [x] `GET /api/v1/products/{slug}/` — Detail view
- [x] Slug generation based on name + SKU
- [x] `ProductServices`: price calc, availability logic
- [x] Pagination, search (`?search=`), filter by category, price range, stock
- [x] Sorting by price, date, etc.

### Tests

- [x] Unit tests (models, services)
- [x] Integration tests (views, serializers)
- [x] Route tests

### Docs

- [x] `api.md`
- [x] `database.md`
- [x] `testing.md`
- [ ] Auto-generated API docs (Swagger/OpenAPI)

---

## 🐳 Phase 2.5: Docker & CI/CD

**Goal:** Containerized local dev and test automation.

- [ ] Dockerfile + docker-compose setup
- [ ] `.env` for env vars
- [ ] `make up`, `make down` commands
- [ ] GitHub Actions:
  - [x] Run tests
  - [ ] Lint check
  - [ ] Code coverage badge

---

## 🔄 Phase 3: Cart & Orders (Guest and Auth Users)

**Goal:** Support shopping cart and order creation for all users.

### Cart

- [x] Models: `Cart`, `CartItem`
- [ ] Endpoints:
  - [ ] `GET /api/v1/cart/`
  - [ ] `POST /api/v1/cart/add/`
  - [ ] `PATCH /api/v1/cart/update/{item_id}/`
  - [ ] `DELETE /api/v1/cart/remove/{item_id}/`
- [ ] Cart session handling (anon vs auth)
- [ ] Quantity validation (≤ product stock)

### Orders

- [x] Models: `Order`, `OrderItem`
- [ ] `POST /api/v1/orders/`:
  - For guests: requires `full_name`, `phone`, `email`
  - For logged-in users: use profile data, but allow override
- [ ] For **authenticated users** only:
  - [ ] `GET /api/v1/orders/` — list user's orders
  - [ ] `GET /api/v1/orders/{id}/` — order detail

### Business logic

- [x] `CartService`, `OrderService`
- [ ] Validation: stock check, empty cart check, duplicate prevention

### Testing

- [ ] Unit & integration tests

---

## 🔐 Phase 4: Authentication (JWT)

**Goal:** Add registration, login, profile, and secure API access.

- [ ] Register endpoint (`POST /api/v1/auth/register/`)
- [ ] Login endpoint (`POST /api/v1/auth/login/`)
- [ ] JWT auth with `djangorestframework-simplejwt`
- [ ] Profile endpoint (`GET /api/v1/users/me/`)
- [ ] Update profile (`PATCH /api/v1/users/me/`)
- [ ] Protected route access with token
- [ ] Tests for all endpoints

---

## 🛠 Phase 5: Debugging & Performance (Django Debug Toolbar)

**Goal:** Enable detailed debugging and performance insights in the development environment.

- [ ] Install **Django Debug Toolbar**:

  - [ ] Install via `pip install django-debug-toolbar`
  - [ ] Add `'debug_toolbar'` to `INSTALLED_APPS`
  - [ ] Include `debug_toolbar.middleware.DebugToolbarMiddleware` in `MIDDLEWARE`
  - [ ] Set `INTERNAL_IPS = ['127.0.0.1']` for local debugging

- [ ] Usage:
  - [ ] Provides detailed analysis of SQL queries, template rendering times, request/response cycle, and more
  - [ ] Highlights performance issues like N+1 queries
  - [ ] Shows cache, signals, and other useful debug info

---

## 🚀 Phase 6: Advanced Features

**Goal:** Improve UX, admin tooling, and scalability.

- [ ] Merge guest + user carts on login
- [ ] Celery: email notifications on order status updates
- [ ] Admin reports: sales statistics, top products
- [ ] Product attributes (color, size, material)
- [ ] OpenAPI UI (Swagger or ReDoc)

---

## 📌 Suggestions & Ideas

- [ ] Add `drf-spectacular` or `drf-yasg` for auto API docs
- [ ] Rate limiting / throttling (for heavy endpoints)
- [ ] Review permissions (e.g., order access, admin-only features)
