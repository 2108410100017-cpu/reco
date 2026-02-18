// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './contexts/CartContext';

// Pages
import HomePage from './pages/HomePage';
import CartPage from './pages/CartPage';
import SimilarProductsPage from './pages/SimilarProductsPage';
import LoginPage from "./pages/LoginPage";

// Components / Pages
import CheckoutPage from './components/CheckoutPage';
import SuccessPage from './components/SuccessPage';
import AddProduct from './components/AddProduct';
import Navigation from './components/Navigation';

function App() {
  const API_BASE =
    // process.env.REACT_APP_API_BASE || "http://localhost:8000";
    process.env.REACT_APP_API_BASE || "https://reco-1-j47k.onrender.com";
    

  return (
    <CartProvider>
      <Router>
        <Navigation />

        <main style={{ padding: "20px" }}>
          <Routes>

            {/* Home */}
            <Route
              path="/"
              element={<HomePage API_BASE={API_BASE} />}
            />

            {/* Cart */}
            <Route
              path="/cart"
              element={<CartPage API_BASE={API_BASE} />}
            />

            {/* Similar Products (FIXED ROUTE) */}
            <Route
              path="/similar/:productId/:depth?"
              element={<SimilarProductsPage API_BASE={API_BASE} />}
            />

            {/* Checkout */}
            <Route
              path="/checkout/:productId"
              element={<CheckoutPage API_BASE={API_BASE} />}
            />

            {/* Success */}
            <Route path="/success" element={<SuccessPage />} />

            {/* Add Product */}
            <Route
              path="/add-product"
              element={<AddProduct API_BASE={API_BASE} />}
            />
            {/*Login*/}
            <Route path="/login" element={<LoginPage />} />

          </Routes>
        </main>
      </Router>
    </CartProvider>
  );
}

export default App;
