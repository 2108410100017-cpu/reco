// src/pages/HomePage.js
import React, { useState } from "react";
import { useCart } from '../contexts/CartContext';
import { Link } from 'react-router-dom';
import SearchRecommendations from '../components/SearchRecommendations';
import LatestProducts from '../components/LatestProducts';
import ImageViewer from '../components/ImageViewer';
import AdminActions from '../components/AdminActions';
import AddProduct from '../components/AddProduct';
import ProductsYouLike from '../components/ProductsYouLike';

const HomePage = () => {
    // Removed unused getItemCount
    useCart();

    const API_BASE = "https://reco-3-4mat.onrender.com";
    // const API_BASE = "http://localhost:8000";


    const [imageUrl, setImageUrl] = useState(null);
    const [showAddProduct] = useState(false); // Removed setter

    const handleImageSelect = (pid) => {
        setImageUrl(`${API_BASE}/image/${pid}.jpg`);
    };

    const handleCloseViewer = () => {
        setImageUrl(null);
    };

    return (
        <div style={{ fontFamily: 'Arial, sans-serif' }}>
            <main>
                {showAddProduct && <AddProduct API_BASE={API_BASE} />}
                
                <SearchRecommendations API_BASE={API_BASE} />
                <ProductsYouLike API_BASE={API_BASE} />
                <LatestProducts API_BASE={API_BASE} onImageSelect={handleImageSelect} />
                
                <div style={{ 
                    marginBottom: "30px",
                    backgroundColor: '#fff',
                    padding: '20px',
                    borderRadius: '8px',
                    border: '1px solid #ddd'
                }}>
                    <h3 style={{ color: '#333' }}>Cart Summary</h3>
                    
                    <div style={{ textAlign: 'center', marginTop: '15px' }}>
                        <Link to="/cart" style={{ textDecoration: 'none' }}>
                            <button style={{
                                padding: '10px 20px',
                                backgroundColor: '#4CAF50',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}>
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