// src/pages/CartPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import Cart from '../components/Cart'; // Import the existing Cart component

const CartPage = () => {
    return (
        <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
            <div style={{ marginBottom: "20px" }}>
                {/* Link to go back to the home page */}
                <Link to="/" style={{ color: '#2196F3', textDecoration: 'none', fontWeight: 'bold' }}>
                    &larr; Back to Shopping
                </Link>
            </div>
            <h1 style={{ color: '#333' }}>Your Shopping Cart</h1>
            {/* The existing Cart component does all the work */}
            <Cart />
        </div>
    );
};

export default CartPage;