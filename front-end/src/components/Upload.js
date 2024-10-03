import React, { useState } from 'react';
import axios from 'axios';
import './Upload.css'; // Optional for additional styling

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file to upload.');
      return;
    }
    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/gifs/create', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage('Upload successful!');
      console.log('Upload successful:', response.data);
    } catch (error) {
      setMessage('Upload error. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Upload Your Video</h2>
      <form onSubmit={handleUpload} className="text-center">
        <div className="form-group mb-3">
          <input
            type="file"
            className="form-control"
            onChange={handleFileChange}
          />
        </div>
        <button
          type="submit"
          className={`btn btn-primary ${uploading ? 'disabled' : ''}`}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
        {message && (
          <div className={`mt-3 alert ${message.includes('error') ? 'alert-danger' : 'alert-success'}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default Upload;
