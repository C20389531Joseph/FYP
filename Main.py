import os
import docx
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from sklearn.model_selection import train_test_split
import numpy as np

# Function to load answers from Word documents
def load_answers_from_docs(doc_files):
    questions = []
    answers = []
    scores = []
    
    for doc_file in doc_files:
        doc = docx.Document(doc_file)
        for paragraph in doc.paragraphs:
            if paragraph.text.startswith("Q"):  # Assume question text starts with "Q"
                questions.append(paragraph.text)
            elif paragraph.text.startswith("A"):  # Assume answer text starts with "A"
                answers.append(paragraph.text[2:].strip())  # Skip "A:"
            elif paragraph.text.startswith("Score"):  # Assume score starts with "Score:"
                scores.append([float(x) for x in paragraph.text.split(":")[1].strip().split(",")])
    
    return questions, answers, scores

# Load dataset
doc_files = ["answerset1.doc", "answerset2.doc", "answerset3.doc", "answerset4.doc", "answerset5.doc", "answerset6.doc", "answerset7.doc", "answerset8.doc", "answerset9.doc", "answerset10.doc",]
questions, answers, scores = load_answers_from_docs(doc_files)

# Preprocess text: Tokenization and padding
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(answers)
answers_seq = tokenizer.texts_to_sequences(answers)
answers_pad = tf.keras.preprocessing.sequence.pad_sequences(answers_seq, maxlen=500)

# Convert scores to NumPy array for model compatibility
scores = np.array(scores)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(answers_pad, scores, test_size=0.2, random_state=42)

# Define the model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=500),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    LSTM(32),
    Dense(64, activation='relu'),
    Dense(len(scores[0]), activation='linear')  # Output matches the rubric categories
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Save the model
model.save("essay_grading_model.h5")

print("Model trained and saved successfully!")
