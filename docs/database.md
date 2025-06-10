# Database Schema

## ER Diagram

![ER Diagram](image/er_diagram.png)

---

## Main Tables

### Users (`users_user`)

| Field          | Type               | Constraints/Indexes    | Description                                                  |
| -------------- | ------------------ | ---------------------- | ------------------------------------------------------------ |
| `id`           | `UUID`             | `PK`                   | Primary Key                                                  |
| `email`        | `VARCHAR(255)`     | `UNIQUE`, `INDEX`      | Unique email (used for authentication)                       |
| `phone`        | `PhoneNumberField` |                        | Phone number in format +7XXXXXXXXXX (non-unique, region: RU) |
| `first_name`   | `VARCHAR(255)`     | `BLANK=True`           | User's first name                                            |
| `last_name`    | `VARCHAR(255)`     | `BLANK=True`           | User's last name                                             |
| `is_active`    | `BOOLEAN`          | `DEFAULT=True`         | Active status                                                |
| `is_staff`     | `BOOLEAN`          | `DEFAULT=False`        | Staff access to admin panel                                  |
| `is_superuser` | `BOOLEAN`          | `DEFAULT=False`        | Superuser status                                             |
| `date_joined`  | `TIMESTAMP`        | `DEFAULT=timezone.now` | Date of user registration                                    |
| `password`     | `VARCHAR(128)`     | `NOT NULL`             | Hashed password (inherited from `AbstractBaseUser`)          |
| `last_login`   | `TIMESTAMP`        | `NULL=True`            | Last login time                                              |

**Features:**

- **Email-based authentication**: `email` is the `USERNAME_FIELD`.
- **Methods**: `get_full_name()` returns `first_name last_name`, `get_short_name()` returns `first_name`.

---

### Categories (`catalog_category`)

| Field         | Type           | Constraints/Indexes             | Description                                                                  |
| ------------- | -------------- | ------------------------------- | ---------------------------------------------------------------------------- |
| `id`          | `UUID`         | `PK`                            | Primary Key                                                                  |
| `name`        | `VARCHAR(100)` | `UNIQUE`                        | Category name (auto-capitalized on save)                                     |
| `slug`        | `VARCHAR(150)` | `UNIQUE`, `INDEX`               | Slug identifier (auto-generated from `name` using `pytils.translit.slugify`) |
| `image`       | `ImageField`   | `DEFAULT="catalog/default.png"` | Path to category image                                                       |
| `description` | `TEXT`         | `NULL=True`, `BLANK=True`       | Category description                                                         |
| `created_at`  | `TIMESTAMP`    | `DEFAULT=timezone.now`          | Creation date                                                                |
| `updated_at`  | `TIMESTAMP`    | `DEFAULT=timezone.now`          | Last update date                                                             |

**Features:**

- **Auto-generate `slug`**: Generated from `name` (e.g., "Living Room" → `living-room`).
- **Auto-capitalize `name`**: `name` is capitalized on save (e.g., "chairs" → "Chairs").
- **Ordering**: Categories sorted alphabetically by `name`.

---

### Products (`catalog_product`)

