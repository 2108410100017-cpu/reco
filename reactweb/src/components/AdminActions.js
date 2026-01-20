import React, { useState } from "react";
import axios from "axios";

const AdminActions = ({ API_BASE }) => {
  const [healthStatus, setHealthStatus] = useState("");
  const [isRetraining, setIsRetraining] = useState(false);
  const [isCheckingHealth, setIsCheckingHealth] = useState(false);
  const [isAddingPrices, setIsAddingPrices] = useState(false);
  const [retrainMessage, setRetrainMessage] = useState("");
  const [priceMessage, setPriceMessage] = useState("");

  const retrainModel = async () => {
    setIsRetraining(true);
    setRetrainMessage("");
    try {
      const response = await axios.post(`${API_BASE}/retrain`);
      setRetrainMessage(`Success: Retraining process started. Server response: ${JSON.stringify(response.data)}`);
    } catch (err) {
      console.error(err);
      setRetrainMessage("Error: Failed to trigger retrain. Please check the server logs.");
    } finally {
      setIsRetraining(false);
    }
  };

  const checkHealth = async () => {
    setIsCheckingHealth(true);
    setHealthStatus("");
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setHealthStatus(response.data.status || "Healthy");
    } catch (err) {
      console.error(err);
      setHealthStatus("Unhealthy");
    } finally {
      setIsCheckingHealth(false);
    }
  };

  const addPrices = async () => {
    setIsAddingPrices(true);
    setPriceMessage("");
    try {
      const response = await axios.post(`${API_BASE}/add-prices`);
      setPriceMessage(`Success: ${response.data.message}`);
    } catch (err) {
      console.error(err);
      setPriceMessage("Error: Failed to add prices. Please check the server logs.");
    } finally {
      setIsAddingPrices(false);
    }
  };

  return (
    <div style={{ marginBottom: "30px" }}>
      <h2 style={{ color: '#333', borderBottom: '2px solid #eee', paddingBottom: '10px', marginBottom: '20px' }}>
        Admin Actions
      </h2>
      
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        {/* Retrain Model Section */}
        <div style={{ 
          backgroundColor: '#fff3e0', 
          padding: '20px', 
          borderRadius: '8px', 
          flex: 1, 
          minWidth: '250px',
          border: '1px solid #ffcc02'
        }}>
          <h3 style={{ color: '#e65100', marginTop: 0 }}>Retrain Model</h3>
          <p style={{ fontSize: '14px', color: '#666', marginBottom: '15px' }}>
            Trigger a retraining of the recommendation model with the latest data.
          </p>
          <button 
            onClick={retrainModel}
            disabled={isRetraining}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: isRetraining ? '#ccc' : '#FF9800', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: isRetraining ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              width: '100%'
            }}
          >
            {isRetraining ? 'Starting Retrain...' : 'Start Retraining'}
          </button>
          {retrainMessage && (
            <p style={{ 
              marginTop: '10px', 
              fontSize: '14px',
              color: retrainMessage.startsWith("Error") ? 'red' : 'green',
              wordBreak: 'break-all'
            }}>
              {retrainMessage}
            </p>
          )}
        </div>
        
        {/* Health Check Section */}
        <div style={{ 
          backgroundColor: '#f3e5f5', 
          padding: '20px', 
          borderRadius: '8px', 
          flex: 1, 
          minWidth: '250px',
          border: '1px solid #ce93d8'
        }}>
          <h3 style={{ color: '#4a148c', marginTop: 0 }}>Health Check</h3>
          <p style={{ fontSize: '14px', color: '#666', marginBottom: '15px' }}>
            Check the status of the API server.
          </p>
          <button 
            onClick={checkHealth}
            disabled={isCheckingHealth}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: isCheckingHealth ? '#ccc' : '#9C27B0', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: isCheckingHealth ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              width: '100%'
            }}
          >
            {isCheckingHealth ? 'Checking...' : 'Check Health'}
          </button>
          {healthStatus && (
            <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#e8eaf6', borderRadius: '4px' }}>
              <p style={{ margin: 0, fontWeight: 'bold' }}>Status:</p>
              <p style={{ 
                margin: '5px 0 0 0', 
                fontSize: '16px',
                color: healthStatus === "ok" || healthStatus === "Healthy" ? 'green' : 'red',
                fontWeight: 'bold'
              }}>
                {healthStatus.toUpperCase()}
              </p>
            </div>
          )}
        </div>
        
        {/* Add Prices Section */}
        <div style={{ 
          backgroundColor: '#e8f5e9', 
          padding: '20px', 
          borderRadius: '8px', 
          flex: 1, 
          minWidth: '250px',
          border: '1px solid #a5d6a7'
        }}>
          <h3 style={{ color: '#2e7d32', marginTop: 0 }}>Add Prices</h3>
          <p style={{ fontSize: '14px', color: '#666', marginBottom: '15px' }}>
            Add price information to all products in the system.
          </p>
          <button 
            onClick={addPrices}
            disabled={isAddingPrices}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: isAddingPrices ? '#ccc' : '#4CAF50', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: isAddingPrices ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              width: '100%'
            }}
          >
            {isAddingPrices ? 'Adding Prices...' : 'Add Prices'}
          </button>
          {priceMessage && (
            <p style={{ 
              marginTop: '10px', 
              fontSize: '14px',
              color: priceMessage.startsWith("Error") ? 'red' : 'green',
              wordBreak: 'break-all'
            }}>
              {priceMessage}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminActions;