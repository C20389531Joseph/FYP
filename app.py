from flask import Flask, request, jsonify

app = Flask(__name__)

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
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    selected_model = request.form["model"]

    # Dummy response for testing
    feedback = {"Grammar": "Score: 4.0", "Coherence": "Score: 3.5"}

    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
