// src/contexts/CartContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

// Create the context
const CartContext = createContext();

// Create a provider component
export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const API_BASE = "http://localhost:8000";

  // Fetch cart from the backend when the provider mounts
  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/cart`);
      setCartItems(response.data.items);
      setTotalPrice(response.data.total_price);
    } catch (error) {
      console.error("Failed to fetch cart:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const addToCart = async (product) => {
    setIsLoading(true);
    try {
      await axios.post(`${API_BASE}/cart/add`, null, {
        params: { product_id: product.id, quantity: 1 }
      });
      // Refetch the cart to get the updated state
      await fetchCart();
      alert(`${product.name} added to cart!`);
    } catch (error) {
      console.error("Failed to add to cart:", error);
      alert("Error adding product to cart.");
    } finally {
      setIsLoading(false);
    }
  };

  const removeFromCart = async (productId) => {
    setIsLoading(true);
    try {
      await axios.delete(`${API_BASE}/cart/item/${productId}`);
      await fetchCart();
    } catch (error) {
      console.error("Failed to remove from cart:", error);
      alert("Error removing item from cart.");
    } finally {
      setIsLoading(false);
    }
  };

  const clearCart = async () => {
    setIsLoading(true);
    try {
      await axios.post(`${API_BASE}/cart/clear`);
      await fetchCart();
    } catch (error) {
      console.error("Failed to clear cart:", error);
      alert("Error clearing cart.");
    } finally {
      setIsLoading(false);
    }
  };
  
  const getItemCount = () => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cartItems,
      totalPrice,
      isLoading,
      addToCart,
      removeFromCart,
      clearCart,
      getItemCount,
      fetchCart
    }}>
      {children}
    </CartContext.Provider>
  );
};

// Create a custom hook for easy access to the context
export const useCart = () => {
  return useContext(CartContext);
};