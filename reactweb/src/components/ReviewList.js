// src/components/ReviewList.js
import React from 'react';
import StarRating from './StarRating';

const ReviewList = ({ reviews }) => {
    if (!reviews || reviews.length === 0) {
        return <p>No reviews yet. Be the first to add one!</p>;
    }

    return (
        <div style={{ marginTop: '20px' }}>
            <h3>Customer Reviews</h3>
            {reviews.map(review => (
                <div key={review.id} style={{ borderBottom: '1px solid #eee', padding: '10px 0' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <strong><StarRating rating={review.rating} /></strong>
                        <span style={{ fontSize: '12px', color: '#888' }}>{review.date}</span>
                    </div>
                    <p style={{ margin: '5px 0 0 0' }}>{review.comment}</p>
                </div>
            ))}
        </div>
    );
};

export default ReviewList;