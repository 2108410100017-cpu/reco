// src/contexts/CartContext.js
import React, { createContext, useState, useContext, useEffect, useCallback  } from 'react';
import api from "../utils/api";

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  // const API_BASE = "http://localhost:8000";
  const API_BASE = "https://reco-3-4mat.onrender.com";
  

  // ⭐ Get logged user ID (IMPORTANT)
  const getUserId = () => {
    return localStorage.getItem("user_id") || "guest_user";
  };


const fetchCart = useCallback(async () => {
  setIsLoading(true);
  try {
    const response = await api.get(`${API_BASE}/cart/`, {
      headers: {
        "X-User-ID": getUserId()
      }
    });

    setCartItems(response.data.items);
    setTotalPrice(response.data.total_price);

  } catch (error) {
    console.error("Fetch cart error:", error);
  } finally {
    setIsLoading(false);
  }
}, [API_BASE]);

useEffect(() => {
  fetchCart();
}, [fetchCart]);





  const addToCart = async (product) => {
    setIsLoading(true);
    try {
      await api.post(`${API_BASE}/cart/add/`, null, {
        params: {
          product_id: product.id,
          quantity: 1,
           // ⭐ KEY FIX
        },
        headers:{
          "X-User-ID":getUserId()
        }
      });

      await fetchCart();
    } catch (error) {
      console.error("Add cart error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const removeFromCart = async (productId) => {
    setIsLoading(true);
    try {
      await api.delete(`${API_BASE}/cart/item/${productId}`, {
        params: { user_id: getUserId() }
      });

      await fetchCart();
    } catch (error) {
      console.error("Remove cart error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearCart = async () => {
    setIsLoading(true);
    try {
      await api.post(`${API_BASE}/cart/clear/`, null, {
        params: { user_id: getUserId() }
      });

      await fetchCart();
    } catch (error) {
      console.error("Clear cart error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getItemCount = () =>
    cartItems.reduce((count, item) => count + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        totalPrice,
        isLoading,
        addToCart,
        removeFromCart,
        clearCart,
        getItemCount,
        fetchCart
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
