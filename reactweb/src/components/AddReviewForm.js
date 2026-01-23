// src/components/AddReviewForm.js
import React, { useState } from 'react';
import axios from 'axios';

const AddReviewForm = ({ API_BASE, productId, onReviewAdded }) => {
    const [rating, setRating] = useState(5);
    const [comment, setComment] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // Send JSON explicitly
            const response = await axios.post(
                `${API_BASE}/reviews-clean/product/${productId}`,
                { rating, comment },  // body
                { headers: { 'Content-Type': 'application/json' } } // <- FIX
            );

            // Reset form
            setComment('');
            setRating(5);
            onReviewAdded(response.data);

        } catch (error) {
            console.error("Failed to submit review:", error);
            alert("Could not submit review. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form 
            onSubmit={handleSubmit} 
            style={{
                marginTop: '20px',
                padding: '15px',
                border: '1px solid #ddd',
                borderRadius: '8px'
            }}
        >
            <h3>Add a Review</h3>

            <div style={{ marginBottom: '10px' }}>
                <label>Rating:</label>
                <select
                    value={rating}
                    onChange={(e) => setRating(Number(e.target.value))}
                    style={{ marginLeft: '10px' }}
                >
                    {[5, 4, 3, 2, 1].map(star => (
                        <option key={star} value={star}>
                            {'★'.repeat(star)}{'☆'.repeat(5 - star)}
                        </option>
                    ))}
                </select>
            </div>

            <div style={{ marginBottom: '10px' }}>
                <label>Comment:</label>
                <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    required
                    rows={3}
                    style={{ width: '100%', marginTop: '5px' }}
                />
            </div>

            <button
                type="submit"
                disabled={isLoading}
                style={{
                    padding: '8px 15px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px'
                }}
            >
                {isLoading ? 'Submitting...' : 'Submit Review'}
            </button>
        </form>
    );
};

export default AddReviewForm;
