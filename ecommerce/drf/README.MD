Absolutely! Here’s a **professional, clear, and beginner-friendly README** for your **Multivendor E-commerce Django REST API**. I’ll include **all major endpoints**, example **payloads**, and **responses**. You can directly put this in your `README.md` on GitHub.

---

# 🛒 Multivendor E-commerce API

This is a **Django REST Framework API** for a **multivendor e-commerce platform**.
It allows vendors to register, create products, and users to browse products, add items to cart, place orders, and write reviews.

---

## 📦 Base URL

```text
http://localhost:8000/api/
```

---

## 🔑 Authentication

All endpoints that require a logged-in user **must include token authentication** (JWT or DRF Token).
Endpoints for creating vendors, products, carts, orders, and reviews require authentication.

---

## 📌 API Endpoints

### 1️⃣ Vendor Registration

* **Endpoint:**

```text
POST /api/vendor/create/
```

* **Payload:**

```json
{
  "store_name": "Leonard's Store",
  "description": "Selling tech gadgets"
}
```

* **Response:**

```json
{
  "id": 1,
  "store_name": "Leonard's Store",
  "description": "Selling tech gadgets",
  "is_active": true,
  "user": {
    "id": 1,
    "email": "leonard@example.com",
    "username": "leonard",
    "is_vendor": true
  }
}
```

---

### 2️⃣ Create Product (Vendor Only)

* **Endpoint:**

```text
POST /api/products/create/
```

* **Payload:**

```json
{
  "name": "Wireless Mouse",
  "slug": "wireless-mouse",
  "description": "Ergonomic wireless mouse",
  "price": "25.99",
  "stock": 50,
  "category": 1
}
```

* **Response:**

```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "slug": "wireless-mouse",
  "description": "Ergonomic wireless mouse",
  "price": "25.99",
  "stock": 50,
  "category": 1,
  "vendor": {
    "id": 1,
    "store_name": "Leonard's Store",
    "user": {
      "id": 1,
      "email": "leonard@example.com"
    }
  },
  "images": []
}
```

---

### 3️⃣ List All Products

* **Endpoint:**

```text
GET /api/products/
```

* **Response:**

```json
[
  {
    "id": 1,
    "name": "Wireless Mouse",
    "slug": "wireless-mouse",
    "description": "Ergonomic wireless mouse",
    "price": "25.99",
    "stock": 50,
    "category": 1,
    "vendor": {
      "id": 1,
      "store_name": "Leonard's Store",
      "user": {
        "id": 1,
        "email": "leonard@example.com"
      }
    },
    "images": []
  }
]
```

---

### 4️⃣ Add Item to Cart

* **Endpoint:**

```text
POST /api/cart/add/
```

* **Payload:**

```json
{
  "product_id": 1,
  "quantity": 2
}
```

* **Response:**

```json
{
  "message": "Item added to cart"
}
```

---

### 5️⃣ Create Order from Cart

* **Endpoint:**

```text
POST /api/order/create/
```

* **Payload:**

```json
{}
```

* **Response:**

```json
{
  "id": 1,
  "user": 1,
  "total_price": "51.98",
  "status": "Pending",
  "items": [
    {
      "id": 1,
      "order": 1,
      "vendor": 1,
      "product": {
        "id": 1,
        "name": "Wireless Mouse",
        "price": "25.99"
      },
      "price": "25.99",
      "quantity": 2
    }
  ]
}
```

---

### 6️⃣ Add Product Review

* **Endpoint:**

```text
POST /api/review/add/
```

* **Payload:**

```json
{
  "product": 1,
  "rating": 5,
  "comment": "Great mouse, highly recommend!"
}
```

* **Response:**

```json
{
  "message": "Review added"
}
```

---

## ⚡ Models Overview

| Model        | Description                                    |
| ------------ | ---------------------------------------------- |
| User         | Custom user with `is_vendor` field             |
| Vendor       | Represents a store and links to a user         |
| Category     | Product categories                             |
| Product      | Product info linked to vendor and category     |
| ProductImage | Optional product images                        |
| Cart         | User shopping cart                             |
| CartItem     | Products inside cart                           |
| Order        | Order created from cart                        |
| OrderItem    | Products inside an order                       |
| Review       | User product reviews                           |
| Payment      | Payment info (optional for future integration) |

---

## 🔧 Setup Instructions

```bash
# Clone the repository
git clone <your-repo-url>
cd ecommerce_site

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 📌 Notes

* Vendor can only create products if `is_vendor=True`.
* Cart is automatically created for users if not present.
* Orders are split per vendor automatically (each `OrderItem` has a vendor reference).
* `ImageField` requires Pillow: `pip install Pillow`.

---