| Field                 | Type            | Constraints/Indexes                         | Description                                        |
| --------------------- | --------------- | ------------------------------------------- | -------------------------------------------------- |
| `id`                  | `UUID`          | `PK`                                        | Primary Key                                        |
| `name`                | `VARCHAR(200)`  |                                             | Product name (auto-capitalized on save)            |
| `sku`                 | `VARCHAR(50)`   | `UNIQUE`, `INDEX`                           | Product SKU (e.g., `CHAIR-001`)                    |
| `price`               | `DECIMAL(10,2)` | `INDEX`, `CHECK (>= 0)`                     | Base price                                         |
| `discount`            | `SMALLINT`      | `DEFAULT=0`, `CHECK (0 <= discount <= 100)` | Discount percentage                                |
| `stock`               | `INT`           | `DEFAULT=0`, `CHECK (>= 0)`                 | Stock quantity                                     |
| `category_id`         | `UUID`          | `FK (catalog_category), NULL=True`          | Foreign key to Category (NULL if category deleted) |
| `main_image`          | `ImageField`    | `DEFAULT="catalog/default.png"`             | Path to main product image                         |
| `slug`                | `VARCHAR(150)`  | `UNIQUE`, `INDEX`                           | Slug identifier (generated from `name` and `sku`)  |
| `description`         | `TEXT`          | `NULL=True`, `BLANK=True`                   | Product description                                |
| `created_at`          | `TIMESTAMP`     | `DEFAULT=timezone.now`                      | Creation date                                      |
| `updated_at`          | `TIMESTAMP`     | `DEFAULT=timezone.now`                      | Last update date                                   |
| `available_for_order` | `BOOLEAN`       | `DEFAULT=True`, `DB_INDEX=True`             | Flag indicating if product can be ordered          |
| `_actual_price`       | `DECIMAL(10,2)` | `EDITABLE=False`, `DEFAULT=0.00`            | Price after discount (calculated)                  |
| `availability_status` | `VARCHAR(20)`   | `DB_INDEX=True`, `EDITABLE=False`           | Status: `in_stock`, `backorder`, `unavailable`     |

**Features:**

- **Auto-generate `slug`**: Generated from `name` and `sku` (e.g., "Wooden Chair (CHAIR-001)" → `wooden-chair-chair-001`).
- **Actual Price Calculation**: `_actual_price = price * (100 - discount) / 100`, rounded to 2 decimal places.
- **Indexes**: On `slug`, `sku`, `price`, and `availability_status, stock` for efficient queries.
- **Validation**: `discount` between 0 and 100, `price` and `stock` non-negative.

---

### Product Extra Images (`catalog_productextraimage`)

| Field        | Type         | Constraints/Indexes         | Description                                       |
| ------------ | ------------ | --------------------------- | ------------------------------------------------- |
| `id`         | `UUID`       | `PK`                        | Primary Key                                       |
| `product_id` | `UUID`       | `FK (catalog_product)`      | Foreign key to Product                            |
| `image`      | `ImageField` |                             | Path to additional product image                  |
| `ordering`   | `INT`        | `DEFAULT=0`, `CHECK (>= 0)` | Display order (auto-incremented if not specified) |
| `created_at` | `TIMESTAMP`  | `DEFAULT=timezone.now`      | Creation date                                     |
| `updated_at` | `TIMESTAMP`  | `DEFAULT=timezone.now`      | Last update date                                  |

**Features:**

- **Auto-increment `ordering`**: Set to next available order if not specified.
- **Sorting**: Images ordered by `ordering` (ascending).

---

### Cart (`cart_cart`)

| Field         | Type          | Constraints/Indexes          | Description                                                     |
| ------------- | ------------- | ---------------------------- | --------------------------------------------------------------- |
| `id`          | `UUID`        | `PK`                         | Primary Key                                                     |
| `user`        | `UUID`        | `FK (users_user), NULL=True` | Foreign key to User (NULL for anonymous users)                  |
| `session_key` | `VARCHAR(40)` | `NULL=True`, `INDEX`         | Session key for anonymous users (20-40 alphanumeric characters) |
| `created_at`  | `TIMESTAMP`   | `DEFAULT=timezone.now`       | Creation date                                                   |
| `updated_at`  | `TIMESTAMP`   | `DEFAULT=timezone.now`       | Last update date                                                |

**Features:**

- **Auto-linking**: Uses `user` for authenticated users or `session_key` for anonymous users.
- **Constraint**: At least one of `user` or `session_key` must be set.
- **Total**: Calculated as `sum(item.total_price for item in items.all())`, rounded to 2 decimal places.
- **Indexes**: On `user` and `session_key` for efficient lookups.

---

### Cart Item (`cart_cartitem`)

| Field      | Type   | Constraints/Indexes               | Description                                      |
| ---------- | ------ | --------------------------------- | ------------------------------------------------ |
| `id`       | `UUID` | `PK`                              | Primary Key                                      |
| `cart`     | `UUID` | `FK (cart_cart)`                  | Foreign key to Cart                              |
| `product`  | `UUID` | `FK (catalog_product), NULL=True` | Foreign key to Product (NULL if product deleted) |
| `quantity` | `INT`  | `>=1`                             | Quantity of product                              |

