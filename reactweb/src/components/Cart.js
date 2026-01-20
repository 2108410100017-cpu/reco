// src/components/Cart.js
import React from 'react';
import { useCart } from '../contexts/CartContext';

const Cart = () => {
  const { cartItems, totalPrice, removeFromCart, clearCart, isLoading } = useCart();

  if (isLoading) {
    return <div>Loading cart...</div>;
  }

  return (
    <div style={{ marginBottom: "30px", backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #ddd' }}>
      <h2 style={{ color: '#333', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>Shopping Cart</h2>
      
      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          {cartItems.map((item) => (
            <div key={item.product_id} style={{ display: 'flex', alignItems: 'center', marginBottom: '15px', borderBottom: '1px solid #f0f0f0', paddingBottom: '15px' }}>
              <img src={`${item.image_url}`} alt={item.name} style={{ width: '60px', height: '60px', objectFit: 'cover', borderRadius: '4px', marginRight: '15px' }} />
              <div style={{ flex: 1 }}>
                <h4 style={{ margin: '0 0 5px 0' }}>{item.name}</h4>
                <p style={{ margin: 0, color: '#666' }}>Price: ${item.price.toFixed(2)} x {item.quantity}</p>
              </div>
              <button 
                onClick={() => removeFromCart(item.product_id)}
                style={{
                  padding: '5px 10px',
                  backgroundColor: '#e53935',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Remove
              </button>
            </div>
          ))}
          
          <div style={{ textAlign: 'right', marginTop: '20px' }}>
            <h3>Total: ${totalPrice.toFixed(2)}</h3>
            <button 
              onClick={clearCart}
              style={{
                padding: '10px 15px',
                backgroundColor: '#9E9E9E',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                marginRight: '10px'
              }}
            >
              Clear Cart
            </button>
            <button 
              style={{
                padding: '10px 20px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Proceed to Checkout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;