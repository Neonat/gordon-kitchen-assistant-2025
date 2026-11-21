import React, { useState } from "react";

function PhotoPreview({ photo, onClose }) {
  const [isSending, setIsSending] = useState(false); // State to track if the photo is being sent
  const [backendResponse, setBackendResponse] = useState(''); // State to store backend response

  // Handle sending the photo to the backend
  const sendPhotoToBackend = async () => {
    if (photo) {
      setIsSending(true); // Set loading state
      try {
        const response = await fetch('http://localhost:5000/api/upload-photo', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json',
          },
          body: JSON.stringify({ photo }), // Send the base64 photo as JSON
        });
  
        if (response.ok) {
          const data = await response.json();
          setBackendResponse(data.detected_items || 'No items detected');
          alert("Photo successfully analyzed!");
        } else {
          alert("Failed to analyze the photo. Status: " + response.status);
          console.error('Response Error:', await response.text());
        }
      } catch (error) {
        console.error("Error sending photo to backend:", error);
        alert("An error occurred while sending the photo. Please check the console for details.");
      } finally {
        setIsSending(false); // Reset loading state
      }
    } else {
      alert("No photo captured!");
    }
  };
  

  return (
    <div className="photo-preview">
      <img src={photo} alt="Captured preview" />
      <button onClick={onClose}>Retake?</button>
      <button onClick={sendPhotoToBackend} disabled={isSending}>
        {isSending ? "Sending..." : "Analyze Image"}
      </button>

      {backendResponse && (
        <div className="mt-4">
          <h4>Detected Items:</h4>
          <pre className="output-area">{backendResponse}</pre>
        </div>
      )}
    </div>
  );
}

export default PhotoPreview;

