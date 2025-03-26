import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from docx import Document

MODEL_PATHS = {
    "2025": r"C:\Users\JOSEP\OneDrive\Documents\FYP\WebsiteDemo\essay_grading_model.keras",
    "2024": r"C:\Users\JOSEP\OneDrive\Documents\FYP\NewModelData\essay_grading_model2.keras",
    "2023": r"C:\Users\JOSEP\OneDrive\Documents\FYP\NewModelData\essay_grading_model3.keras"
}
MAX_SCORES_BY_YEAR = {
    "2025": [4, 2, 3, 3, 6],
    "2024": [3, 2, 3, 2, 5],
    #"2023": [3, 2, 3, 2, 5]
}


_loaded_models = {}

# Initialize tokenizer (ideally, you'd load your trained tokenizer)
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(["dummy"])  # Prevent tokenizer errors before real fitting

def preprocess_text(text):
    # Tokenize
    sequences = tokenizer.texts_to_sequences([text])
    # Pad to the expected length
    padded = pad_sequences(sequences, maxlen=500, padding='post', truncating='post')
    return padded

def load_model_for_year(year):
    if year not in _loaded_models:
        model_path = MODEL_PATHS.get(year)
        if model_path:
            _loaded_models[year] = tf.keras.models.load_model(model_path)
        else:
            raise ValueError(f"No model found for year {year}")
    return _loaded_models[year]

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext == ".docx":
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type. Only .txt and .docx are allowed.")

def grade_essay(filepath, year):
    text = extract_text(filepath)

    # Preprocessing
    processed = preprocess_text(text)

    model = load_model_for_year(year)
    result = model.predict(processed)[0]  # Get the first (and likely only) prediction

    max_scores = MAX_SCORES_BY_YEAR.get(year)
    if not max_scores:
        raise ValueError(f"No max scores defined for year {year}")

    # Format each prediction as actual_score/max_score
    formatted_scores = [f"{score:.4f}/{max_score}" for score, max_score in zip(result, max_scores)]
    formatted_output = ", ".join(formatted_scores)

    return f"Predicted Grade (Model {year}): {formatted_output}"
