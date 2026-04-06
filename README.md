code README.md
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

link to live link   --->  https://marketplace-connect.onrender.com/
