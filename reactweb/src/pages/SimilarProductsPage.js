// src/pages/SimilarProductsPage.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/ProductCard';

const SimilarProductsPage = () => {
    // Get both productId and depth from the URL parameters
    const { productId, depth: depthParam } = useParams(); 
    const depth = parseInt(depthParam) || 0; // Default to 0 if not provided

    const [recommendations, setRecommendations] = useState([]);
    const [baseProduct, setBaseProduct] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const API_BASE = "http://localhost:8000";
    const MAX_DEPTH = 3; // Prevent infinite loops

    useEffect(() => {
        const fetchSimilarProducts = async () => {
            if (!productId) return;
            
            setIsLoading(true);
            try {
                const response = await axios.get(`${API_BASE}/products/similar/${productId}?top_k=10`);
                setRecommendations(response.data);

                // Get base product details for display
                const productResponse = await axios.get(`${API_BASE}/debug/product/${productId}`);
                setBaseProduct(productResponse.data);

            } catch (error) {
                console.error("Error fetching similar products:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSimilarProducts();
    }, [productId, API_BASE]);

    const showDrillDown = depth < MAX_DEPTH && recommendations.length > 0;

    return (
        <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
            <div style={{ marginBottom: "20px" }}>
                <Link to="/" style={{ color: '#2196F3', textDecoration: 'none', fontWeight: 'bold' }}>
                    &larr; Back to Shopping
                </Link>
            </div>

            {/* Different UI for base page vs drill-down page */}
            {depth === 0 && baseProduct && (
                <div style={{ textAlign: 'center', marginBottom: "30px", padding: '20px', backgroundColor: '#fff', borderRadius: '8px' }}>
                    <h2>Because you liked this product:</h2>
                    <ProductCard product={baseProduct.product_info} API_BASE={API_BASE} />
                </div>
            )}

            <h1 style={{ textAlign: 'center', color: '#333' }}>
                {depth === 0 ? 'You Might Also Like' : 'More Similar Products'}
            </h1>
            
            {isLoading ? (
                <div style={{ textAlign: 'center', padding: '20px' }}>Loading similar products...</div>
            ) : recommendations.length > 0 ? (
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', 
                    gap: '20px'
                }}>
                    {recommendations.map((item) => (
                        <ProductCard key={item.id} product={item} API_BASE={API_BASE} depth={depth + 1} />
                    ))}
                </div>
            ) : (
                <p style={{ textAlign: 'center', color: '#888' }}>No similar products found.</p>
            )}
        </div>
    );
};

export default SimilarProductsPage;