// src/components/ProductsYouLike.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';

const ProductsYouLike = ({ API_BASE }) => {
    const [randomProducts, setRandomProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const { addToCart } = useCart();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRandomProducts = async () => {
            const url = `${API_BASE}/products/random?n=12`;
            setIsLoading(true);
            try {
                const response = await axios.get(url);
                setRandomProducts(response.data);
            } catch (err) {
                console.error("ProductsYouLike: Error fetching random products:", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchRandomProducts();
    }, [API_BASE]);

    // CORRECT: This function accepts a 'product' as its argument.
    const handleBuyNow = (product) => {
        navigate(`/checkout/${product.id}`, { state: { product } });
    };

    if (isLoading) {
        return <div style={{ textAlign: 'center', padding: '20px' }}>Loading recommendations...</div>;
    }

    return (
        <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
            <h2 style={{ color: '#555' }}>Products You Might Like</h2>
            
            {randomProducts.length === 0 ? (
                 <div style={{ marginTop: '20px', padding: '20px', textAlign: 'center', color: '#888', fontStyle: 'italic' }}>
                    No products to display.
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '20px', marginTop: '15px' }}>
                    {randomProducts.map((item) => ( // <-- The variable here is 'item'
                        <div key={item.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px', backgroundColor: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.1)', transition: 'transform 0.2s', cursor: 'pointer', display: 'flex', flexDirection: 'column' }}
                        onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-5px)'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; }}
                        >
                            <Link to={`/similar/${item.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                <img src={`${API_BASE}${item.image_url}`} alt={item.name} style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '4px', marginBottom: '10px' }} onError={(e) => { e.target.onerror = null; e.target.src = `https://picsum.photos/seed/product${item.id}/200/200.jpg`; }} />
                                <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>{item.name || `Product ${item.id}`}</h4>
                                <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>ID: {item.id}</p>
                                {item.category && (<p style={{ margin: '5px 0 0 0', fontSize: '12px', color: '#888' }}>Category: {item.category}</p>)}
                            </Link>
                            
                            <div style={{ marginTop: 'auto', paddingTop: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' }}>
                                <p style={{ margin: 0, fontSize: '18px', fontWeight: 'bold', color: '#e53935' }}>${item.price ? item.price.toFixed(2) : '0.00'}</p>
                                <div style={{ display: 'flex', gap: '8px' }}>
                                    <button onClick={(e) => { e.preventDefault(); e.stopPropagation(); addToCart(item); }} style={{ padding: '6px 12px', backgroundColor: '#FF9800', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Add to Cart</button>
                                    
                                    {/* CORRECT: The onClick calls handleBuyNow and passes the 'item' to it */}
                                    <button 
                                        onClick={() => handleBuyNow(item)} 
                                        style={{ padding: '6px 12px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                                    >
                                        Buy
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ProductsYouLike;