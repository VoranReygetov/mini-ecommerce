# 🛍️ Product List App

Mini e-commerce feature: browse products, search by name, and view product details.  
Built with **FastAPI + PostgreSQL + React**.

---

## Features

### Frontend
- Browse product list in a grid
- Search products by name
- View product details

### Backend API Endpoints
- `GET /products` – Retrieve all products
- `GET /products/search?name=productname` – Search products by name
- `POST /products` – Add new product(s)
- `PUT /products/{product_id}` – Update product details
- `DELETE /products/{product_id}` – Delete a product

---

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL  
- **Frontend:** React (Vite), plain CSS  
- **DB ORM:** SQLAlchemy (async)  

---

## Setup

### 1. Backend

```bash
    cd backend
```

- Run the backend:
```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python main.py
```

### 2. Frontend

```bash
    cd frontend
    npm install
    npm run dev
```

- The React application will be at http://localhost:5173.

