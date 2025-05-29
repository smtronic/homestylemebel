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
  - [x] `/admin/cart/cart/<id>/history/` — View cart history
  - [x] `/admin/cart/cartitem/` — List cart items
  - [x] `/admin/cart/cartitem/add/` — Add cart item
  - [x] `/admin/cart/cartitem/<id>/change/` — Edit cart item
  - [x] `/admin/cart/cartitem/<id>/delete/` — Delete cart item
  - [x] `/admin/cart/cartitem/<id>/history/` — View cart item history

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
- [ ] Auto-generated API docs (Swagger/OpenAPI UI)

---

## 🔄 Phase 3: Orders

**Goal:** Support order creation for all users.

### Orders

- [ ] Models: `Order`, `OrderItem`
- [ ] Endpoints:
  - [ ] `POST /api/v1/orders/` — Create order
    - For guests: requires `full_name`, `phone`, `email`
    - For logged-in users: use profile data, but allow override
  - [ ] For **authenticated users** only:
    - [ ] `GET /api/v1/orders/` — List user's orders
    - [ ] `GET /api/v1/orders/{id}/` — Order detail

### Business logic

- [x] `OrderService`
- [ ] Validation: stock check, empty cart check, duplicate prevention

### Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Edge cases: stock issues, invalid user data

### Docs

- [ ] Update `api.md`
- [ ] Update `database.md`

---

## 🔄 Phase 4: Authentication

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

- [ ] Install **Django Debug Toolbar**:
  - [ ] Install via `pip install django-debug-toolbar`
  - [ ] Add `'debug_toolbar'` to `INSTALLED_APPS`
  - [ ] Include `debug_toolbar.middleware.DebugToolbarMiddleware` in `MIDDLEWARE`
  - [ ] Set `INTERNAL_IPS = ['127.0.0.1']` for local debugging
- [ ] Usage:
  - [ ] Provides detailed analysis of SQL queries, template rendering times, request/response cycle
  - [ ] Highlights performance issues like N+1 queries
  - [ ] Shows cache, signals, and other debug info

---

## 📌 Suggestions & Ideas

- [x] Add `drf-spectacular` for OpenAPI schema
- [ ] Add `drf-yasg` or Swagger UI for interactive API docs
- [ ] Rate limiting / throttling (for heavy endpoints)
- [ ] Review permissions (e.g., order access, admin-only features)
