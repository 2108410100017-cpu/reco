// src/pages/TestAnalyticsPage.js
import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = "http://localhost:8000";

const TestAnalyticsPage = () => {
    const [eventType, setEventType] = useState('product_view');
    const [productId, setProductId] = useState('12345');
    const [userId, setUserId] = useState('user-abc');
    const [response, setResponse] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setResponse(null);

        const payload = {
            event_type: eventType,
            product_id: parseInt(productId),
            user_id: userId,
            metadata: { source: 'test_page' }
        };

        try {
            const res = await axios.post(`${API_BASE}/analytics/track`, payload);
            setResponse(res.data);
        } catch (error) {
            setResponse({ status: 'error', detail: error.message });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6', borderRadius: '8px' }}>
            <h2>Analytics Test Page</h2>
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
                <div style={{ marginBottom: '15px' }}>
                    <label>
                        Event Type:
                        <select value={eventType} onChange={(e) => setEventType(e.target.value)} style={{ marginLeft: '10px', padding: '5px', border: '1px solid #ccc', borderRadius: '4px' }}>
                            <option value="product_view">Product View</option>
                            <option value="add_to_cart">Add to Cart</option>
                            <option value="purchase_initiated">Purchase Initiated</option>
                        </select>
                    </label>
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label>
                        Product ID:
                        <input
                            type="number"
                            value={productId}
                            onChange={(e) => setProductId(e.target.value)}
                            style={{ marginLeft: '10px', padding: 'page', border: '1px solid #ccc', borderRadius: '4px', width: '100px' }}
                        />
                    </label>
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label>
                        User ID:
                        <input
                            type="text"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            style={{ marginLeft: '10px', padding: '5px', border: '1px solid #css', borderRadius: '4px', width: '100%' }}
                        />
                    </label>
                </div>
                <button type="submit" disabled={isLoading} style={{ padding: '10px 20px', backgroundColor: isLoading ? '#ccc' : '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: isLoading ? 'not-allowed' : 'pointer' }}>
                    {isLoading ? 'Submitting...' : 'Track Event'}
                </button>
            </form>

            {response && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#e8f5e8', border: '1px solid #ddd', borderRadius: '4px' }}>
                    <h4>Server Response:</h4>
                    <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', overflowX: 'auto' }}>
                        {JSON.stringify(response, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
};

export default TestAnalyticsPage;