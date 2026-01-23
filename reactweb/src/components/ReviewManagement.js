// src/components/ReviewManagement.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ReviewManagement = ({ API_BASE }) => {
    const [reviews, setReviews] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await axios.get(`${API_BASE}/admin/reviews`, {
                    headers: { 'x-admin-key': 'super-secret-key-123' }
                });
                setReviews(response.data);
            } catch (error) {
                console.error("Failed to fetch reviews:", error);
                alert("Failed to fetch reviews. Check console for details.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchReviews();
    }, [API_BASE]);

    const handleDelete = async (reviewId) => {
        if (!window.confirm('Are you sure you want to delete this review?')) return;
        try {
            await axios.delete(`${API_BASE}/admin/reviews/${reviewId}`, {
                headers: { 'x-admin-key': 'super-secret-key-123' }
            });
            setReviews(reviews.filter(r => r.id !== reviewId));
            alert('Review deleted successfully!');
        } catch (error) {
            console.error("Failed to delete review:", error);
            alert("Failed to delete review.");
        }
    };

    if (isLoading) return <p>Loading reviews...</p>;

    return (
        <div>
            <h2>Review Management</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ background: '#f2f2f2' }}>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>ID</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Product ID</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Rating</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Comment</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {reviews.map(review => (
                        <tr key={review.id}>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{review.id}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{review.product_id}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{'★'.repeat(review.rating)}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{review.comment}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                                <button onClick={() => handleDelete(review.id)} style={{ color: 'red', background: 'none', border: '1px solid red', cursor: 'pointer' }}>
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ReviewManagement;