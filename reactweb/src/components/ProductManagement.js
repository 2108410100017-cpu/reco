// src/components/ProductManagement.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductManagement = ({ API_BASE }) => {
    const [products, setProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                // The admin key is sent in the headers
                const response = await axios.get(`${API_BASE}/admin/products`, {
                    headers: { 'x-admin-key': 'super-secret-key-123' }
                });
                setProducts(response.data);
            } catch (error) {
                console.error("Failed to fetch products:", error);
                alert("Failed to fetch products. Check console for details.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchProducts();
    }, [API_BASE]);

    const handleDelete = async (productId) => {
        if (!window.confirm('Are you sure you want to delete this product?')) return;

        try {
            await axios.delete(`${API_BASE}/admin/products/${productId}`, {
                headers: { 'x-admin-key': 'super-secret-key-123' }
            });
            setProducts(products.filter(p => p.id !== productId));
            alert('Product deleted successfully!');
        } catch (error) {
            console.error("Failed to delete product:", error);
            alert("Failed to delete product.");
        }
    };

    if (isLoading) return <p>Loading products...</p>;

    return (
        <div>
            <h2>Product Management</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ background: '#f2f2f2' }}>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>ID</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Name</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Price</th>
                        <th style={{ padding: '10px', border: '1px solid #ddd' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map(product => (
                        <tr key={product.id}>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{product.id}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>{product.name}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>${product.price}</td>
                            <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                                <button onClick={() => handleDelete(product.id)} style={{ color: 'red', background: 'none', border: '1px solid red', cursor: 'pointer' }}>
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

export default ProductManagement;