// src/pages/SimilarProductsWrapper.js
import React from 'react';
import { useParams } from 'react-router-dom';
import SimilarProductsPage from './SimilarProductsPage';

const SimilarProductsWrapper = () => {
    const { productId } = useParams();
    return <SimilarProductsPage key={productId} />;
};

export default SimilarProductsWrapper;