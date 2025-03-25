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

    # Preprocessing (update with your real logic)
    processed = preprocess_text(text)

    model = load_model_for_year(year)
    result = model.predict(processed)

    return f"Predicted Grade (Model {year}): {result[0]}"