// src/components/ProductCard.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import ProductReviews from "./ProductReviews";

const ProductCard = ({ product, API_BASE, depth = 0 }) => {
    const { addToCart } = useCart();
    const navigate = useNavigate();
    const [showReviews, setShowReviews] = useState(false);

    // ⭐ CRITICAL FIX: Prevent crash if product undefined
    if (!product || !product.id) {
        return null;
    }

    const handleBuyNow = (productToBuy) => {
        navigate(`/checkout/${productToBuy.id}`, { state: { product: productToBuy } });
    };

    const handleAddToCart = (e, productToAdd) => {
        e.preventDefault();
        e.stopPropagation();
        addToCart(productToAdd);
    };

    const handleBuyClick = (e, productToBuy) => {
        e.preventDefault();
        e.stopPropagation();
        handleBuyNow(productToBuy);
    };

    const toggleReviews = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setShowReviews(!showReviews);
    };

    return (
        <div style={cardStyle}>
            <Link
                to={`/similar/${product.id}?depth=${depth + 1}`}
                style={{ textDecoration: 'none', color: 'inherit', flexGrow: 1 }}
            >
                <img
                    src={`${API_BASE}${product.image_url}`}
                    alt={product.name || "Product"}
                    style={imageStyle}
                    onError={(e) => {
                        e.target.src = `https://picsum.photos/seed/${product.id}/200/200`;
                    }}
                />

                <h4>{product.name || "Unnamed Product"}</h4>
                <p>ID: {product.id}</p>

                <p style={priceStyle}>
                    ${product.price?.toFixed(2) || "0.00"}
                </p>
            </Link>

            {/* Buttons */}
            <div style={buttonRow}>
                <button onClick={(e) => handleAddToCart(e, product)} style={cartBtn}>
                    Add Cart
                </button>

                <button onClick={(e) => handleBuyClick(e, product)} style={buyBtn}>
                    Buy
                </button>

                <button onClick={toggleReviews} style={reviewBtn}>
                    ⭐ Review
                </button>
            </div>

            {/* Reviews */}
            {showReviews && (
                <ProductReviews
                    productId={product.id}
                    API_BASE={API_BASE}
                />
            )}
        </div>
    );
};

export default ProductCard;


/* ===== Styles ===== */

const cardStyle = {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '15px',
    backgroundColor: 'white',
    boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    transition: 'transform 0.2s',
    height: '100%'
};

const imageStyle = {
    width: '100%',
    height: '200px',
    objectFit: 'cover',
    borderRadius: '4px',
    marginBottom: '8px'
};

const priceStyle = {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#e53935'
};

const buttonRow = {
    display: 'flex',
    gap: '6px',
    marginTop: '10px'
};

const cartBtn = {
    flex: 1,
    backgroundColor: '#FF9800',
    color: '#fff',
    border: 'none',
    padding: '8px',
    borderRadius: '4px'
};

const buyBtn = {
    flex: 1,
    backgroundColor: '#4CAF50',
    color: '#fff',
    border: 'none',
    padding: '8px',
    borderRadius: '4px'
};

const reviewBtn = {
    flex: 1,
    backgroundColor: '#673AB7',
    color: '#fff',
    border: 'none',
    padding: '8px',
    borderRadius: '4px'
};
