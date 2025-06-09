# 🛒 HomestyleMebel API & Admin Routes

## Overview

- **Base API URL:** `/api/v1/`
- **Admin URL:** `/admin/`
- **Format:** JSON (API)
- **Authentication:** Not required for public catalog/cart endpoints. Orders and user profile require authentication.

---

## 🛠 Django Admin Routes

- `/admin/` — Main admin dashboard
- `/admin/catalog/category/` — Manage categories
- `/admin/catalog/product/` — Manage products
- `/admin/cart/cart/` — Manage carts
- `/admin/cart/cartitem/` — Manage cart items
- `/admin/orders/order/` — Manage orders
- `/admin/orders/orderitem/` — Manage order items
- `/admin/users/user/` — Manage users

Each model supports:

- List, add, change, delete, view history
- Example: `/admin/catalog/product/add/`, `/admin/catalog/product/<id>/change/`

---

## 📚 Catalog API

- `GET /api/v1/catalog/categories/` — List categories
- `GET /api/v1/catalog/categories/{slug}/` — Category details
- `GET /api/v1/catalog/products/` — List products (filters, search, ordering)
- `GET /api/v1/catalog/products/{slug}/` — Product details

**Query params:**

- `search`, `ordering`, `category`, `price__gte`, `price__lte`, `stock__gte`

---

## 🛒 Cart API

- `GET /api/v1/carts/` — List all carts (admin only)
- `GET /api/v1/carts/detail/` — Get current user's cart
- `POST /api/v1/carts/add/` — Add product to cart
- `PATCH /api/v1/carts/{item_id}/update/` — Update cart item quantity
- `DELETE /api/v1/carts/{item_id}/remove/` — Remove item from cart

---

## 📦 Orders API

- `GET /api/v1/orders/` — List user's orders (auth required)
- `POST /api/v1/orders/` — Create order from cart
- `GET /api/v1/orders/{id}/` — Order details (auth required)
- `POST /api/v1/orders/{id}/cancel/` — Cancel order (admin only)
- `PATCH /api/v1/orders/{id}/edit/` — Edit order contact info (if not completed)

---

## 🔐 Auth API (Planned)

- `POST /api/v1/auth/login/` — Login (JWT)
- `POST /api/v1/auth/register/` — Register
- `POST /api/v1/auth/refresh/` — Refresh JWT
- `GET /api/v1/users/me/` — User profile
- `PATCH /api/v1/users/me/` — Update profile

---

## 🗂 API Schema & Docs

- `/api/v1/schema/` — OpenAPI schema (YAML/JSON)
- `/api/v1/schema/swagger-ui/` — Swagger UI (interactive docs)
- `/api/v1/schema/redoc/` — Redoc (alternative docs)

---

## 📝 Notes

- All admin routes available at `/admin/` and subroutes per model.
- All API endpoints are versioned under `/api/v1/`.
- For full details, see Swagger or Redoc UI.

---

## 📁 File References

- Views: `apps/catalog/views.py`, `apps/cart/views.py`, `apps/orders/views.py`
- Serializers: `apps/catalog/serializers.py`, `apps/cart/serializers.py`, `apps/orders/serializers.py`
- Routes: `apps/catalog/urls.py`, `apps/cart/urls.py`, `apps/orders/urls.py`
- Main router: `config/urls.py`
