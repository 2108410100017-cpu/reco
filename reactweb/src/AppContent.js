// src/AppContent.js
import React, { useState } from "react";
import { useCart } from './contexts/CartContext'; // Import the hook HERE
import Cart from './components/Cart';
import SearchRecommendations from './components/SearchRecommendations';
import LatestProducts from './components/LatestProducts';
import ImageViewer from './components/ImageViewer';
import AdminActions from './components/AdminActions';
import AddProduct from './components/AddProduct';

const AppContent = () => {
    // Call the hook INSIDE this component function.
    // This works because AppContent is a child of CartProvider.
    const { getItemCount } = useCart(); 
    
    const API_BASE = "http://localhost:8000";
    const [imageUrl, setImageUrl] = useState(null);
    const [showAddProduct, setShowAddProduct] = useState(false);

    const handleImageSelect = (pid) => {
        setImageUrl(`${API_BASE}/image/${pid}.jpg`);
    };

    const handleCloseViewer = () => {
        setImageUrl(null);
    };

    return (
        <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
            <header style={{ textAlign: 'center', marginBottom: '40px', position: 'relative' }}>
                <h1 style={{ color: '#2c3e50', margin: 0 }}>Image Recommendation System</h1>
                <p style={{ color: '#7f8c8d' }}>Discover products powered by AI</p>
                <div style={{ position: 'absolute', top: '0', right: '20px', background: '#FF9800', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                    {getItemCount()}
                </div>
                <div style={{ textAlign: 'center', marginTop: '10px' }}>
                    <button
                        onClick={() => setShowAddProduct(!showAddProduct)}
                        style={{
                            padding: '8px 15px',
                            backgroundColor: '#3498db',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        {showAddProduct ? 'Hide' : 'Show'} Product Addition Form
                    </button>
                </div>
            </header>

            <main>
                {showAddProduct && <AddProduct API_BASE={API_BASE} />}
                
                <SearchRecommendations API_BASE={API_BASE} />
                <LatestProducts API_BASE={API_BASE} onImageSelect={handleImageSelect} />
                
                <Cart />
                
                <ImageViewer imageUrl={imageUrl} onClose={handleCloseViewer} />
                <AdminActions API_BASE={API_BASE} />
            </main>

            <footer style={{ textAlign: 'center', marginTop: '40px', padding: '20px', color: '#95a5a6', fontSize: '14px' }}>
                <p>&copy; 2024 Image Recommendation App</p>
            </footer>
        </div>
    );
};

export default AppContent;