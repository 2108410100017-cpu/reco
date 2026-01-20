// src/components/SearchRecommendations.js

import React, { useState } from "react";
import axios from "axios";
import { useCart } from '../contexts/CartContext'; // 1. Import is correct, it stays here at the top.

// WRONG: This is where the error is. Calling the hook outside the function.
// const { addToCart } = useCart(); 

function SearchRecommendations({ API_BASE }) {
    // CORRECT: The hook MUST be called inside the function, like this.
    const { addToCart } = useCart(); 

    const [recommendInput, setRecommendInput] = useState("");
    const [recommendResult, setRecommendResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleRecommend = async () => {
        if (!recommendInput.trim()) return;
        
        setIsLoading(true);
        try {
            const response = await axios.post(`${API_BASE}/recommend`, {
                query: recommendInput,
                top_k: 10
            });
            setRecommendResult(response.data);
        } catch (err) {
            console.error(err);
            setRecommendResult("Error in recommendation");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
            <h2 style={{ color: '#555' }}>Search for Recommendations</h2>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
                <input
                    type="text"
                    placeholder="Enter your query (e.g., 'red dress')"
                    value={recommendInput}
                    onChange={(e) => setRecommendInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleRecommend()}
                    style={{ 
                        flex: 1, 
                        padding: '10px', 
                        border: '1px solid #ddd', 
                        borderRadius: '4px',
                        fontSize: '16px'
                    }}
                />
                <button 
                    onClick={handleRecommend} 
                    disabled={isLoading}
                    style={{ 
                        padding: '10px 20px', 
                        backgroundColor: isLoading ? '#ccc' : '#4CAF50', 
                        color: 'white', 
                        border: 'none', 
                        borderRadius: '4px',
                        cursor: isLoading ? 'not-allowed' : 'pointer',
                        fontSize: '16px'
                    }}
                >
                    {isLoading ? 'Searching...' : 'Get Recommendations'}
                </button>
            </div>
            
            {recommendResult && typeof recommendResult !== 'string' && (
                <div>
                    <h3 style={{ color: '#555', marginTop: '20px' }}>Recommendation Results</h3>
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', 
                        gap: '20px',
                        marginTop: '15px'
                    }}>
                        {recommendResult.map((item, index) => (
                            <div key={index} style={{ 
                                border: '1px solid #ddd', 
                                borderRadius: '8px', 
                                padding: '15px',
                                backgroundColor: 'white',
                                boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                                transition: 'transform 0.2s',
                                display: 'flex',
                                flexDirection: 'column'
                            }}>
                                <img 
                                    src={`${API_BASE}${item.image_url}`} 
                                    alt={item.name} 
                                    style={{ 
                                        width: '100%', 
                                        height: '200px', 
                                        objectFit: 'cover',
                                        borderRadius: '4px',
                                        marginBottom: '10px'
                                    }}
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = 'https://picsum.photos/seed/fallback/200/200.jpg';
                                    }}
                                />
                                <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>{item.name}</h4>
                                <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>ID: {item.id}</p>
                                <p style={{ margin: '5px 0 0 0', fontSize: '14px', color: '#0066cc' }}>
                                    Similarity: {(item.score * 100).toFixed(2)}%
                                </p>
                                <div style={{ marginTop: 'auto', paddingTop: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <p style={{ 
                                        margin: 0, 
                                        fontSize: '18px', 
                                        fontWeight: 'bold', 
                                        color: '#e53935' 
                                    }}>
                                        ${item.price ? item.price.toFixed(2) : '0.00'}
                                    </p>
                                    <button 
                                        onClick={() => addToCart(item)} // The hook is used here
                                        style={{
                                            padding: '6px 12px',
                                            backgroundColor: '#FF9800',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '4px',
                                            cursor: 'pointer'
                                        }}
                                    >
                                        Add to Cart
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            {recommendResult && typeof recommendResult === 'string' && (
                <div style={{ color: 'red', marginTop: '10px' }}>{recommendResult}</div>
            )}
        </div>
    );
}

export default SearchRecommendations;