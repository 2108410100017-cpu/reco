// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CartProvider } from './contexts/CartContext';

// Import your page components
import HomePage from './pages/HomePage';
import CartPage from './pages/CartPage';
import SimilarProductsPage from './pages/SimilarProductsPage'; // NEW

// Import the Navigation component
import Navigation from './components/Navigation';

function App() {
  return (
    <CartProvider>
      <Router>
        <div>
          <Navigation />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/similar/:productId" element={<SimilarProductsPage />} /> {/* NEW */}
          </Routes>
        </div>
      </Router>
    </CartProvider>
  );
}

export default App;