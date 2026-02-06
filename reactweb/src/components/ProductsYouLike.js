// src/components/ProductsYouLike.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import ProductReviews from "./ProductReviews";

const ProductsYouLike = ({ API_BASE }) => {
    const [randomProducts, setRandomProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [activeReviewProduct, setActiveReviewProduct] = useState(null);

    const { addToCart } = useCart();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRandomProducts = async () => {
            setIsLoading(true);
            try {
                const { data } = await axios.get(
                    `${API_BASE}/products/random?n=12`
                );
                setRandomProducts(data || []);
            } catch (err) {
                console.error("Error fetching random products:", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchRandomProducts();
    }, [API_BASE]);

    const handleBuyNow = (product, e) => {
        e.preventDefault();
        e.stopPropagation();
        navigate(`/checkout/${product.id}`, { state: { product } });
    };

    const toggleReviews = (e, productId) => {
        e.preventDefault();
        e.stopPropagation();
        setActiveReviewProduct(prev =>
            prev === productId ? null : productId
        );
    };

    if (isLoading) {
        return (
            <div style={{ textAlign: "center", padding: "20px" }}>
                Loading recommendations...
            </div>
        );
    }

    return (
        <div style={container}>
            <h2 style={{ color: "#555" }}>Products You Might Like</h2>

            {randomProducts.length === 0 ? (
                <div style={emptyBox}>
                    No products to display.
                </div>
            ) : (
                <div style={grid}>
                    {randomProducts.map((item) => (
                        <div key={item.id} style={card}>
                            
                            {/* Product clickable section */}
                            <Link
                                to={`/similar/${item.id}`}
                                style={{
                                    textDecoration: "none",
                                    color: "inherit",
                                    flexGrow: 1
                                }}
                            >
                                <img
                                    src={`${API_BASE}${item.image_url}`}
                                    alt={item.name}
                                    style={imageStyle}
                                    onError={(e) => {
                                        e.target.src =
                                            `https://picsum.photos/seed/product${item.id}/200/200.jpg`;
                                    }}
                                />

                                <h4>{item.name || `Product ${item.id}`}</h4>
                                <p>ID: {item.id}</p>

                                {item.category && (
                                    <p style={{ fontSize: "12px", color: "#888" }}>
                                        Category: {item.category}
                                    </p>
                                )}
                            </Link>

                            {/* Price + buttons */}
                            <div style={footer}>
                                <p style={priceStyle}>
                                    ${item.price?.toFixed(2) || "0.00"}
                                </p>

                                <div style={btnRow}>
                                    <button
                                        onClick={(e) => {
                                            e.preventDefault();
                                            e.stopPropagation();
                                            addToCart(item);
                                        }}
                                        style={cartBtn}
                                    >
                                        Add Cart
                                    </button>

                                    <button
                                        onClick={(e) =>
                                            handleBuyNow(item, e)
                                        }
                                        style={buyBtn}
                                    >
                                        Buy
                                    </button>

                                    {/* REVIEW BUTTON */}
                                    <button
                                        onClick={(e) =>
                                            toggleReviews(e, item.id)
                                        }
                                        style={reviewBtn}
                                    >
                                        ⭐ Review
                                    </button>
                                </div>
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
};

export default ProductsYouLike;


/* ===== STYLES ===== */

const container = {
    marginBottom: "30px",
    backgroundColor: "#f9f9f9",
    padding: "20px",
    borderRadius: "8px",
};

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
};

const imageStyle = {
    width: "100%",
    height: "200px",
    objectFit: "cover",
    borderRadius: "4px",
    marginBottom: "10px",
};

const footer = {
    marginTop: "auto",
};

const priceStyle = {
    fontSize: "18px",
    fontWeight: "bold",
    color: "#e53935",
};

const btnRow = {
    display: "flex",
    gap: "6px",
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
