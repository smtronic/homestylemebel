# ✅ Project Roadmap — homestylemebel

Last updated: 2025-05-29

---

## ✅ Phase 1: Setup & Models

- [x] Django project setup
- [x] Models: `User`, `Category`, `Product`, `ProductExtraImage`
- [x] Custom user model (email-based auth)
- [x] Database migrations
- [x] Admin panel customization

---

## ✅ Phase 2: Public API (Catalog & Cart)

**Goal:** Provide product, category, and cart data to unauthenticated and authenticated users.

### Categories

- [x] Models: `Category`
- [x] Endpoints:
  - [x] `GET /api/v1/categories/`
  - [x] `GET /api/v1/categories/{slug}/`
- [x] Filters: search, ordering

### Products

- [x] Models: `Product`, `ProductExtraImage`
- [x] Endpoints:
  - [x] `GET /api/v1/products/`
  - [x] `GET /api/v1/products/{slug}/`
- [x] Pagination, search (`?search=`), filter by category, price range, stock
- [x] Sorting by price, date, etc.

### Cart

- [x] Models: `Cart`, `CartItem`
- [x] Endpoints:
  - [x] `GET /api/v1/cart/` — Retrieve list of items in current cart
  - [x] `POST /api/v1/cart/add/` — Add product to cart
  - [x] `PATCH /api/v1/cart/<pk>/update/` — Update cart item quantity
  - [x] `DELETE /api/v1/cart/<pk>/remove/` — Remove cart item
  - [x] `GET /api/v1/cart/detail/` — Get current cart details (items, total)
- [x] Cart session handling (anonymous via `session_key`, authenticated via `user`)
- [x] Quantity validation (≤ product stock)
- [x] Product existence and availability validation (`available_for_order`)
- [x] API documentation with `drf-spectacular` (OpenAPI schema)
- [x] Admin panel routes:
  - [x] `/admin/cart/cart/` — List carts
  - [x] `/admin/cart/cart/add/` — Add cart
  - [x] `/admin/cart/cart/<id>/change/` — Edit cart
  - [x] `/admin/cart/cart/<id>/delete/` — Delete cart
  - [x] `/admin/cart/cartitem/` — List cart items
  - [x] `/admin/cart/cartitem/add/` — Add cart item
  - [x] `/admin/cart/cartitem/<id>/change/` — Edit cart item
  - [x] `/admin/cart/cartitem/<id>/delete/` — Delete cart item

### Tests

- [x] Unit tests (models, services, serializers)
- [x] Integration tests (views, permissions, endpoints)
- [x] Route tests (API and admin routes)
- [x] Cart operation tests (add, update, remove, detail, session handling)

### Docs

- [x] `api.md`
- [x] `database.md`
- [x] `testing.md`
- [x] OpenAPI schema with `drf-spectacular`
- [x] Auto-generated API docs (Swagger/OpenAPI UI)

---

## 🔄 Phase 3: Orders

**Goal:** Support order creation for all users.

### Orders

- [x] Models: `Order`, `OrderItem`
- [x] Endpoints:
  - [x] `POST /api/v1/orders/` — Create order
    - For guests: requires `full_name`, `phone`, `email`
    - For logged-in users: use profile data, but allow override
  - [x] For **authenticated users** only:
    - [x] `GET /api/v1/orders/` — List user's orders
    - [x] `GET /api/v1/orders/{id}/` — Order detail
    - [x] `POST /api/v1/orders/{id}/cancel/` — Cancel order (admin only)
    - [x] `PATCH /api/v1/orders/{id}/edit/` — Edit order contact info

### Business logic

- [x] `OrderService`
- [x] Validation: stock check, empty cart check, duplicate prevention

### Testing

- [x] Unit tests
- [x] Integration tests
- [x] Edge cases: stock issues, invalid user data

### Docs

- [x] Update `api.md`
- [x] Update `database.md`

---

## ✅ Phase 4: Authentication

**Goal:** Enable secure user authentication.

- [ ] JWT Authentication (django-rest-framework-simplejwt)
- [ ] Endpoints:
  - [ ] `POST /api/v1/auth/login/`
  - [ ] `POST /api/v1/auth/refresh/`
  - [ ] `POST /api/v1/auth/register/`
  - [ ] `GET /api/v1/users/me/` — User profile
  - [ ] `PATCH /api/v1/users/me/` — Update profile
- [ ] Password reset flow
- [ ] Email confirmation

---

## 🔄 Phase 5: Debugging Tools

**Goal:** Enable detailed debugging and performance insights in the development environment.

- [x] Install **Django Debug Toolbar**
- [x] Add `'debug_toolbar'` to `INSTALLED_APPS` in dev
- [x] Include `debug_toolbar.middleware.DebugToolbarMiddleware` in `MIDDLEWARE` in dev
- [x] Set `INTERNAL_IPS = ['127.0.0.1']` for local debugging
- [x] Usage: SQL queries, template rendering, request/response cycle, N+1 queries, cache, signals, etc.

---

## 📌 Suggestions & Ideas

- [x] Add `drf-spectacular` for OpenAPI schema
- [x] Swagger UI/Redoc for interactive API docs
- [ ] Rate limiting / throttling (for heavy endpoints)
- [ ] Review permissions (e.g., order access, admin-only features)