**Features:**

- **Price Calculation**: Uses `product.actual_price` if product exists and is available, else `0.00`.
- **Total Price**: `product.actual_price * quantity`, rounded to 2 decimal places.
- **Validation**:
  - `quantity` must not exceed `product.stock`.
  - Product must exist and be `available_for_order`.
- **Unique Constraint**: One product per cart (for non-NULL products).
- **Indexes**: On `cart` and `product` for efficient queries.

---

### Orders (`orders_order`)

| Field        | Type               | Constraints/Indexes       | Description                                                 |
| ------------ | ------------------ | ------------------------- | ----------------------------------------------------------- |
| `id`         | `UUID`             | `PK`                      | Primary Key                                                 |
| `cart`       | `UUID`             | `OneToOne (cart_cart)`    | One-to-one relation with Cart                               |
| `full_name`  | `VARCHAR(255)`     |                           | Recipient's full name                                       |
| `phone`      | `PhoneNumberField` |                           | Contact phone number (region: RU)                           |
| `email`      | `VARCHAR(255)`     | `NULL=True`, `BLANK=True` | Contact email (optional)                                    |
| `status`     | `VARCHAR(20)`      | `DEFAULT="new"`           | Order status: `new`, `processing`, `completed`, `cancelled` |
| `created_at` | `TIMESTAMP`        | `DEFAULT=timezone.now`    | Creation date                                               |
| `updated_at` | `TIMESTAMP`        | `DEFAULT=timezone.now`    | Last update date                                            |

**Features:**

- **One-to-one with Cart**: Deletes cart if order is deleted (`on_delete=models.CASCADE`).
- **Total**: Calculated as `sum(item.total_price for item in items.all())`.
- **Statuses**: Enum-like choices for order lifecycle.

---

### Order Item (`orders_orderitem`)

| Field      | Type            | Constraints/Indexes    | Description                                      |
| ---------- | --------------- | ---------------------- | ------------------------------------------------ |
| `id`       | `UUID`          | `PK`                   | Primary Key                                      |
| `order`    | `UUID`          | `FK (orders_order)`    | Foreign key to Order                             |
| `product`  | `UUID`          | `FK (catalog_product)` | Foreign key to Product (protected from deletion) |
| `quantity` | `INT`           | `>=1`                  | Quantity of product                              |
| `price`    | `DECIMAL(10,2)` |                        | Price at time of order                           |

**Features:**

- **Validation**: `quantity` must not exceed `product.stock`.
- **Price Assignment**: Defaults to `product.actual_price` if not set.
- **Total Price**: `price * quantity`, rounded to 2 decimal places.
- **Unique Constraint**: One product per order.
- **Protection**: `on_delete=models.PROTECT` prevents product deletion if referenced.

---

## Business Logic

### Order Processing

1. **`OrderService`:**

   - **`create_order_from_cart`**:
     - Creates order from cart with stock validation.
     - Decrements product `stock`.
     - Deletes cart after order creation.
   - **`cancel_order`**:
     - Restores product `stock` if order cancelled.
     - Prohibits cancellation of `completed` orders.

2. **Transactions**: Methods like `create_order_from_cart` and `cancel_order` use atomic transactions for data integrity.

3. **Validations**:
   - Prevents orders from empty carts.
   - Validates product stock before order creation.

### Working with Cart

1. **`CartService`:**

   - **`get_or_create_cart(request)`**: Creates/retrieves cart for anonymous (`session_key`) or authenticated (`user`) users.
   - **`add_to_cart(cart, product, quantity)`**: Adds product with stock validation, updates quantity if product exists.
   - **`update_cart_item(cart_item, quantity)`**: Updates item quantity with stock validation.
   - **`remove_from_cart(cart_item)`**: Removes item from cart.

2. **Validations**:

   - `quantity <= product.stock` in `CartItem`.
   - Product must exist and be `available_for_order`.
   - `Cart` requires either `user` or `session_key`.

3. **Transactions**: `add_to_cart`, `update_cart_item`, and `remove_from_cart` use atomic transactions for consistency.
