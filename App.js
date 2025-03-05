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
