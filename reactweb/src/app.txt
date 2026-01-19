import React, { useState } from "react";
import axios from "axios";

function App() {
  const [recommendInput, setRecommendInput] = useState("");
  const [recommendResult, setRecommendResult] = useState(null);
  const [latestData, setLatestData] = useState([]);
  const [imageUrl, setImageUrl] = useState("");
  const [healthStatus, setHealthStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const API_BASE = "http://localhost:8000"; // adjust if different

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

  const fetchLatest = async () => {
    try {
      const response = await axios.get(`${API_BASE}/latest`);
      setLatestData(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchImage = (pid) => {
    setImageUrl(`${API_BASE}/image/${pid}`);
  };

  const retrainModel = async () => {
    try {
      const response = await axios.post(`${API_BASE}/retrain`);
      alert("Retrain triggered: " + JSON.stringify(response.data));
    } catch (err) {
      console.error(err);
      alert("Error triggering retrain");
    }
  };

  const checkHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setHealthStatus(response.data.status || "Healthy");
    } catch (err) {
      console.error(err);
      setHealthStatus("Unhealthy");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#333', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>Image Recommendation System</h1>

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
              gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', 
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
                  ':hover': {
                    transform: 'translateY(-5px)'
                  }
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
                </div>
              ))}
            </div>
          </div>
        )}
        
        {recommendResult && typeof recommendResult === 'string' && (
          <div style={{ color: 'red', marginTop: '10px' }}>{recommendResult}</div>
        )}
      </div>

      <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
        <h2 style={{ color: '#555' }}>Latest Data</h2>
        <button 
          onClick={fetchLatest}
          style={{ 
            padding: '8px 15px', 
            backgroundColor: '#2196F3', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Fetch Latest
        </button>
        
        {latestData.length > 0 && (
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', 
            gap: '20px',
            marginTop: '15px'
          }}>
            {latestData.slice(0, 10).map((item, index) => (
              <div key={index} style={{ 
                border: '1px solid #ddd', 
                borderRadius: '8px', 
                padding: '15px',
                backgroundColor: 'white',
                boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
              }}>
                {item.pid && (
                  <>
                    <img 
                      src={`${API_BASE}/image/${item.pid}`} 
                      alt={`Product ${item.pid}`}
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
                    <h4 style={{ margin: '0 0 5px 0', fontSize: '16px', color: '#333' }}>
                      {item.name || `Product ${item.pid}`}
                    </h4>
                    <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>ID: {item.pid}</p>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {imageUrl && (
        <div style={{ marginBottom: "30px", backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px' }}>
          <h2 style={{ color: '#555' }}>Image View</h2>
          <img 
            src={imageUrl} 
            alt="Fetched" 
            style={{ 
              maxWidth: "300px", 
              border: '1px solid #ddd',
              borderRadius: '4px'
            }} 
          />
        </div>
      )}

      <div style={{ display: 'flex', gap: '20px', marginBottom: "30px" }}>
        <div style={{ backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px', flex: 1 }}>
          <h2 style={{ color: '#555' }}>Retrain Model</h2>
          <button 
            onClick={retrainModel}
            style={{ 
              padding: '8px 15px', 
              backgroundColor: '#FF9800', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Retrain
          </button>
        </div>
        
        <div style={{ backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px', flex: 1 }}>
          <h2 style={{ color: '#555' }}>Health Check</h2>
          <button 
            onClick={checkHealth}
            style={{ 
              padding: '8px 15px', 
              backgroundColor: '#9C27B0', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Check Health
          </button>
          {healthStatus && <p style={{ marginTop: '10px' }}>Status: {healthStatus}</p>}
        </div>
      </div>
    </div>
  );
}

export default App;