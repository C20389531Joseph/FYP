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

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    setFeedback(result.feedback);
  };

  return (
    <div className="container">
      <h2>Essay Grader</h2>

      {/* Model Selection Dropdown */}
      <label>Select Model:</label>
      <select onChange={(e) => setSelectedModel(e.target.value)}>
        <option value="BERT">BERT</option>
        <option value="LSTM">LSTM</option>
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
