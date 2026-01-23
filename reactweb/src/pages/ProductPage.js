import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ProductCard from "../components/ProductCard";
import ReviewList from "../components/ReviewList";
import AddReviewForm from "../components/AddReviewForm";

const ProductPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [recommended, setRecommended] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      let p = await api.get(`/product/${id}`);
      let r = await api.get(`/recommend/${id}`);
      let rv = await api.get(`/reviews/${id}`);

      setProduct(p.data);
      setRecommended(r.data);
      setReviews(rv.data);
    } catch (err) {
      console.error("Frontend Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  if (loading) return <h3>Loading...</h3>;

  return (
    <div style={{ padding: 20 }}>
      <h2>Product Details</h2>
      <ProductCard product={product} />

      <h3 style={{ marginTop: 30 }}>Recommended Products</h3>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
        {recommended.map((rec) => (
          <ProductCard key={rec.id} product={rec} />
        ))}
      </div>

      <h3 style={{ marginTop: 30 }}>User Reviews</h3>
      <ReviewList reviews={reviews} />

      <AddReviewForm productId={id} onSuccess={fetchData} />
    </div>
  );
};

export default ProductPage;
