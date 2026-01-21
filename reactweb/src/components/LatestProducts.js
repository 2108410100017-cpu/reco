// src/components/LatestProducts.js

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom'; // 1. Import useNavigate
import { useCart } from '../contexts/CartContext';

function LatestProducts({ API_BASE }) {
    const { addToCart } = useCart(); 
    const navigate = useNavigate(); // 2. Initialize navigate

    const [latestData, setLatestData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const fetchLatest = async () => {
        setIsLoading(true);
        try {
            const response = await axios.get(`${API_BASE}/latest`);
            setLatestData(response.data);
        } catch (err) {
            console.error(err);
            alert("Error fetching latest products");
        } finally {
            setIsLoading(false);
        }
    };

    // 3. Create the handleBuyNow function
    const handleBuyNow = (product) => {
        navigate(`/checkout/${product.id}`, { state: { product } });
    };

    return (
        <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
            <h2 style={{ color: '#555' }}>Latest Products</h2>
            <button 
                onClick={fetchLatest}
                disabled={isLoading}
                style={{ 
                    padding: '8px 15px', 
                    backgroundColor: isLoading ? '#ccc' : '#2196F3', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px',
                    cursor: isLoading ? 'not-allowed' : 'pointer'
                }}
            >
                {isLoading ? 'Loading...' : 'Fetch Latest'}
            </button>
            
            {latestData.length > 0 && (
                <div>
                    <h3 style={{ color: '#555', marginTop: '20px' }}>Recent Products</h3>
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', 
                        gap: '20px',
                        marginTop: '15px'
                    }}>
                        {latestData.slice(0, 10).map((item, index) => (
                            <div key={index} style={{ 
                                border: '1px solid #ddd', 
                                borderRadius: '8px', 
                                padding: '15px',
                                backgroundColor: 'white',
                                boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                                transition: 'transform 0.2s',
                                cursor: 'pointer',
                                display: 'flex',
                                flexDirection: 'column'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.transform = 'translateY(-5px)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.transform = 'translateY(0)';
                            }}
                            >
                                <img 
                                    src={`${API_BASE}${item.image_url}`} 
                                    alt={`Product ${item.id}`}
                                    style={{ 
                                        width: '100%', 
                                        height: '200px', 
                                        objectFit: 'cover',
                                        borderRadius: '4px',
                                        marginBottom: '10px'
                                    }}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = 'https://picsum.photos/seed/product' + (item.id) + '/200/200.jpg';
                                    }}
                                />
                                <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>
                                    {item.name || `Product ${item.id}`}
                                </h4>
                                <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>
                                    ID: {item.id}
                                </p>
                                {item.category && (
                                    <p style={{ margin: '5px 0 0 0', fontSize: '12px', color: '#888' }}>
                                        Category: {item.category}
                                    </p>
                                )}
                                <div style={{ marginTop: 'auto', paddingTop: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' }}>
                                    <p style={{ 
                                        margin: 0, 
                                        fontSize: '18px', 
                                        fontWeight: 'bold', 
                                        color: '#e53935' 
                                    }}>
                                        ${item.price ? item.price.toFixed(2) : '0.00'}
                                    </p>
                                    <div style={{ display: 'flex', gap: '8px' }}>
                                        <button 
                                            onClick={() => addToCart(item)}
                                            style={{
                                                padding: '6px 12px',
                                                backgroundColor: '#FF9800',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            Add to Cart
                                        </button>
                                        {/* 4. Add the new "Buy" button */}
                                        <button 
                                            onClick={() => handleBuyNow(item)}
                                            style={{
                                                padding: '6px 12px',
                                                backgroundColor: '#4CAF50',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            Buy
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            {latestData.length === 0 && !isLoading && (
                <div style={{ 
                    marginTop: '20px', 
                    padding: '20px', 
                    textAlign: 'center', 
                    color: '#888',
                    fontStyle: 'italic'
                }}>
                    No products loaded yet. Click "Fetch Latest" to see the most recent products.
                </div>
            )}
        </div>
    );
}

export default LatestProducts;