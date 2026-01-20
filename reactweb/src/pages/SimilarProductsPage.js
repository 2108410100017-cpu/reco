// src/pages/SimilarProductsPage.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/ProductCard'; // We'll create this reusable component next

const SimilarProductsPage = () => {
    const { productId } = useParams(); // Gets the ID from the URL
    const [recommendations, setRecommendations] = useState([]);
    const [baseProduct, setBaseProduct] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const API_BASE = "http://localhost:8000";

    useEffect(() => {
        const fetchSimilarProducts = async () => {
            if (!productId) return;
            
            setIsLoading(true);
            try {
                // First, get the recommendations for the product
                const response = await axios.post(`${API_BASE}/recommend`, {
                    query: productId, // Using the ID as a query is a simple way to find similar items
                    top_k: 10
                });
                setRecommendations(response.data);

                // Second, get the details of the base product to display
                const productResponse = await axios.get(`${API_BASE}/debug/product/${productId}`);
                setBaseProduct(productResponse.data);

            } catch (error) {
                console.error("Error fetching similar products:", error);
                // Handle error state
            } finally {
                setIsLoading(false);
            }
        };

        fetchSimilarProducts();
    }, [productId, API_BASE]);

    if (isLoading) {
        return <div style={{ padding: "20px", textAlign: "center" }}>Loading similar products...</div>;
    }

    return (
        <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
            <div style={{ marginBottom: "20px" }}>
                <Link to="/" style={{ color: '#2196F3', textDecoration: 'none', fontWeight: 'bold' }}>
                    &larr; Back to Shopping
                </Link>
            </div>

            {baseProduct && (
                <div style={{ textAlign: 'center', marginBottom: '30px', padding: '20px', backgroundColor: '#fff', borderRadius: '8px' }}>
                    <h2>Because you liked this product:</h2>
                    <ProductCard product={baseProduct.product_info} API_BASE={API_BASE} />
                </div>
            )}

            <h1 style={{ textAlign: 'center', color: '#333' }}>You Might Also Like</h1>
            
            {recommendations.length > 0 ? (
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', 
                    gap: '20px'
                }}>
                    {recommendations.map((item) => (
                        <ProductCard key={item.id} product={item} API_BASE={API_BASE} />
                    ))}
                </div>
            ) : (
                <p style={{ textAlign: 'center', color: '#888' }}>No similar products found.</p>
            )}
        </div>
    );
};

export default SimilarProductsPage;