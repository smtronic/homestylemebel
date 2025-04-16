# Database Schema

## ER Diagram
![ER Diagram](image/er_diagram.png)

---

## Main Tables

### Users (`users_user`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `email`        | `VARCHAR(255)`     | `UNIQUE`, `INDEX`                         | Unique email (used for authentication)                                      |
| `phone`        | `PhoneNumberField` | `INDEX (partial)`                         | Phone number in the format +7XXXXXXXXXX (non-unique, region: RU)            |
| `first_name`   | `VARCHAR(255)`     | `BLANK=True`                              | User's first name                                                            |
| `last_name`    | `VARCHAR(255)`     | `BLANK=True`                              | User's last name                                                             |
| `is_active`    | `BOOLEAN`          | `DEFAULT=True`                            | Active status                                                                |
| `is_staff`     | `BOOLEAN`          | `DEFAULT=False`                           | Staff access to the admin panel                                              |
| `is_superuser` | `BOOLEAN`          | `DEFAULT=False`                           | Superuser (inherits from `PermissionsMixin`)                                  |
| `date_joined`  | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Date when the user registered                                                |
| `password`     | `VARCHAR(128)`     | `NOT NULL`                                | Hashed password (inherits from `AbstractBaseUser`)                           |
| `last_login`   | `TIMESTAMP`        | `NULL=True`                               | Last login time                                                               |

---

### Categories (`catalog_category`)

| Field         | Type               | Constraints/Indexes                        | Description                                                                 |
|---------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`          | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `name`        | `VARCHAR(100)`     | `UNIQUE`                                  | Category name (auto-capitalized upon saving)                                |
| `slug`        | `VARCHAR(150)`     | `UNIQUE`                                  | Slug identifier (automatically generated from name)                         |
| `image`       | `VARCHAR(255)`     | `DEFAULT="catalog/default.png"`           | Path to the category image                                                   |
| `description` | `TEXT`             | `NULL=True`                               | Description of the category                                                  |
| `created_at`  | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Creation date                                                                |
| `updated_at`  | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Last update date                                                             |

**Features:**
- **Auto-generate `slug`:** The `slug` field is generated automatically from the `name` field (e.g., "Living Room Furniture" → `living-room-furniture`).
- **Auto-capitalize `name`:** The `name` field is capitalized automatically (e.g., "chairs" → "Chairs").
- **Ordering:** Categories are ordered alphabetically (`ordering = ["name"]`).

---

### Products (`catalog_product`)

| Field               | Type               | Constraints/Indexes                        | Description                                                                 |
|---------------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`                | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `name`              | `VARCHAR(200)`     |                                           | Product name (auto-capitalized upon saving)                                 |
| `sku`               | `VARCHAR(50)`      | `UNIQUE`, `INDEX`                         | Product SKU (e.g., `PROD-001`)                                               |
| `price`             | `DECIMAL(10,2)`    | `INDEX`, `CHECK (>= 0)`                   | Base price (used to calculate `actual_price`)                               |
| `discount`          | `SMALLINT`         | `DEFAULT=0`, `CHECK (0 <= discount <= 100)` | Discount percentage (automatically calculates `actual_price`)               |
| `stock`             | `INT`              | `DEFAULT=0`, `CHECK (>= 0)`               | Stock quantity                                                              |
| `category_id`       | `UUID`             | `FK (catalog_category), NULL=True`         | Foreign key to Category (set to NULL if Category is deleted)                |
| `main_image`        | `VARCHAR(255)`     | `DEFAULT="catalog/default.png"`           | Path to the main product image                                               |
| `slug`              | `VARCHAR(150)`     | `UNIQUE`, `INDEX`                         | Slug identifier (generated from `name` and `sku`)                           |
| `description`       | `TEXT`             | `NULL=True`                               | Product description                                                          |
| `created_at`        | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Product creation date                                                        |
| `updated_at`        | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Product last update date                                                     |
| `available_for_order` | `BOOLEAN`        | `DEFAULT=True`, `DB_INDEX=True`           | Available for order flag (indexed)                                           |
| `_actual_price`     | `DECIMAL(10,2)`    | `EDITABLE=False`, `DEFAULT=0.00`          | Price after discount (calculated automatically)                             |
| `availability_status` | `VARCHAR(20)`     | `DB_INDEX=True`, `EDITABLE=False`         | Availability status (`in_stock`, `backorder`, `unavailable`)                |

**Features:**
- **Auto-generate `slug`:** The `slug` is generated from `name` and `sku` using transliteration (e.g., "Wooden Chair (STL-001)" → `wooden-chair-stl-001`).
- **Actual Price Calculation:** `actual_price = price * (100 - discount) / 100` (rounded to 2 decimal places).
- **Indexes:** Separate indexes are created for `sku`, `price`, and `slug` to speed up searching.

---

