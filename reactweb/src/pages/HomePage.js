// src/pages/HomePage.js
import React, { useState } from "react";
import { useCart } from '../contexts/CartContext'; // Import the hook
import { Link } from 'react-router-dom'; // FIX 1: Import the Link component
import Cart from '../components/Cart'; // We still need the Cart component for the inline view
import SearchRecommendations from '../components/SearchRecommendations';
import LatestProducts from '../components/LatestProducts';
import ImageViewer from '../components/ImageViewer';
import AdminActions from '../components/AdminActions';
// FIX 2: Correct the import path for AddProduct. It's in the 'components' folder.
import AddProduct from '../components/AddProduct'; 
import ProductsYouLike from '../components/ProductsYouLike'; // NEW IMPORT

const HomePage = () => {
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
        <div style={{ fontFamily: 'Arial, sans-serif' }}>
            {/* The main content of your home page */}
            <main>
                {showAddProduct && <AddProduct API_BASE={API_BASE} />}
                
                <SearchRecommendations API_BASE={API_BASE} />
                <ProductsYouLike API_BASE={API_BASE} />
                <LatestProducts API_BASE={API_BASE} onImageSelect={handleImageSelect} />
                
                {/* This is a smaller, inline view of the cart */}
                <div style={{ marginBottom: "30px", backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #ddd' }}>
                    <h3 style={{ color: '#333' }}>Cart Summary</h3>
                    {/* <Cart />  */}
                    <div style={{ textAlign: 'center', marginTop: '15px' }}>
                        {/* The Link component now works because we imported it */}
                        <Link to="/cart" style={{ textDecoration: 'none' }}>
                            <button style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                                View Full Cart
                            </button>
                        </Link>
                    </div>
                </div>
                
                <ImageViewer imageUrl={imageUrl} onClose={handleCloseViewer} />
                <AdminActions API_BASE={API_BASE} />
            </main>
        </div>
    );
};

export default HomePage;