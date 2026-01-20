// src/components/Navigation.js
import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import { useCart } from '../contexts/CartContext'; // Import the hook

const Navigation = () => {
    const { getItemCount } = useCart(); // Use the hook to get item count
    const itemCount = getItemCount();

    return (
        <header style={{ textAlign: 'center', marginBottom: '40px', position: 'relative' }}>
            <h1 style={{ color: '#2c3e50', margin: 0 }}>Image Recommendation System</h1>
            <p style={{ color: '#7f8c8d' }}>Discover products powered by AI</p>
            
            {/* This is the cart button that is now a Link */}
            <Link to="/cart" style={{ textDecoration: 'none' }}>
                <div style={{ position: 'absolute', top: '0', right: '20px', background: '#FF9800', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                    {itemCount}
                </div>
            </Link>
        </header>
    );
};

export default Navigation;