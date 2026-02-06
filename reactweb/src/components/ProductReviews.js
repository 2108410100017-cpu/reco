import React, { useEffect, useState } from "react";
import axios from "axios";

const ProductReviews = ({ productId, API_BASE }) => {
  const [reviews, setReviews] = useState([]);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);

  // Load reviews when product changes
  useEffect(() => {
    fetchReviews();
  }, [productId]);

  const fetchReviews = async () => {
    try {
      const { data } = await axios.get(
        `${API_BASE}/reviews-clean/product/${productId}`
      );
      setReviews(data.reviews || []);
    } catch (err) {
      console.error("Error fetching reviews:", err);
    }
  };

  // Submit review
  const submitReview = async () => {
    if (!comment.trim()) {
      alert("Write a review first");
      return;
    }

    setLoading(true);

    try {
      await axios.post(
        `${API_BASE}/reviews-clean/product/${productId}`,
        {
          product_id: productId,
          rating,
          comment,
        }
      );

      // Reset form
      setComment("");
      setRating(5);

      // Refresh reviews list
      fetchReviews();
    } catch (err) {
      console.error(err);
      alert("Failed to submit review");
    } finally {
      setLoading(false);
    }
  };

  // Calculate average rating
  const avgRating =
    reviews.length > 0
      ? (
          reviews.reduce((sum, r) => sum + r.rating, 0) /
          reviews.length
        ).toFixed(1)
      : null;

  return (
    <div style={box}>
      <h3>Ratings & Reviews</h3>

      {avgRating && (
        <p>
          ⭐ Average Rating: <strong>{avgRating}</strong> / 5
        </p>
      )}

      {/* Review Form */}
      <div style={form}>
        <select
          value={rating}
          onChange={(e) => setRating(Number(e.target.value))}
        >
          {[5, 4, 3, 2, 1].map((r) => (
            <option key={r} value={r}>
              {r} ⭐
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Write your review..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          style={{ flex: 1, padding: "6px" }}
        />

        <button
          onClick={submitReview}
          disabled={loading}
          style={submitBtn}
        >
          {loading ? "Posting..." : "Submit"}
        </button>
      </div>

      {/* Reviews List */}
      <div>
        {reviews.length === 0 ? (
          <p>No reviews yet.</p>
        ) : (
          reviews.map((r) => (
            <div key={r.id} style={reviewItem}>
              <strong>{r.rating} ⭐</strong>
              <p>{r.comment}</p>
              <small>{r.date}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ProductReviews;


/* ===== Styles ===== */

const box = {
  borderTop: "1px solid #ddd",
  marginTop: "20px",
  paddingTop: "10px",
};

const form = {
  display: "flex",
  flexWrap: "wrap",   // prevents button hiding
  gap: "10px",
  marginBottom: "15px",
};

const reviewItem = {
  borderBottom: "1px solid #eee",
  padding: "8px 0",
};

const submitBtn = {
  backgroundColor: "#4CAF50",
  color: "white",
  border: "none",
  padding: "8px 14px",
  borderRadius: "4px",
  cursor: "pointer",
  fontWeight: "bold",
};
