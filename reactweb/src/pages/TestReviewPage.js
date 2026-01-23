// src/pages/TestReviewPage.js
import React, { useState, useEffect } from 'react';
import AddReviewForm from '../components/AddReviewForm';
import ReviewList from '../components/ReviewList';
import StarRating from '../components/StarRating';

const TestReviewPage = () => {
    const productId = 39386; // Use a fixed product ID for testing
    const [reviews, setReviews] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const API_BASE = "http://localhost:8000";

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                // --- FIX IS HERE ---
                // Use the new, working endpoint: /reviews-clean/product/{id}
                const response = await axios.get(`${API_BASE}/reviews-clean/product/${productId}`);
                setReviews(response.data.reviews || []);
            } catch (error) {
                console.error("Failed to fetch reviews:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchReviews();
    }, [productId, API_BASE]);

    const handleReviewAdded = (newReview) => {
        setReviews(prevReviews => [newReview, ...prevReviews]);
    };

    const averageRating = reviews.length > 0
        ? (reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length).toFixed(1)
        : 0;

    return (
        <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
            <h1>Review System Test Page (Product ID: {productId})</h1>
            
            <div style={{ padding: '20px', backgroundColor: '#fff', borderRadius: '8px', marginTop: '20px' }}>
                <h2>Product Details</h2>
                <p><strong>Average Rating:</strong> <StarRating rating={averageRating} /></p>
            </div>

            <div style={{ padding: '20px', backgroundColor: '#fff', borderRadius: '8px', marginTop: '20px' }}>
                <h2>Customer Reviews</h2>
                <AddReviewForm 
                    API_BASE={API_BASE} 
                    productId={productId} 
                    onReviewAdded={handleReviewAdded} 
                />
                <ReviewList reviews={reviews} />
            </div>
        </div>
    );
};

export default TestReviewPage;