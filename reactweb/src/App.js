// src/App.js
import React from 'react';
import { CartProvider } from './contexts/CartContext'; // Import the Provider
import AppContent from './AppContent'; // Import the component that will USE the cart

function App() {
  // Wrap AppContent with the Provider.
  // App.js itself does NOT use the cart.
  return (
    <CartProvider>
      <AppContent />
    </CartProvider>
  );
}

export default App;