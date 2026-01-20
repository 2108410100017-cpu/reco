// src/components/ProductCard.js
import React from 'react';

const ProductCard = ({ product, API_BASE }) => {
    // The 'product' prop can be from the /recommend endpoint or /debug endpoint
    const { id, name, price, image_url } = product;

    return (
        <div style={{
            border: '1px solid #ddd', 
            borderRadius: '8px', 
            padding: '15px',
            backgroundColor: 'white',
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <img 
                src={`${API_BASE}${image_url}`} 
                alt={name} 
                style={{ 
                    width: '100%', 
                    height: '200px', 
                    objectFit: 'cover',
                    borderRadius: '4px',
                    marginBottom: '10px'
                }}
                onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://picsum.photos/seed/product' + (id) + '/200/200.jpg';
                }}
            />
            <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>{name}</h4>
            <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>ID: {id}</p>
            <p style={{ 
                margin: 'auto 0 0 0', // Pushes price to the bottom
                fontSize: '18px', 
                fontWeight: 'bold', 
                color: '#e53935' 
            }}>
                ${price ? price.toFixed(2) : '0.00'}
            </p>
        </div>
    );
};

export default ProductCard;