// src/components/StarRating.js
import React from 'react';

const StarRating = ({ rating }) => {
    return (
        <span style={{ fontSize: '14px', color: '#555' }}>
            {'★'.repeat(Math.round(rating))}{'☆'.repeat(5 - Math.round(rating))}
            <span style={{ fontSize: '12px', color: '#888', marginLeft: '5px' }}>({rating})</span>
        </span>
    );
};

export default StarRating;