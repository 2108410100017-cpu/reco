// src/components/MockCheckoutForm.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function MockCheckoutForm() {
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Basic client-side validation
        const cardNumber = event.target.cardNumber.value;
        if (!cardNumber) {
            alert("Please enter a card number.");
            return;
        }

        setIsLoading(true);

        // Simulate a network delay for payment processing
        await new Promise(resolve => setTimeout(resolve, 2000)); // 2-second delay

        // Simulate a successful payment
        console.log("Mock payment successful!");
        navigate('/success');
    };

    return (
        <form id="payment-form" onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
                <label htmlFor="cardNumber" style={{ display: 'block', marginBottom: '5px', fontSize: '14px', color: '#555' }}>
                    Card Information
                </label>
                <input
                    id="cardNumber"
                    name="cardNumber"
                    type="text"
                    placeholder="1234 1234 1234 1234"
                    style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        fontSize: '16px',
                        boxSizing: 'border-box'
                    }}
                />
                <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                    <input
                        type="text"
                        placeholder="MM / YY"
                        style={{
                            flex: '1',
                            padding: '10px',
                            border: '1px solid #ccc',
                            borderRadius: '4px',
                            fontSize: '16px'
                        }}
                    />
                    <input
                        type="text"
                        placeholder="CVC"
                        maxLength={4}
                        style={{
                            width: '80px',
                            padding: '10px',
                            border: '1px solid #ccc',
                            borderRadius: '4px',
                            fontSize: '16px'
                        }}
                    />
                </div>
            </div>

            <div style={{ marginBottom: '15px' }}>
                <label htmlFor="email" style={{ display: 'block', marginBottom: '5px', fontSize: '14px', color: '#555' }}>
                    Email Address
                </label>
                <input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    required
                    style={{
                        width: '100%',
                        padding: '10px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        fontSize: '16px',
                        boxSizing: 'border-box'
                    }}
                />
            </div>

            <button
                disabled={isLoading}
                type="submit"
                style={{
                    width: '100%',
                    padding: '12px',
                    backgroundColor: isLoading ? '#cccccc' : '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '16px',
                    fontWeight: 'bold',
                    cursor: isLoading ? 'not-allowed' : 'pointer'
                }}
            >
                {isLoading ? "Processing..." : "Pay now"}
            </button>
        </form>
    );
}