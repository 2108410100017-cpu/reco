// src/components/CheckoutForm.js
import React, { useState } from 'react';
import { PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';

export default function CheckoutForm() {
    const stripe = useStripe();
    const elements = useElements();
    const [message, setMessage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!stripe || !elements) return;

        setIsLoading(true);
        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                // This is the URL the user will be redirected to after payment
                return_url: `${window.location.origin}/success`,
            },
        });

        if (error.type === "card_error" || error.type === "validation_error") {
            setMessage(error.message);
        } else {
            setMessage("An unexpected error occurred.");
        }
        setIsLoading(false);
    };

    return (
        <form id="payment-form" onSubmit={handleSubmit}>
            <PaymentElement id="payment-element" />
            <button disabled={isLoading || !stripe || !elements} id="submit" style={{ marginTop: '20px', width: '100%', padding: '12px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', fontSize: '16px', cursor: 'pointer', opacity: (isLoading || !stripe || !elements) ? 0.6 : 1 }}>
                <span id="button-text">{isLoading ? "Processing..." : "Pay now"}</span>
            </button>
            {message && <div id="payment-message" style={{ marginTop: '15px', color: '#c62828', textAlign: 'center' }}>{message}</div>}
        </form>
    );
}