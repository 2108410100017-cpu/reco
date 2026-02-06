// src/components/LatestProducts.js

import React, { useState, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import ProductReviews from "./ProductReviews";

function LatestProducts({ API_BASE }) {
    const { addToCart } = useCart();
    const navigate = useNavigate();

    const [latestData, setLatestData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [activeReviewProduct, setActiveReviewProduct] = useState(null);

    // Fetch latest products
    const fetchLatest = useCallback(async () => {
        setIsLoading(true);
        try {
            const { data } = await axios.get(`${API_BASE}/latest`);
            setLatestData(data || []);
        } catch (err) {
            console.error(err);
            alert("Error fetching latest products");
        } finally {
            setIsLoading(false);
        }
    }, [API_BASE]);

    const handleBuyNow = useCallback((product, e) => {
        e.stopPropagation();
        navigate(`/checkout/${product.id}`, { state: { product } });
    }, [navigate]);

    const handleSimilarClick = useCallback((productId) => {
        navigate(`/similar/${productId}/0`);
    }, [navigate]);

    const toggleReviews = (e, productId) => {
        e.stopPropagation();
        setActiveReviewProduct(prev =>
            prev === productId ? null : productId
        );
    };

    return (
        <div style={container}>
            <h2 style={{ color: "#555" }}>Latest Products</h2>

            <button
                onClick={fetchLatest}
                disabled={isLoading}
                style={buttonStyle(isLoading)}
            >
                {isLoading ? "Loading..." : "Fetch Latest"}
            </button>

            {latestData.length > 0 && (
                <div>
                    <h3 style={{ color: "#555", marginTop: "20px" }}>
                        Recent Products
                    </h3>

                    <div style={grid}>
                        {latestData.slice(0, 10).map((item) => (
                            <div
                                key={item.id}
                                style={card}
                                onClick={() => handleSimilarClick(item.id)}
                            >
                                <img
                                    src={`${API_BASE}${item.image_url}`}
                                    alt={item.name}
                                    loading="lazy"
                                    style={imageStyle}
                                    onError={(e) => {
                                        e.target.src =
                                            `https://picsum.photos/seed/${item.id}/200/200`;
                                    }}
                                />

                                <h4>{item.name || `Product ${item.id}`}</h4>
                                <p>ID: {item.id}</p>

                                {item.category && (
                                    <p style={{ fontSize: "12px", color: "#888" }}>
                                        Category: {item.category}
                                    </p>
                                )}

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

                                {/* Reviews section */}
                                {activeReviewProduct === item.id && (
                                    <ProductReviews
                                        productId={item.id}
                                        API_BASE={API_BASE}
                                    />
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {latestData.length === 0 && !isLoading && (
                <div style={emptyBox}>
                    No products loaded yet. Click "Fetch Latest".
                </div>
            )}
        </div>
    );
}

export default LatestProducts;


/* ===== STYLES ===== */

const container = {
    marginBottom: "30px",
    backgroundColor: "#f9f9f9",
    padding: "20px",
    borderRadius: "8px",
};

const buttonStyle = (loading) => ({
    padding: "8px 15px",
    backgroundColor: loading ? "#ccc" : "#2196F3",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: loading ? "not-allowed" : "pointer",
});

const grid = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
    gap: "20px",
    marginTop: "15px",
};

const card = {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "15px",
    backgroundColor: "white",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    cursor: "pointer",
};

const imageStyle = {
    width: "100%",
    height: "200px",
    objectFit: "cover",
    borderRadius: "4px",
    marginBottom: "10px",
};

const btnRow = {
    display: "flex",
    gap: "8px",
    marginTop: "10px",
};

const cartBtn = {
    padding: "6px 12px",
    backgroundColor: "#FF9800",
    color: "white",
    border: "none",
    borderRadius: "4px",
};

const buyBtn = {
    padding: "6px 12px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
};

const reviewBtn = {
    padding: "6px 12px",
    backgroundColor: "#673AB7",
    color: "white",
    border: "none",
    borderRadius: "4px",
};

const emptyBox = {
    marginTop: "20px",
    padding: "20px",
    textAlign: "center",
    color: "#888",
    fontStyle: "italic",
};
