// src/components/ProductCard.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import { useCart } from '../contexts/CartContext'; // Import useCart

const ProductCard = ({ product, API_BASE, depth = 0 }) => {
    const { addToCart } = useCart(); // Initialize cart hook
    const navigate = useNavigate(); // Initialize navigate hook

    // Function to handle "Buy" button click
    const handleBuyNow = (productToBuy) => {
        navigate(`/checkout/${productToBuy.id}`, { state: { product: productToBuy } });
    };

    // Function to handle "Add to Cart" button click
    const handleAddToCart = (e, productToAdd) => {
        e.preventDefault(); // Stop the Link's navigation
        e.stopPropagation(); // Stop the event from bubbling up
        addToCart(productToAdd);
    };

    // Function to handle "Buy" button click with event stopping
    const handleBuyClick = (e, productToBuy) => {
        e.preventDefault();
        e.stopPropagation();
        handleBuyNow(productToBuy);
    };

    const { id, name, price, image_url } = product;

    return (
        // The main card container is no longer wrapped by the Link
        <div style={{
            border: '1px solid #ddd', borderRadius: '8px', padding: '15px',
            backgroundColor: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
            display: 'flex', flexDirection: 'column',
            transition: 'transform 0.2s, box-shadow 0.2s',
            cursor: 'pointer',
            height: '100%'
        }}
        onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-5px)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(0.0,0,0.15)';
        }}
        onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        }}
        >
            {/* The Link now only wraps the visual content, not the buttons */}
            <Link 
                to={`/similar/${product.id}?depth=${depth + 1}`} 
                style={{ textDecoration: 'none', color: 'inherit', flexGrow: 1 }}
            >
                <img 
                    src={`${API_BASE}${product.image_url}`} 
                    alt={product.name} 
                    style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '4px', marginBottom: '8px' }}
                    onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = 'https://picsum.photos/seed/product' + (product.id) + '/200/200.jpg';
                    }}
                />
                <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>{product.name}</h4>
                <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>ID: {product.id}</p>
                <p style={{ 
                    margin: 'auto 0 10px 0', // Adjusted margin for button space
                    fontSize: '18px', 
                    fontWeight: 'bold', color: '#e53935' 
                }}>
                    ${product.price ? product.price.toFixed(2) : '0.00'}
                </p>
            </Link>

            {/* The buttons are now in their own container, outside the Link */}
            <div style={{ display: 'flex', gap: '8px', marginTop: 'auto' }}>
                <button
                    onClick={(e) => handleAddToCart(e, product)}
                    style={{
                        flex: 1,
                        padding: '8px 12px',
                        backgroundColor: '#FF9800',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: 'bold'
                    }}
                >
                    Add to Cart
                </button>
                <button
                    onClick={(e) => handleBuyClick(e, product)}
                    style={{
                        flex: 1,
                        padding: '8px 12px',
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: 'bold'
                    }}
                >
                    Buy
                </button>
            </div>
        </div>
    );
};

export default ProductCard;