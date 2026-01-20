// src/components/ProductCard.js
import React from 'react';
import { Link } from 'react-router-dom'; // Import Link

const ProductCard = ({ product, API_BASE, depth = 0 }) => {
    // The 'product' prop can be from the /recommend endpoint or /debug endpoint
    const { id, name, price, image_url } = product;

    return (
        // Wrap the entire card in a Link component
        <Link 
            to={`/similar/${product.id}?depth=${depth + 1}`} // Navigate to the similar page with an incremented depth
            style={{ textDecoration: 'none', color: 'inherit' }}
        >
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
                margin: 'auto 0 0 0', fontSize: '18px', 
                fontWeight: 'bold', color: '#e53935' 
            }}>
                ${product.price ? product.price.toFixed(2) : '0.00'}
            </p>
        </div>
        </Link>
    );
};

export default ProductCard;