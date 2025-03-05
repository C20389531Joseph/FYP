from flask import Flask, request, jsonify
from flask_cors import CORS
from models import EssayGradingModel


app = Flask(__name__)

CORS(app)  # Enable CORS

# ✅ Add a route for `/`
@app.route("/")  
def home():
    return "✅ Essay Grading API is running! Use /upload to submit an essay."

# ✅ Add a route for `/favicon.ico` to prevent unnecessary errors
@app.route("/favicon.ico")
def favicon():
    return "", 204  # Returns an empty response with status code 204 (No Content)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:  # Check if file is sent
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]  # Get file from request
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Get the model type from the form data
    model_type = request.form.get("model")
    if model_type not in ["LSTM", "BERT", "GPT"]:
        return jsonify({"error": "Invalid model type"}), 400

    # Create an instance of EssayGradingModel
    essay_grader = EssayGradingModel(model_type)
    
    # Process the file and grade the essay
    feedback = essay_grader.grade_essay(file)
    
    # Return feedback as a JSON response
    return jsonify(feedback), 200
if __name__ == "__main__":
    app.run(debug=True)
