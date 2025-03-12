import React, { useState, useRef } from "react";

export default function AssignmentSubmission() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [model, setModel] = useState("LSTM");
  const [feedback, setFeedback] = useState("");
  const fileInputRef = useRef(null);

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

  const handleClickUpload = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a file before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model", model);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log(result); 
      setFeedback(result || {});
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit. Check console for details.");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Automatic Exam Essay Grader with AI Feedback <br></br></h1>
      <p>My automatic exam essay grader with AI feedback program allows students to get estimates of 
        the quality of their exam practice and possibly points of feedback and advice on weaknesses and potential 
        areas of improvements for their study. This system will use a combination of BERT and LSTM machine learning 
        models to grade practice exam papers. The results of this paper and the grading rubric, and the paper will be 
        passed on into an AI that will rewrite the grade and feedback into a more human readable format and with additional context.</p>
        
      <h2>Submit Assignment</h2>
      <p><strong>Files to submit:</strong> {file ? file.name : "(0) file(s) to submit"}</p>
      
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClickUpload}
        style={{
          border: "2px dashed #ccc",
          padding: "20px",
          textAlign: "center",
          marginBottom: "10px",
          backgroundColor: dragActive ? "#f0f0f0" : "white",
          cursor: "pointer"
        }}
      >
        {file ? file.name : "Drag & drop a file here or click to upload"}
        <input type="file" ref={fileInputRef} onChange={handleFileUpload} style={{ display: "none" }} />
      </div>
      
      <label>Select Model:</label>
      <select value={model} onChange={(e) => setModel(e.target.value)} style={{ display: "block", marginBottom: "10px" }}>
        <option value="LSTM">LSTM</option>
        <option value="BERT">BERT</option>
        <option value="GPT">GPT</option>
      </select>
      
      <button onClick={handleSubmit} style={{ marginRight: "10px" }}>Submit</button>
      <button onClick={() => setFile(null)}>Cancel</button>
      
      {feedback && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc", backgroundColor: "#f9f9f9" }}>
          <strong>Feedback:</strong>
          {Object.keys(feedback).length === 0 ? (
            <p>No feedback available. Please check if the model type or file is correct.</p>
          ) : (
            <ul>
              {Object.entries(feedback).map(([category, score]) => (
                <li key={category}>
                  <strong>{category}:</strong> {score}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
