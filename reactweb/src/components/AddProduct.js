import React, { useState } from 'react';
import axios from 'axios';

const AddProduct = ({ API_BASE }) => {
  const [businessId, setBusinessId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [image, setImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    
    const formData = new FormData();
    formData.append('business_id', businessId);
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('image', image);
    
    try {
      const response = await axios.post(`${API_BASE}/business/add-product`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setMessage(`Success: Product added with ID ${response.data.id}`);
      // Reset form
      setBusinessId('');
      setName('');
      setDescription('');
      setPrice('');
      setImage(null);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.detail || 'Failed to add product'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ marginBottom: "30px", backgroundColor: '#f0f8ff', padding: '20px', borderRadius: '8px' }}>
      <h2 style={{ color: '#333' }}>Add New Product (Business)</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Business ID:</label>
          <input
            type="text"
            value={businessId}
            onChange={(e) => setBusinessId(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Product Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Description:</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Price ($):</label>
          <input
            type="number"
            step="0.01"
            min="0"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Product Image:</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
            required
            style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
          />
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: '10px 20px',
            backgroundColor: isLoading ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer'
          }}
        >
          {isLoading ? 'Adding Product...' : 'Add Product'}
        </button>
        
        {message && (
          <div style={{ marginTop: '15px', padding: '10px', backgroundColor: message.startsWith('Success') ? '#d4edda' : '#f8d7da', borderRadius: '4px' }}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default AddProduct;