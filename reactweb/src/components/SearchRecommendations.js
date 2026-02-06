// src/components/SearchRecommendations.js

import React, { useState, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import ProductReviews from "./ProductReviews";

function SearchRecommendations({ API_BASE }) {
    const { addToCart } = useCart();
    const navigate = useNavigate();

    const [recommendInput, setRecommendInput] = useState("");
    const [recommendResult, setRecommendResult] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeReviewProduct, setActiveReviewProduct] = useState(null);

    const handleRecommend = useCallback(async () => {
        if (!recommendInput.trim()) return;

        setIsLoading(true);
        setError(null);

        try {
            const { data } = await axios.post(`${API_BASE}/recommend`, {
                query: recommendInput,
                top_k: 10,
            });

            setRecommendResult(data || []);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch recommendations.");
        } finally {
            setIsLoading(false);
        }
    }, [recommendInput, API_BASE]);

    const handleSimilarClick = useCallback(
        (productId) => {
            navigate(`/similar/${productId}/0`);
        },
        [navigate]
    );

    const handleBuyNow = useCallback(
        (product, e) => {
            e.stopPropagation();
            navigate(`/checkout/${product.id}`, { state: { product } });
        },
        [navigate]
    );

    const toggleReviews = (e, productId) => {
        e.stopPropagation();
        setActiveReviewProduct(prev =>
            prev === productId ? null : productId
        );
    };

    return (
        <div style={container}>
            <h2>Search Product Recommendations</h2>

            <div style={searchBar}>
                <input
                    type="text"
                    placeholder="Search e.g. red dress, sneakers..."
                    value={recommendInput}
                    onChange={(e) => setRecommendInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleRecommend()}
                    style={inputStyle}
                />

                <button
                    onClick={handleRecommend}
                    disabled={isLoading}
                    style={buttonStyle(isLoading)}
                >
                    {isLoading ? "Searching..." : "Search"}
                </button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {recommendResult.length > 0 && (
                <div style={grid}>
                    {recommendResult.map((item) => (
                        <div key={item.id} style={card}>
                            
                            {/* Click image for similar products */}
                            <img
                                src={`${API_BASE}${item.image_url}`}
                                alt={item.name}
                                loading="lazy"
                                onClick={() => handleSimilarClick(item.id)}
                                style={imageStyle}
                                onError={(e) => {
                                    e.target.src =
                                        "https://picsum.photos/200/200";
                                }}
                            />

                            <h4>{item.name}</h4>
                            <p>ID: {item.id}</p>

                            <p style={{ color: "#2196F3" }}>
                                Similarity: {(item.score * 100).toFixed(1)}%
                            </p>

                            <h3 style={{ color: "#e53935" }}>
                                ${item.price?.toFixed(2) || "0.00"}
                            </h3>

                            <div style={btnRow}>
                                <button
                                    style={cartBtn}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        addToCart(item);
                                    }}
                                >
                                    Add Cart
                                </button>

                                <button
                                    style={buyBtn}
                                    onClick={(e) => handleBuyNow(item, e)}
                                >
                                    Buy
                                </button>

                                {/* NEW REVIEW BUTTON */}
                                <button
                                    style={reviewBtn}
                                    onClick={(e) => toggleReviews(e, item.id)}
                                >
                                    ⭐ Review
                                </button>
                            </div>

                            {/* Reviews toggle */}
                            {activeReviewProduct === item.id && (
                                <ProductReviews
                                    productId={item.id}
                                    API_BASE={API_BASE}
                                />
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default SearchRecommendations;


/* ================= STYLES ================= */

const container = {
    marginBottom: "30px",
    padding: "20px",
    background: "#f9f9f9",
    borderRadius: "8px",
};

const searchBar = {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
};

const inputStyle = {
    flex: 1,
    padding: "10px",
    fontSize: "16px",
};

const buttonStyle = (loading) => ({
    padding: "10px 20px",
    background: loading ? "#ccc" : "#4CAF50",
    color: "#fff",
    border: "none",
});

const grid = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))",
    gap: "20px",
};

const card = {
    background: "#fff",
    padding: "15px",
    borderRadius: "8px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
};

const imageStyle = {
    width: "100%",
    height: "200px",
    objectFit: "cover",
    borderRadius: "6px",
    cursor: "pointer",
};

const btnRow = {
    display: "flex",
    gap: "6px",
    marginTop: "10px",
};

const cartBtn = {
    background: "#FF9800",
    color: "#fff",
    border: "none",
    padding: "6px 12px",
};

const buyBtn = {
    background: "#4CAF50",
    color: "#fff",
    border: "none",
    padding: "6px 12px",
};

const reviewBtn = {
    background: "#673AB7",
    color: "#fff",
    border: "none",
    padding: "6px 12px",
};
