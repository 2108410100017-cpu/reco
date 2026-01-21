// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './contexts/CartContext';

// Import your page components
import HomePage from './pages/HomePage';
import CartPage from './pages/CartPage';
import SimilarProductsPage from './pages/SimilarProductsPage';
import CheckoutPage from './components/CheckoutPage'; // We import the PAGE, not the form
import SuccessPage from './components/SuccessPage';
import AddProduct from './components/AddProduct';

// Import the Navigation component
import Navigation from './components/Navigation';

// --- STRIPE IMPORTS AND INITIALIZATION ARE REMOVED ---

function App() {
  // Define the API_BASE here so you can use it for any route that needs it
  const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

  return (
    // --- THE <Elements> PROVIDER WRAPPER IS REMOVED ---
    <CartProvider>
      <Router>
        <div>
          <Navigation />
          <main style={{ padding: '20px' }}>
            <Routes>
              <Route path="/" element={<HomePage API_BASE={API_BASE} />} />
              <Route path="/cart" element={<CartPage API_BASE={API_BASE} />} />
              <Route path="/similar/:productId" element={<SimilarProductsPage API_BASE={API_BASE} />} />
              
              {/* This route renders the CheckoutPage, which internally uses MockCheckoutForm */}
              <Route path="/checkout/:productId" element={<CheckoutPage API_BASE={API_BASE} />} />
              
              <Route path="/success" element={<SuccessPage />} />
              <Route path="/add-product" element={<AddProduct API_BASE={API_BASE} />} />
            </Routes>
          </main>
        </div>
      </Router>
    </CartProvider>
  );
}

export default App;