📦 E-Commerce Recommendation Platform

A full-stack web application that provides AI-powered product recommendations, a dynamic shopping cart, and a clean checkout experience. This project integrates a FastAPI backend with a React frontend for a seamless shopping workflow.

📋 Table of Contents

Features

Tech Stack

Project Structure

Prerequisites

Installation & Setup

Usage

API Endpoints

Future Enhancements

License

✨ Features

🤖 AI-Powered Recommendations — find similar products and search using natural language

🛍 Product Catalog — browse latest, random, and related items

🛒 Dynamic Shopping Cart — add/remove items with React Context state

🔍 Semantic Search — search products through text queries

💳 Seamless Checkout — full mock checkout UI flow

➕ Product Ingestion — UI to add new products to the catalog

📱 Responsive Design — works across desktop, tablet, and mobile

🎯 Modern Frontend + Fast API Integration

🛠 Tech Stack

Frontend

React.js

React Router

Axios

React Context

Backend

FastAPI

Pandas

Uvicorn

Torch (for embeddings / recommendations)

python-dotenv

Stripe (optional checkout mock)

📂 Project Structure
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
        │   └── ...
        ├── contexts/
        │   └── CartContext.js
        ├── pages/
        │   ├── HomePage.js
        │   ├── CartPage.js
        │   └── SimilarProductsPage.js
        ├── App.js
        └── index.js

🚀 Prerequisites

Node.js + npm

Python 3.8+

pip

🧩 Installation & Setup
1. Clone the Repository
git clone <your-repository-url>
cd <your-repository-name>

2. Backend Setup

Enter the backend folder:

cd backend


Create virtual environment:

python -m venv venv


Activate environment:

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate


Install dependencies:

pip install fastapi "uvicorn[standard]" pandas torch python-dotenv stripe


Create .env file:

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...


Run server:

uvicorn main:app --reload


Backend runs at:

http://localhost:8000

3. Frontend Setup
cd ../frontend


Install dependencies:

npm install


Create .env:

REACT_APP_API_BASE=http://localhost:8000


Start dev server:

npm start


Frontend runs at:

http://localhost:3000

📖 Usage

✔ Browse products on homepage
✔ Add items to cart
✔ Checkout using UI form
✔ Search for items via text
✔ View similar items from product page
✔ Add new products through admin UI

🔗 API Endpoints
Method	Endpoint	Description
GET	/latest	Fetch latest products
GET	/products/random?n=12	Fetch random products
GET	/products/{id}	Fetch product by ID
POST	/cart/add	Add item to cart
GET	/cart	Get cart contents
POST	/recommend	Get text-based recommendations
GET	/products/similar/{id}	Find similar products
🚧 Future Enhancements

Full Stripe checkout & webhooks

User authentication & profiles

Admin dashboard for product management

Replace CSV with PostgreSQL / MongoDB

Review & rating system

Personalized embeddings per user history
