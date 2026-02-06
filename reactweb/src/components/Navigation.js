// src/components/Navigation.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';

const Navigation = () => {
    const { cartItems } = useCart();
    const navigate = useNavigate();

    // ⭐ Get logged user
    const userId = localStorage.getItem("user_id") || "Guest";

    const handleLogout = () => {
        localStorage.clear();
        navigate("/login");
    };

    return (
        <nav style={navStyle}>
            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                <Link to="/" style={logoStyle}>
                    MyStore
                </Link>

                <Link to="/add-product" style={linkStyle}>
                    Add Product
                </Link>
            </div>

            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                
                {/* ⭐ Always show username */}
                <span style={{ fontWeight: 'bold' }}>
                    👤 {userId}
                </span>

                {/* ⭐ Logout button only if logged in */}
                {userId !== "Guest" && (
                    <button onClick={handleLogout} style={logoutBtn}>
                        Logout
                    </button>
                )}

                <Link to="/cart" style={linkStyle}>
                    Cart ({cartItems?.length || 0})
                </Link>
            </div>
        </nav>
    );
};

export default Navigation;


/* ===== Styles ===== */

const navStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundColor: '#333',
    color: 'white'
};

const logoStyle = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '18px',
    fontWeight: 'bold'
};

const linkStyle = {
    color: 'white',
    textDecoration: 'none'
};

const logoutBtn = {
    padding: '6px 12px',
    backgroundColor: '#e53935',
    border: 'none',
    borderRadius: '4px',
    color: 'white',
    cursor: 'pointer'
};
