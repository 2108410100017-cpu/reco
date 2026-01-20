// src/components/ProductsYouLike.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

const ProductsYouLike = ({ API_BASE }) => {
    const [randomProducts, setRandomProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        console.log("ProductsYouLike: useEffect is running.");
        const fetchRandomProducts = async () => {
            const url = `${API_BASE}/products/random?n=12`;
            console.log(`ProductsYouLike: Fetching from URL: ${url}`);
            setIsLoading(true);
            try {
                const response = await axios.get(url);
                console.log("ProductsYouLike: Received API response:", response.data);
                console.log(`ProductsYouLike: Response data type: ${typeof response.data}`);
                console.log(`ProductsYouLike: Response data length: ${response.data.length}`);
                setRandomProducts(response.data);
            } catch (err) {
                console.error("ProductsYouLike: Error fetching random products:", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchRandomProducts();
    }, [API_BASE]);

    console.log(`ProductsYouLike: Rendering. isLoading: ${isLoading}, randomProducts.length: ${randomProducts.length}`);

    if (isLoading) {
        return <div style={{ textAlign: 'center', padding: '20px' }}>Loading recommendations...</div>;
    }

    return (
        <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
            <h2 style={{ color: '#555' }}>Products You Might Like</h2>
            {randomProducts.length === 0 ? (
                 <p>No products to display.</p>
            ) : (
                // ... (the rest of your JSX remains the same)
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', 
                    gap: '15px',
                    marginTop: '15px'
                }}>
                    {randomProducts.map((item) => (
                        <Link 
                            to={`/similar/${item.id}`} 
                            key={item.id} 
                            style={{ textDecoration: 'none', color: 'inherit' }}
                        >
                            <div style={{
                                border: '1px solid #ddd', borderRadius: '8px', padding: '10px',
                                backgroundColor: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                                transition: 'transform 0.2s, box-shadow 0.2s', cursor: 'pointer',
                                height: '100%', display: 'flex', flexDirection: 'column'
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.transform = 'translateY(-5px)';
                                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.transform = 'translateY(0)';
                                e.currentTarget.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                            }}
                        >
                            <img 
                                src={`${API_BASE}${item.image_url}`} 
                                alt={item.name} 
                                style={{ width: '100%', height: '180px', objectFit: 'cover', borderRadius: '4px', marginBottom: '8px' }}
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = 'https://picsum.photos/seed/product' + (item.id) + '/180/180.jpg';
                                }}
                            />
                            <h4 style={{ margin: '0 0 5px 0', fontSize: '14px', color: '#333', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.name}</h4>
                            <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>ID: {item.id}</p>
                            <p style={{ margin: 'auto 0 0 0', fontSize: '16px', fontWeight: 'bold', color: '#e53935' }}>
                                ${item.price ? item.price.toFixed(2) : '0.00'}
                            </p>
                        </div>
                    </Link>
                ))}
            </div>
            )}
        </div>
    );
};

export default ProductsYouLike;