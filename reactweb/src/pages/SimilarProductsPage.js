// src/pages/SimilarProductsPage.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/ProductCard';

const SimilarProductsPage = () => {
    const { productId, depth: depthParam } = useParams();
    const depth = parseInt(depthParam) || 0;

    const [recommendations, setRecommendations] = useState([]);
    const [baseProduct, setBaseProduct] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const API_BASE = "http://localhost:8000";
    const MAX_DEPTH = 3;

    useEffect(() => {
        const fetchSimilarProducts = async () => {
            if (!productId) return;

            setIsLoading(true);

            try {
                // ⭐ Similar products
                const response = await axios.get(
                    `${API_BASE}/products/similar/${productId}?top_k=10`
                );

                // Defensive filtering
                const cleanResults = (response.data || []).filter(p => p && p.id);
                setRecommendations(cleanResults);

                // ⭐ Instead of debug endpoint, fetch actual product info
                if (cleanResults.length > 0) {
                    setBaseProduct(cleanResults[0]);
                }

            } catch (error) {
                console.error("Error fetching similar products:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSimilarProducts();
    }, [productId]);

    return (
        <div style={{ padding: "20px", backgroundColor: '#f4f7f6' }}>
            <Link to="/" style={{ color: '#2196F3', fontWeight: 'bold' }}>
                ← Back to Shopping
            </Link>

            {/* Base Product */}
            {depth === 0 && baseProduct && (
                <div style={{
                    textAlign: 'center',
                    marginBottom: "30px",
                    padding: '20px',
                    backgroundColor: '#fff',
                    borderRadius: '8px'
                }}>
                    <h2>Because you liked this product:</h2>
                    <ProductCard product={baseProduct} API_BASE={API_BASE} />
                </div>
            )}

            <h1 style={{ textAlign: 'center' }}>
                {depth === 0 ? 'You Might Also Like' : 'More Similar Products'}
            </h1>

            {isLoading ? (
                <p style={{ textAlign: 'center' }}>Loading...</p>
            ) : recommendations.length > 0 ? (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
                    gap: '20px'
                }}>
                    {recommendations.map(item => (
                        <ProductCard
                            key={item.id}
                            product={item}
                            API_BASE={API_BASE}
                            depth={depth + 1}
                        />
                    ))}
                </div>
            ) : (
                <p style={{ textAlign: 'center' }}>No similar products found.</p>
            )}
        </div>
    );
};

export default SimilarProductsPage;
