# 🛒 HomestyleMebel API (Stage 2: Catalog & Cart - Public Endpoints)

## Overview

- **Base URL:** `/api/v1/`
- **Format:** JSON
- **Authentication:** Not required for public catalog and cart endpoints. Some cart actions require authentication or session.

---

## 📚 Catalog

### `GET /api/v1/categories/`

Retrieve a list of product categories.

**Query Parameters:**

- `search`: Search by name (e.g., `?search=chair`)
- `ordering`: Sort by fields (e.g., `?ordering=name` or `?ordering=-created_at`)

**Response:** `200 OK`

```json
[
  {
    "id": "uuid",
    "name": "Chairs",
    "slug": "chairs",
    "image": "/media/catalog/chairs.png",
    "description": "Comfortable seating options"
  }
]
```

### `GET /api/v1/categories/{slug}/`

Retrieve details of a specific category.

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "name": "Chairs",
  "slug": "chairs",
  "image": "/media/catalog/chairs.png",
  "description": "Comfortable seating options"
}
```

**Errors:**

- `404 Not Found`: Category not found.

### `GET /api/v1/products/`

Retrieve a list of products.

**Query Parameters:**

- `category`: Filter by category slug (e.g., `?category=chairs`)
- `search`: Search by name or SKU (e.g., `?search=wooden`)
- `price__gte`, `price__lte`: Filter by price range
- `stock__gte`: Filter by minimum stock
- `ordering`: Sort by fields (e.g., `?ordering=price` or `?ordering=-created_at`)

**Response:** `200 OK`

```json
[
  {
    "id": "uuid",
    "sku": "CHAIR-001",
    "name": "Wooden Chair",
    "slug": "wooden-chair-chair-001",
    "main_image": "/media/catalog/chair_001.png",
    "price": "3000.00",
    "discount": 10,
    "actual_price": "2700.00",
    "stock": 50,
    "category": {
      "id": "uuid",
      "name": "Chairs",
      "slug": "chairs"
    }
  }
]
```

### `GET /api/v1/products/{slug}/`

Retrieve details of a specific product by slug.

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "sku": "CHAIR-001",
  "name": "Wooden Chair",
  "slug": "wooden-chair-chair-001",
  "main_image": "/media/catalog/chair_001.png",
  "price": "3000.00",
  "discount": 10,
  "actual_price": "2700.00",
  "stock": 50,
  "category": {
    "id": "uuid",
    "name": "Chairs",
    "slug": "chairs"
  },
  "description": "A sturdy wooden chair."
}
```

**Errors:**

- `404 Not Found`: Product not found.

---

## 🛍 Cart

### `GET /api/v1/cart/`

Retrieve the current user's cart (anonymous or authenticated).

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "items": [
    {
      "id": "uuid",
      "product": {
        "id": "uuid",
        "sku": "CHAIR-001",
        "name": "Wooden Chair",
        "actual_price": "2700.00",
        "slug": "wooden-chair-chair-001"
      },
      "quantity": 2,
      "total_price": "5400.00",
      "is_available": true
    }
  ],
  "total": "5400.00",
  "created_at": "2025-05-28T11:14:00Z",
  "updated_at": "2025-05-28T11:14:00Z"
}
```

### `POST /api/v1/cart/add/`

Add a product to the cart.

**Request Body:**

```json
{
  "product_id": "uuid",
  "quantity": 2
}
```

**Response:** `201 Created`

```json
{
  "id": "uuid",
  "product": {
    "id": "uuid",
    "sku": "CHAIR-001",
    "name": "Wooden Chair",
    "actual_price": "2700.00",
    "slug": "wooden-chair-chair-001"
  },
  "quantity": 2,
  "total_price": "5400.00",
  "is_available": true
}
```

**Errors:**

- `400 Bad Request`: Invalid product ID or quantity exceeds stock.
- `404 Not Found`: Product not found.

### `PATCH /api/v1/cart/update/{item_id}/`

Update the quantity of a cart item.

**Request Body:**

```json
{
  "quantity": 3
}
```

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "product": {
    "id": "uuid",
    "sku": "CHAIR-001",
    "name": "Wooden Chair",
    "actual_price": "2700.00",
    "slug": "wooden-chair-chair-001"
  },
  "quantity": 3,
  "total_price": "8100.00",
  "is_available": true
}
```

**Errors:**

- `400 Bad Request`: Invalid quantity.
- `404 Not Found`: Cart item not found.

### `DELETE /api/v1/cart/remove/{item_id}/`

Remove an item from the cart.

**Response:** `204 No Content`

**Errors:**

- `404 Not Found`: Cart item not found.

---

## ✅ Implemented

- [x] `GET /api/v1/categories/`
- [x] `GET /api/v1/categories/{slug}/`
- [x] `GET /api/v1/products/`
- [x] `GET /api/v1/products/{slug}/`
- [x] `GET /api/v1/cart/`
- [x] `POST /api/v1/cart/add/`
- [x] `PATCH /api/v1/cart/update/{item_id}/`
- [x] `DELETE /api/v1/cart/remove/{item_id}/`

## 🧪 Testing

- All catalog and cart endpoints covered with unit and integration tests.
- Tested filters, search, ordering, data integrity, and cart operations (add, update, remove).
- Tests located in `tests/cart/` and `tests/catalog/`.

---

## 🚧 Upcoming (Next Stages)

- Order creation
- JWT Authentication
- Personal account APIs (user profile and order history)
- Auto-generated API docs (Swagger/OpenAPI)

---

📁 File References:

- Views: `apps/catalog/views.py`, `apps/cart/views.py`
- Serializers: `apps/catalog/serializers.py`, `apps/cart/serializers.py`
- Routes: `apps/catalog/urls.py`, `apps/cart/urls.py`
- Main router: `config/urls.py`
