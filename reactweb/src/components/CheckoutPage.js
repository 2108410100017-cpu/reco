// src/components/CheckoutPage.js
import React from 'react';
import { useParams } from 'react-router-dom';

// Import the MOCK form
import MockCheckoutForm from './MockCheckoutForm';

export default function CheckoutPage() {
    // We still get the productId from the URL, but we won't use it to fetch data.
    const { productId } = useParams();

    // --- MOCK PRODUCT DATA ---
    // In a real app, this data would come from the backend.
    // For now, we're using a static object to build the UI.
    const mockProduct = {
        id: productId, // Use the ID from the URL for display
        name: `Demo Product ${productId}`,
        price: 99.99,
        image_url: '/images/default.jpg' // Use a default or placeholder image
    };

    return (
        <div style={{ padding: '20px', maxWidth: '500px', margin: '40px auto', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
            <div style={{ marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '20px' }}>
                <h2>Checkout</h2>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    {/* Using a placeholder image from a service */}
                    <img 
                        src={`https://picsum.photos/seed/product${mockProduct.id}/80/80.jpg`} 
                        alt={mockProduct.name} 
                        style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '8px' }} 
                    />
                    <div>
                        <h4 style={{ margin: 0, color: '#333' }}>{mockProduct.name}</h4>
                        <p style={{ margin: '5px 0 0 0', fontSize: '18px', fontWeight: 'bold', color: '#e53935' }}>
                            ${mockProduct.price.toFixed(2)}
                        </p>
                    </div>
                </div>
            </div>
            
            {/* Render the mock form directly */}
            <MockCheckoutForm />
        </div>
    );
}