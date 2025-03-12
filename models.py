import torch
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import docx
import numpy as np
from flask import jsonify
import json


tf.get_logger().setLevel("ERROR")

class EssayGradingModel:
    def __init__(self, model_type):
        self.model_type = model_type
        self.models = {
            # "LSTM": tf.keras.models.load_model(r"C:\Users\JOSEP\OneDrive\Documents\FYP\DemoCode\essay_grading_model.keras"),
            "BERT": TFBertForSequenceClassification.from_pretrained(r"C:\Users\JOSEP\Documents\bert_essay_grading_model"),  # Change this
        }
        self.tokenizers = {
            "BERT": BertTokenizer.from_pretrained("bert-base-uncased"),
        }

    def process_text(self, file):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])

    def grade_essay(self, file):
        essay_text = self.process_text(file)

        if self.model_type == "BERT":
            tokenizer = self.tokenizers["BERT"]
            tokens = tokenizer(essay_text, padding=True, truncation=True, return_tensors="tf")
            scores = self.models["BERT"].predict(tokens.data)[0].tolist()
        
        elif self.model_type == "LSTM":
            tokenizer = tf.keras.preprocessing.text.Tokenizer()
            sequence = tokenizer.texts_to_sequences([essay_text])
            padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=500)
            scores = self.models["LSTM"].predict(padded_sequence)[0].tolist()
        
        else:
            raise ValueError("Unsupported model type. Choose either 'LSTM' or 'BERT'.")

        rubric_categories = ["Grammar", "Coherence", "Content Depth", "Language Clarity", "Style"]
        print(scores)  # Debugging step
        scores = scores[0] if isinstance(scores, list) and len(scores) > 0 else []

        scores = scores[:len(rubric_categories)]
        
        print("Generated Scores:", scores)  # Check what model outputs
        print("Rubric Categories:", rubric_categories)  # Ensure categories exist
        
        if len(scores) != len(rubric_categories):
            print(f"Error: Number of scores ({len(scores)}) does not match categories ({len(rubric_categories)})")
            return jsonify({"error": "Model output size mismatch. Please check model predictions."})

        # Formulate feedback
         # Formulate feedback
        feedback = {category: f"{float(score):.2f}" for category, score in zip(rubric_categories, scores)}
        
        return feedback  # Just return the dictionary


