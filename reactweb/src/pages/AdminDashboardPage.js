// src/pages/AdminDashboardPage.js
import React, { useState } from 'react'; // <-- REMOVED useEffect
// import axios from 'axios'; // <-- REMOVED axios

import ProductManagement from '../components/ProductManagement';
import ReviewManagement from '../components/ReviewManagement';

const AdminDashboardPage = ({ API_BASE }) => {
    const [activeTab, setActiveTab] = useState('products');
    const [adminKey, setAdminKey] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleLogin = (e) => {
        e.preventDefault();
        if (adminKey === 'super-secret-key-123') {
            setIsAuthenticated(true);
        } else {
            alert('Invalid Admin Key');
        }
    };

    if (!isAuthenticated) {
        return (
            <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
                <h2>Admin Login</h2>
                <form onSubmit={handleLogin}>
                    <input
                        type="password"
                        placeholder="Enter Admin Key"
                        value={adminKey}
                        onChange={(e) => setAdminKey(e.target.value)}
                        style={{ width: '100%', padding: '10px', marginBottom: '10px', boxSizing: 'border-box' }}
                    />
                    <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
                        Login
                    </button>
                </form>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px' }}>
            <h1>Admin Dashboard</h1>
            <div style={{ marginBottom: '20px' }}>
                <button onClick={() => setActiveTab('products')} style={{ marginRight: '10px', padding: '10px', border: activeTab === 'products' ? '1px solid #007bff' : '1px solid #ccc', background: activeTab === 'products' ? '#e9f5ff' : '#f9f9f9' }}>
                    Manage Products
                </button>
                <button onClick={() => setActiveTab('reviews')} style={{ padding: '10px', border: activeTab === 'reviews' ? '1px solid #007bff' : '1px solid #ccc', background: activeTab === 'reviews' ? '#e9f5ff' : '#f9f9f9' }}>
                    Manage Reviews
                </button>
            </div>

            {activeTab === 'products' && <ProductManagement API_BASE={API_BASE} />}
            {activeTab === 'reviews' && <ReviewManagement API_BASE={API_BASE} />}
        </div>
    );
};

export default AdminDashboardPage;