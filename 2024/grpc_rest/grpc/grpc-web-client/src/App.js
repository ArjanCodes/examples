import React, { useState } from 'react';
import { EncodingServiceClient } from 'grpc/encoding_grpc_web_pb';
import { UploadVideoRequest } from 'grpc/encoding_pb';
import './App.css'; // Import the updated styles
import logo from './logo.svg'; // Placeholder logo (replace with your own)

const client = new EncodingServiceClient('http://localhost:8080');

const App = () => {
  const [videoName, setVideoName] = useState('');
  const [videoUrl, setVideoUrl] = useState('');

  const handleUpload = () => {
    const request = new UploadVideoRequest();
    request.setVideoName(videoName);

    client.uploadVideo(request, {}, (err, response) => {
      if (err) {
        console.error('Error uploading video:', err.message);
        return;
      }
      setVideoUrl(response.getVideoUrl());
    });
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
        <button className="upload-button" onClick={handleUpload}>Upload Video</button>
        {fakeUrl && <p className="video-url">Uploaded video URL:</p>}
        {fakeUrl && <p className="video-url">{fakeUrl}</p>}
      </div>
    </div>
  );
};

export default App;
