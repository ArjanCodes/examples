import React, { useState } from "react";
import "./App.css";
import axios from "axios";
import logo from "./logo.svg"; // Placeholder logo (replace with your own)

const App = () => {
  const [videoName, setVideoName] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const handleUpload = async () => {
    try {
      const response = await axios.post("http://localhost:8080/upload", {
        video_name: videoName,
        headers: { 'Content-Type': 'application/json'}
        
      });
      setVideoUrl(response.data.video_url);
    } catch (error) {
      console.error("Error uploading video:", error.message);
    }
  };

  const fakeUrl = videoUrl && `academy.arjancodes.com${videoUrl}`;

  return (
    <div className="app-container">
      <div className="upload-card">
        <img src={logo} alt="Logo" className="logo" />

        <h3>Upload Your Video</h3>
        <input
          type="text"
          className="input-field"
          value={videoName}
          onChange={(e) => setVideoName(e.target.value)}
          placeholder="Enter video name"
        />
        <button className="upload-button" onClick={handleUpload}>
          Upload Video
        </button>
        {fakeUrl && <p className="video-url">Uploaded video URL:</p>}
        {fakeUrl && <p className="video-url">{fakeUrl}</p>}
      </div>
    </div>
  );
};

export default App;
