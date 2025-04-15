# Module for grading essays using BERT-based models.
# Supports loading year-specific models and generating scores for input essays.
# Author: Joseph Egan    Complier: VSCode   Last updated:15/04/2025

import os
import torch
from transformers import BertTokenizer, BertModel
from transformers import BertForSequenceClassification
from docx import Document

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

MODEL_PATHS = {'SampleQuestions': 'C:\\Users\\JOSEP\\Documents\\bert_essay_grading_model', '2024Adv4007': 'C:\\Users\\JOSEP\\Documents\\bert_essay_grading_model2', '2023Adv4007': 'C:\\Users\\JOSEP\\Documents\\bert_essay_grading_model3'}

MAX_SCORES_BY_YEAR = {
    "SampleQuestions": [4, 2, 3, 3, 6],
    "2024Adv4007": [3, 2, 3, 2, 5],
    "2023Adv4007": [3, 2, 3, 2, 5]
}

_loaded_models = {}
_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def load_model_for_year(year):
    if year not in _loaded_models:
        model_path = MODEL_PATHS.get(year)
        if not model_path:
            raise ValueError(f"No model path for year {year}")
        model = BertForSequenceClassification.from_pretrained(
            model_path,
            from_tf=True
        )
        model.eval()
        _loaded_models[year] = model
    return _loaded_models[year]


def preprocess(text):
    return _tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

def grade_BERT_essay(text, year):
    model = load_model_for_year(year)
    inputs = preprocess(text)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    scores = outputs.logits.squeeze().tolist()
    
    if isinstance(scores, float):  # error handling
        scores = [scores]
        
    max_scores = MAX_SCORES_BY_YEAR[year]
    formatted_scores = [f"{score:.4f}/{max_score}" for score, max_score in zip(scores, max_scores)]
    return f"Predicted Grade BERT model: {year}\n" + ", ".join(formatted_scores)
