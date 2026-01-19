import React from 'react';

const ImageViewer = ({ imageUrl, onClose }) => {
  if (!imageUrl) {
    // If there's no image URL, don't render anything
    return null;
  }

  return (
    <div style={{ 
      marginBottom: "30px", 
      backgroundColor: '#f9f9f9', 
      padding: '20px', 
      borderRadius: '8px',
      border: '1px solid #e0e0e0'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h2 style={{ color: '#555', margin: 0 }}>Image Viewer</h2>
        <button 
          onClick={onClose}
          style={{
            padding: '5px 10px',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          Close
        </button>
      </div>
      
      <div style={{ textAlign: 'center' }}>
        <img 
          src={imageUrl} 
          alt="Fetched product" 
          style={{ 
            maxWidth: "100%", // Changed to 100% for responsiveness
            height: 'auto',    // Maintain aspect ratio
            maxHeight: "500px", // Set a max height
            border: '1px solid #ddd',
            borderRadius: '4px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
          }}
          onError={(e) => {
            // Handle cases where the image fails to load
            e.target.onerror = null; // Prevent infinite loop
            e.target.src = 'https://picsum.photos/seed/error/400/400.jpg'; // Fallback image
          }}
        />
        <p style={{ marginTop: '10px', fontSize: '12px', color: '#888' }}>
          Source: {imageUrl}
        </p>
      </div>
    </div>
  );
};

export default ImageViewer;