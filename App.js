import React, { useState } from "react";

export default function EssayGrader() {
  const [selectedModel, setSelectedModel] = useState("BERT");
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState("");

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload an essay file!");
      return;
    }

    const formData = new FormData();
    formData.append("model", selectedModel);
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,  // No JSON.stringify
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      setFeedback(data);  // Store response feedback
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit essay. Check console for details.");
    }
  };

  return (
    <div className="container">
      <h2>Essay Grader</h2>

      {/* Model Selection Dropdown */}
      <label>Select Model:</label>
      <select onChange={(e) => setSelectedModel(e.target.value)}>
        <option value="LSTM">LSTM</option>
        <option value="BERT">BERT</option>
        <option value="GPT">GPT</option>
      </select>

      {/* File Upload */}
      <input type="file" onChange={handleFileUpload} />

      {/* Submit Button */}
      <button onClick={handleSubmit}>Grade Essay</button>

      {/* Display Feedback */}
      {feedback && (
        <div>
          <h3>Feedback:</h3>
          <pre>{JSON.stringify(feedback, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

/*
 TODO test redesign 
import React, { useState } from "react";

export default function AssignmentSubmission() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);
    if (event.dataTransfer.files.length > 0) {
      setFile(event.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a file before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      alert("Submission successful!");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit. Check console for details.");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h2>Submit Assignment</h2>
      <p><strong>Files to submit:</strong> {file ? file.name : "(0) file(s) to submit"}</p>
      
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          border: "2px dashed #ccc",
          padding: "20px",
          textAlign: "center",
          marginBottom: "10px",
          backgroundColor: dragActive ? "#f0f0f0" : "white"
        }}
      >
        {file ? file.name : "Drag & drop a file here or click to upload"}
        <input type="file" onChange={handleFileUpload} style={{ display: "none" }} />
      </div>
      
      <button onClick={handleSubmit} style={{ marginRight: "10px" }}>Submit</button>
      <button onClick={() => setFile(null)}>Cancel</button>
    </div>
  );
}
*/