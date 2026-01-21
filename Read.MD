E-Commerce Recommendation Platform
A full-stack web application that provides AI-powered product recommendations, a dynamic shopping cart, and a seamless checkout experience. This project demonstrates the integration of a Python/FastAPI backend with a React frontend.

License
React
FastAPI
Python

📖 Table of Contents
Features
Tech Stack
Project Structure
Prerequisites
Installation & Setup
Usage
API Endpoints
Future Enhancements
✨ Features
🤖 AI-Powered Recommendations: Get product suggestions based on text queries or similar items.
🛒 Dynamic Shopping Cart: Add/remove items with real-time updates using React Context.
🔍 Advanced Search: Find products using natural language queries.
🛍️ Product Catalog: Browse through random, latest, and similar products.
💳 Seamless Checkout UI: A complete, frontend-only checkout flow for a smooth user experience.
➕ Add Products: A dedicated UI for businesses to add new products to the catalog.
📱 Responsive Design: A clean and modern UI that works on all device sizes.
🛠️ Tech Stack
Frontend
React.js
React Router for navigation
Axios for API requests
React Context for state management
Backend
FastAPI for the API framework
Pandas for data manipulation
Uvicorn for the ASGI server
Python
📁 Project Structure

.
├── backend/
│   ├── routers/
│   │   ├── admin.py
│   │   ├── cart.py
│   │   ├── debug.py
│   │   ├── payment.py
│   │   ├── products.py
│   │   └── recommendations.py
│   ├── .env                 # Environment variables (STRIPE keys)
│   ├── config.py
│   ├── database.py
│   └── main.py              # Main FastAPI application
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── AddProduct.js
    │   │   ├── CheckoutPage.js
    │   │   ├── MockCheckoutForm.js
    │   │   ├── Navigation.js
    │   │   ├── ProductCard.js
    │   │   ├── ProductsYouLike.js
    │   │   └── ...
    │   ├── contexts/
    │   │   └── CartContext.js
    │   ├── pages/
    │   │   ├── HomePage.js
    │   │   ├── CartPage.js
    │   │   └── SimilarProductsPage.js
    │   ├── App.js
    │   └── index.js
    └── .env                  # Environment variables (API_BASE)
🚀 Prerequisites
Node.js and npm
Python 3.8+
pip
🛠️ Installation & Setup
1. Clone the Repository
bash

git clone <your-repository-url>
cd <your-repository-name>
2. Backend Setup
Navigate to the backend directory:
bash

cd backend
Create and activate a virtual environment:
bash

python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
Install dependencies:
bash

pip install -r requirements.txt
(If you don't have a requirements.txt, create it and add: fastapi, "uvicorn[standard]", pandas, torch, python-dotenv, stripe)
Create environment variables:
Create a file named .env in the backend directory and add your configuration:

STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
Run the FastAPI server:
bash

uvicorn main:app --reload
The API will be available at http://localhost:8000.
3. Frontend Setup
Navigate to the frontend directory:
bash

cd frontend
Install dependencies:
bash

npm install
Create environment variables:
Create a file named .env in the frontend directory and add:

REACT_APP_API_BASE=http://localhost:8000
Run the React development server:
bash

npm start
The application will open in your browser at http://localhost:3000.
📖 Usage
Browse Products: View random and latest products on the homepage.
Get Recommendations: Use the search bar to find products based on a description.
View Similar Items: Click on any product to see a list of similar items.
Manage Cart: Click "Add to Cart" on any product. View your cart by clicking the "Cart" link in the navigation.
Checkout: Click the "Buy" button on any product to go directly to the mock checkout page. Fill out the form and complete the purchase.
Add a Product: Use the "Add Product" link in the navigation to access the form for adding new items to the catalog.
🔗 API Endpoints
Here are some of the key API endpoints available:

Method
Endpoint
Description
GET	/latest	Fetches the latest products.
GET	/products/random?n=12	Fetches a list of random products.
GET	/products/{id}	Fetches a single product by its ID.
POST	/cart/add	Adds a product to the shopping cart.
GET	/cart	Retrieves the current shopping cart.
POST	/recommend	Gets recommendations based on a query.
GET	/products/similar/{id}	Gets products similar to a given ID.

🚀 Future Enhancements
Real Payment Integration: Implement full Stripe payment processing with webhooks.
User Authentication: Add user accounts and order history.
Admin Dashboard: Create a comprehensive admin panel for managing products and orders.
Database Integration: Replace CSV files with a persistent database like PostgreSQL or MongoDB.
Review and Rating System: Allow users to review and rate products.
