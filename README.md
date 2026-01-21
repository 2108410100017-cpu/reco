# 📦 E-Commerce Recommendation Platform

A full-stack web application that provides **AI-powered product recommendations**, a dynamic shopping cart, and a modern checkout flow using **FastAPI + React**.

---
- ![React](https://img.shields.io/badge/Frontend-React-61dafb?logo=react&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
- ![Python](https://img.shields.io/badge/Language-Python-3776ab?logo=python&logoColor=white)


## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project-Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation--Setup](#-installation--setup)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## ✨ Features

- 🤖 **AI Recommendations**
- 🔍 **Semantic Search**
- 🛍 **Product Catalog**
- 🛒 **React Shopping Cart**
- 💳 **Checkout UI**
- ➕ **Add Product Form**
- 📱 **Responsive Design**

---

## 🛠 Tech Stack

### **Frontend**
- React.js
- React Router
- Axios
- React Context

### **Backend**
- FastAPI
- Pandas
- Torch
- Uvicorn
- python-dotenv
- Stripe (mock)

---

## 📁 Project Structure

```
.
├── backend/
│   ├── routers/
│   │   ├── admin.py
│   │   ├── cart.py
│   │   ├── debug.py
│   │   ├── payment.py
│   │   ├── products.py
│   │   └── recommendations.py
│   ├── .env
│   ├── config.py
│   ├── database.py
│   └── main.py
│
└── frontend/
    ├── public/
    └── src/
        ├── components/
        │   ├── AddProduct.js
        │   ├── CheckoutPage.js
        │   ├── MockCheckoutForm.js
        │   ├── Navigation.js
        │   ├── ProductCard.js
        │   ├── ProductsYouLike.js
        ├── contexts/
        │   └── CartContext.js
        ├── pages/
        │   ├── HomePage.js
        │   ├── CartPage.js
        │   └── SimilarProductsPage.js
        ├── App.js
        └── index.js
```

---

## 🚀 Prerequisites

- Node.js + npm
- Python 3.8+
- pip

---

## 🛠 Installation & Setup

### **1. Clone Repository**

```bash
git clone <your-repository-url>
cd <your-folder>
```

### **2. Backend Setup**

```bash
cd backend
python -m venv venv
```

Activate env:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi "uvicorn[standard]" pandas torch python-dotenv stripe
```

Create `.env`:

```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Run server:

```bash
uvicorn main:app --reload
```

Backend available at:

> http://localhost:8000

---

### **3. Frontend Setup**

```bash
cd ../frontend
npm install
```

Create `.env`:

```
REACT_APP_API_BASE=http://localhost:8000
```

Run dev server:

```bash
npm start
```

Frontend available at:

> http://localhost:3000

---

## 📖 Usage

- Browse products
- Search similar products
- Add to cart
- Checkout UI flow
- Add new products from UI

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/latest` | Fetch latest products |
| GET | `/products/random?n=12` | Fetch random products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/cart/add` | Add item to cart |
| GET | `/cart` | Get cart items |
| POST | `/recommend` | Text recommendations |
| GET | `/products/similar/{id}` | Similar items |

---

## 🚧 Future Enhancements

- Full Stripe checkout
- User authentication
- Admin dashboard
- Database migration (Postgres/MongoDB)
- Reviews & ratings
- Personalized recommendations

---