### Product Extra Images (`catalog_productextraimage`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `product_id`   | `UUID`             | `FK (catalog_product)`                    | Foreign key to the Product                                                  |
| `image`        | `VARCHAR(255)`     |                                           | Path to the additional product image                                         |
| `ordering`     | `INT`              | `DEFAULT=0`, `CHECK (>= 0)`               | Display order (automatically increases when new images are added)            |
| `created_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Image creation date                                                          |
| `updated_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Image last update date                                                       |

**Features:**
- **Auto-increment `ordering`:** If `ordering` is not specified, it is automatically set to the next available order.
- **Sorting:** Images are sorted by the `ordering` field (ascending).

---

### Cart (`cart_cart`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `user`         | `UUID`             | `FK (users_user), NULL=True`              | Foreign key to the User (NULL for anonymous users)                           |
| `session_key`  | `VARCHAR(40)`      | `NULL=True`                               | Session key for anonymous users                                              |
| `created_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Cart creation date                                                           |
| `updated_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Cart last update date                                                        |

**Features:**
- **Auto-linking:** For anonymous users, `session_key` is used; for authenticated users, `user` is used.
- **`total`:** Calculates the total price of the cart: `sum(item.total_price for item in items.all())`.

---

### Cart Item (`cart_cartitem`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `cart`         | `UUID`             | `FK (cart_cart)`                          | Foreign key to the Cart                                                     |
| `product`      | `UUID`             | `FK (catalog_product)`                    | Foreign key to the Product                                                  |
| `quantity`     | `INT`              | `>=1`                                     | Product quantity                                                            |
| `price`        | `DECIMAL(10,2)`    |                                           | Price of the product at the time of adding to the cart                      |

**Features:**
- **Stock validation:** Ensures that `quantity <= product.stock` when saving.
- **Automatic price assignment:** If `price` is not provided, `product.actual_price` is used.
- **`total_price`:** Calculates the total price of an item: `price * quantity`.

---

### Orders (`orders_order`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `cart`         | `UUID`             | `OneToOne (cart_cart)`                    | One-to-one relation with Cart                                               |
| `full_name`    | `VARCHAR(255)`     |                                           | Recipient's full name                                                       |
| `phone`        | `PhoneNumberField` | `INDEX (partial)`                         | Contact phone number                                                         |
| `email`        | `VARCHAR(255)`     | `NULL=True`                               | Contact email (optional)                                                    |
| `status`       | `VARCHAR(20)`      | `ENUM: new, processing, completed, cancelled` | Order status (`new` by default)                                             |
| `created_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Order creation date                                                          |
| `updated_at`   | `TIMESTAMP`        | `DEFAULT=timezone.now`                    | Last update date                                                             |

**Features:**
- **One-to-one with Cart:** This creates a strict relationship with a cart (`on_delete=models.Cascade` to delete the cart when the order is deleted).
- **`total`:** Calculates the total price of the order: `sum(item.total_price for item in items.all())`.
- **Statuses:**
  - `new` — Order is created but not processed
  - `processing` — Order is being processed
  - `completed` — Order is completed
  - `cancelled` — Order is cancelled

---

### Order Item (`orders_orderitem`)

| Field          | Type               | Constraints/Indexes                        | Description                                                                 |
|----------------|--------------------|-------------------------------------------|-----------------------------------------------------------------------------|
| `id`           | `UUID`             | `PK`                                      | Primary Key                                                                 |
| `order`        | `UUID`             | `FK (orders_order)`                       | Foreign key to the Order                                                    |
| `product`      | `UUID`             | `FK (catalog_product)`                    | Foreign key to the Product                                                  |
| `quantity`     | `INT`              | `>=1`                                     | Product quantity                                                            |
| `price`        | `DECIMAL(10,2)`    |                                           | Price of the product at the time of the order                               |

**Features:**
- **Stock validation:** Ensures that `quantity <= product.stock` when saving.
- **Automatic price assignment:** If `price` is not provided, `product.actual_price` is used.
- **`total_price`:** Calculates the total price of an item: `price * quantity`.

---

## Business Logic

### Order Processing

1. **`OrderService`:**
   - **`create_order_from_cart`:**
     - Creates an order from the cart with stock validation.
     - Decreases the `stock` of products in the catalog.
     - Deletes the cart after successful order creation.
   - **`cancel_order`:**
     - Returns products to the stock if the order is cancelled.
     - Cancellation of completed orders is not allowed.

2. **Transactions:**
   Methods like `create_order_from_cart` and `cancel_order` are executed in atomic transactions to ensure data integrity.

3. **Validations:**
   - Prevent creating an order with an empty cart.
   - Check available product quantities before placing an order.

### Working with Cart

1. **`CartService`:**
   - **`get_or_create_cart(request)`:**
     Creates a cart for anonymous or authenticated users.
   - **`add_to_cart(cart, product, quantity)`:**
     Adds a product to the cart with stock validation. If the product is already in the cart, the quantity is increased.

2. **Validations:**
   - In `CartItem`, `quantity > product.stock` is not allowed.
   - In `Cart`, either `user` or `session_key` must be set.

3. **Transactions:**
   The `add_to_cart` method is executed within an atomic transaction to ensure data consistency.
