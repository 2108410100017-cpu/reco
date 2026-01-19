import React, { useState } from "react";
import axios from "axios";

function App() {
  const [recommendInput, setRecommendInput] = useState("");
  const [recommendResult, setRecommendResult] = useState(null);
  const [latestData, setLatestData] = useState([]);
  const [imageUrl, setImageUrl] = useState("");
  const [healthStatus, setHealthStatus] = useState("");

  const API_BASE = "http://localhost:8000"; // adjust if different

  const handleRecommend = async () => {
    try {
      const response = await axios.post(`${API_BASE}/recommend`, {
        query: recommendInput
      });
      setRecommendResult(response.data);
    } catch (err) {
      console.error(err);
      setRecommendResult("Error in recommendation");
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
    <div style={{ padding: "20px" }}>
      <h1>FastAPI React UI</h1>

      <div style={{ marginBottom: "20px" }}>
        <h2>Recommend</h2>
        <input
          type="text"
          placeholder="Enter query"
          value={recommendInput}
          onChange={(e) => setRecommendInput(e.target.value)}
        />
        <button onClick={handleRecommend}>Get Recommendation</button>
        {recommendResult && <pre>{JSON.stringify(recommendResult, null, 2)}</pre>}
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h2>Latest Data</h2>
        <button onClick={fetchLatest}>Fetch Latest</button>
        <ul>
          {latestData.map((item, index) => (
            <li key={index}>
              {JSON.stringify(item)}
              {item.pid && (
                <button onClick={() => fetchImage(item.pid)}>Show Image</button>
              )}
            </li>
          ))}
        </ul>
      </div>

      {imageUrl && (
        <div style={{ marginBottom: "20px" }}>
          <h2>Image</h2>
          <img src={imageUrl} alt="Fetched" style={{ maxWidth: "300px" }} />
        </div>
      )}

      <div style={{ marginBottom: "20px" }}>
        <h2>Retrain Model</h2>
        <button onClick={retrainModel}>Retrain</button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h2>Health Check</h2>
        <button onClick={checkHealth}>Check Health</button>
        {healthStatus && <p>Status: {healthStatus}</p>}
      </div>
    </div>
  );
}

export default App;
