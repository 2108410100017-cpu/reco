import React, { useState } from "react";
import './App.css'; // Optional: for global styles

// Import all the modular components
import SearchRecommendations from './components/SearchRecommendations';
import LatestProducts from './components/LatestProducts';
import ImageViewer from './components/ImageViewer';
import AdminActions from './components/AdminActions';

function App() {
  // Base URL for all API calls
  const API_BASE = "http://localhost:8000";

  // State to control the ImageViewer component.
  // When an image URL is set, the viewer will appear.
  const [imageUrl, setImageUrl] = useState(null);

  /**
   * Handler function to be passed to child components (like LatestProducts).
   * When a product image is selected, this function updates the state,
   * causing the ImageViewer to render with the correct image URL.
   * @param {string|number} pid - The product ID of the image to show.
   */
  const handleImageSelect = (pid) => {
    setImageUrl(`${API_BASE}/image/${pid}.jpg`);
  };

  /**
   * Handler function to be passed to the ImageViewer component.
   * Clears the imageUrl state, which hides the ImageViewer.
   */
  const handleCloseViewer = () => {
    setImageUrl(null);
  };

  return (
    <div style={{ padding: "20px", fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f7f6' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ color: '#2c3e50', margin: 0 }}>Image Recommendation System</h1>
        <p style={{ color: '#7f8c8d' }}>Discover products powered by AI</p>
      </header>

      <main>
        {/* Component for searching and displaying recommendations */}
        <SearchRecommendations API_BASE={API_BASE} />

        {/* Component for displaying the latest products.
            We pass the image selection handler so it can communicate with the ImageViewer. */}
        <LatestProducts 
          API_BASE={API_BASE} 
          onImageSelect={handleImageSelect} 
        />

        {/* The ImageViewer component. It only renders when imageUrl is not null.
            We pass the current imageUrl and the function to close it. */}
        <ImageViewer 
          imageUrl={imageUrl} 
          onClose={handleCloseViewer} 
        />

        {/* Component for administrative actions like retraining and health checks */}
        <AdminActions API_BASE={API_BASE} />
      </main>

      <footer style={{ textAlign: 'center', marginTop: '40px', padding: '20px', color: '#95a5a6', fontSize: '14px' }}>
        <p>&copy; 2024 Image Recommendation App</p>
      </footer>
    </div>
  );
}

export default App;