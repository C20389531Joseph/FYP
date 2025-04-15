# Utility module for loading and running LSTM models for essay grading.
# Includes support for multiple model years and tokenizers.
# Author: Joseph Egan    Complier: VSCode   Last updated:15/04/2025

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Top-level global load to avoid models not loading in loader functions (unknown why they do not load)
MODEL_PATH = r"C:\Users\JOSEP\Documents\LSTMMocks\essay_grading_model_v2.keras"
TOKENIZER_PATH = r"C:\Users\JOSEP\Documents\LSTMMocks\tokenizer.pkl"

model2 = r"C:\Users\JOSEP\Documents\LSTM2024\essay_grading_model_2024.keras"
tokenizer2 = r"C:\Users\JOSEP\Documents\LSTM2024\tokenizer.pkl"

model3 = r"C:\Users\JOSEP\Documents\LSTM2023\essay_grading_model_2023.keras"
tokenizer3 = r"C:\Users\JOSEP\Documents\LSTM2023\tokenizer.pkl"

modelSampleQuestions = tf.keras.models.load_model(MODEL_PATH)
with open(TOKENIZER_PATH, "rb") as f:
    tokenizerSampleQuestions = pickle.load(f)
    
model2024 = tf.keras.models.load_model(model2)
with open(tokenizer2, "rb") as f:
    tokenizer2024 = pickle.load(f)
    
model2023 = tf.keras.models.load_model(model3)
with open(tokenizer3, "rb") as f:
    tokenizer2023s = pickle.load(f)
    
MAX_SCORES_BY_YEAR = {
    "SampleQuestions": [2, 3, 3, 2],
    "2024Adv4007": [3, 2, 3, 2, 5],
    "2023Adv4007": [3, 2, 3, 2, 5]
}


def grade_LSTM_essay(text,year):
    print("grade_")
    if (year == 'SampleQuestions'):
        sequence = tokenizerSampleQuestions.texts_to_sequences([text])
        model = modelSampleQuestions
        
    if (year == '2024Adv4007'):
        sequence = tokenizer2024.texts_to_sequences([text])
        model = model2024
        
    if (year == '2023Adv4007'):
        sequence = tokenizer2023s.texts_to_sequences([text])
        model = model2023
        
    padded = pad_sequences(sequence, maxlen=500, padding='post', truncating='post')

    max_scores = np.array(MAX_SCORES_BY_YEAR[year])

    # Predict using preloaded model
    raw_scores = model.predict(padded)[0]
    
    formatted_scores = [f"{s:.4f}/{m}" for s, m in zip(raw_scores, max_scores)]
    return f"Predicted Grade LSTM model: {year}\n" + ", ".join(formatted_scores)
