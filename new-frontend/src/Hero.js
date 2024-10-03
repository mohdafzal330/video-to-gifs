import React, { useState } from "react";
import "./Hero.css";
import axios from 'axios';
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
function Hero() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      console.log("Selected video file:", file);
      // Perform any validation or further processing here
    }
  };

  const handleUploadClick = () => {
    document.getElementById("video-upload-input").click();
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/api/gifs/create', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success('Conversion successful!');
      console.log('Conversion successful:', response.data);
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <section className="hero" id="hero">
      <ToastContainer/>
      <h1>Convert Your Videos to GIFs Instantly!</h1>
      <p>Upload any video, customize your GIF, and download in seconds.</p>
      <button className="upload-btn" onClick={handleUploadClick}>
        Upload Video
      </button>
      {/* Hidden file input */}
      <input
        id="video-upload-input"
        type="file"
        accept="video/mp4, video/avi, video/mov" /* Allowed formats */
        style={{ display: "none" }} /* Hide the input */
        onChange={handleFileChange}
      />
      {/* Display selected file info */}
      {selectedFile && (
        <div className="video-upload">
          <p>Selected Video: {selectedFile.name}</p>
          <button onClick={handleUpload} disabled={isUploading}>
            {isUploading ? "Converting..." : "Convert Now"}
          </button>
        </div>
      )}
      <br />
      <br /> <br />
      <img
        src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGhlbXYwZ3lmeWF3aXBrcXJqa3BwanU2MWhtbHY3cndoa2F0c2VjaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9dg/r2wde5QYFcYnB8ujcM/giphy.gif"
        alt="Example GIF"
        className="example-gif"
      />
    </section>
  );
}

export default Hero;
