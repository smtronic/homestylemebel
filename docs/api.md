# 🛒 HomestyleMebel API (Stage 2: Catalog - Public Endpoints)

## Overview

- **Base URL:** `/api/v1/`
- **Format:** JSON
- **Authentication:** Not required for public catalog endpoints.

---

## 🔹 Categories

### `GET /api/v1/categories/`

Retrieve the list of product categories.

**Response:** `200 OK`

```json
[
  {
    "id": "uuid",
    "name": "Tables",
    "slug": "tables",
    "description": "",
    "image": "http://localhost:8000/media/catalog/default.png"
  }
]
```

### `GET /api/v1/categories/{slug}/`

Retrieve details of a specific category by slug.

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "name": "Chairs",
  "slug": "chairs",
  "description": "",
  "image": "http://localhost:8000/media/catalog/categories/chairs.jpg"
}
```

---

## 🔹 Products

### `GET /api/v1/products/`

Retrieve a list of products with filters and search.

**Query Parameters:**

- `search`: Search by name, description, or SKU.
- `category`: Filter by category slug.
- `ordering`: Sort by `price`, `-price`, `sku`, etc.

**Example:**

```
GET /api/v1/products/?search=chair&category=chairs&ordering=-price
```

**Response:** `200 OK`

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "sku": "CHAIR-001",
      "name": "Wooden Chair",
      "price": "3000.00",
      "discount": 10,
      "actual_price": "2700.00",
      "main_image": "http://localhost:8000/media/catalog/products/main/chair.jpg",
      "stock": 15,
      "category": "chairs"
    }
  ]
}
```

### `GET /api/v1/products/{slug}/`

Retrieve details of a specific product by slug.

**Response:** `200 OK`

```json
{
  "sku": "CHAIR-001",
  "name": "Wooden Chair",
  "description": "Comfortable wooden chair.",
  "price": "3000.00",
  "discount": 10,
  "actual_price": "2700.00",
  "stock": 15,
  "main_image": "http://localhost:8000/media/catalog/products/main/chair.jpg",
  "extra_images": [
    {
      "image": "http://localhost:8000/media/catalog/products/extra/chair1.jpg"
    },
    { "image": "http://localhost:8000/media/catalog/products/extra/chair2.jpg" }
  ],
  "category": {
    "id": "uuid",
    "name": "Chairs",
    "slug": "chairs",
    "description": "",
    "image": "http://localhost:8000/media/catalog/categories/chairs.jpg"
  },
  "slug": "wooden-chair-chair-001"
}
```

---

## ✅ Implemented

- [x] `GET /api/v1/categories/`
- [x] `GET /api/v1/categories/{slug}/`
- [x] `GET /api/v1/products/`
- [x] `GET /api/v1/products/{slug}/`

## 🧪 Testing

- All endpoints covered with unit and integration tests.
- Tested filters, search, ordering, and data integrity.

---

## 🚧 Upcoming (Next Stages)

- Cart (anonymous + authenticated users)
- Order creation
- JWT Authentication
- Personal account APIs (user profile and order history)

---

📁 File References:

- Views: `apps/catalog/views.py`
- Serializers: `apps/catalog/serializers.py`
- Routes: `apps/catalog/urls.py`
- Main router: `config/urls.py`
