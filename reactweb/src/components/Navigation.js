// src/components/Navigation.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext'; // Assuming you have a cart context

const Navigation = () => {
    const { cartItems } = useCart(); // Example: to show cart item count

    return (
        <nav style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            padding: '10px 20px', 
            backgroundColor: '#333', 
            color: 'white' 
        }}>
            <div style={{ display: 'flex', gap: '20px' }}>
                <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '18px' }}>
                    MyStore
                </Link>
                {/* --- NEW NAVIGATION LINK --- */}
                <Link to="/add-product" style={{ color: 'white', textDecoration: 'none' }}>
                    Add Product
                </Link>
            </div>
            <div style={{ display: 'flex', gap: '20px' }}>
                <Link to="/cart" style={{ color: 'white', textDecoration: 'none' }}>
                    Cart ({cartItems?.length || 0})
                </Link>
            </div>
        </nav>
    );
};

export default Navigation;