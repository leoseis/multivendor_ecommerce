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



Marketplace Connect – Full Stack Documentation
🛒 Marketplace Connect – Multivendor E‑commerce Platform

A full‑stack multivendor e‑commerce platform built with Django REST Framework (API) and React (Frontend). The system supports Admins, Vendors, and Customers, enabling vendors to manage products and customers to place orders through a secure API‑driven architecture.

🚀 Tech Stack
Backend

Python 3.12

Django 6+

Django REST Framework

SQLite (development)

JWT Authentication

Frontend

React

Axios

React Router

👥 User Roles
Role	Description
ADMIN	Full access via Django Admin
VENDOR	Manages own products & orders
CUSTOMER	Browses products & places orders
🔧 Backend (Django REST API)
📂 Project Structure
ecommerce_site/
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── manage.py
├── drf/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── admin.py
└── venv/
⚙️ Backend Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/
🔐 Authentication (JWT)
Login

POST /api/auth/login/

Payload

{
  "username": "vendor1",
  "password": "password123"
}

Response

{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
📦 Products API
Get all products (Public)

GET /api/products/

Response

[
  {
    "id": 1,
    "name": "Laptop",
    "price": "350000.00",
    "vendor": 2
  }
]
Vendor Products (Vendor only)

GET /api/vendor/products/

Headers

Authorization: Bearer <access_token>
🛒 Orders API
Create Order (Customer)

POST /api/orders/

Payload

{
  "items": [
    {"product": 1, "quantity": 2}
  ]
}

Response

{
  "order_id": 10,
  "status": "PENDING",
  "total": "700000.00"
}
Vendor Orders

GET /api/vendor/orders/

🎨 Frontend (React)
📂 Frontend Structure
src/
├── api/
│   └── axios.js
├── services/
│   ├── authService.js
│   ├── productService.js
│   └── orderService.js
├── pages/
│   ├── Login.jsx
│   ├── Products.jsx
│   ├── Cart.jsx
│   └── VendorDashboard.jsx
└── components/
⚙️ Frontend Setup
npm install
npm start

Frontend runs at:

http://localhost:3000
🔗 API Connection (Axios)
import axios from "axios";


const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});


api.interceptors.request.use(config => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export default api;
🧠 Frontend Auth Flow

User logs in

JWT token stored in localStorage

Axios automatically attaches token

Protected routes enabled

🔐 Security Best Practices

Admin access restricted to staff

Vendors can only access own data

Customers cannot access admin/vendor APIs

JWT used for authentication

🚀 Future Enhancements

Payment gateway (Paystack)

Product reviews

Vendor analytics dashboard

Order tracking

Deployment (Railway + Netlify)

👨‍💻 Author

Leonard Emelieze
Django & React Full‑Stack Developer
