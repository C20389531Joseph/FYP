import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from sklearn.model_selection import train_test_split

# Example dataset
X = ["essay1 content", "essay2 content", "essay3 content"] # split q answer into docs later. Generated dataset
y = [[3, 4, 5], [2, 3, 4], [5, 5, 5]]  # Scores based on rubric categories

# Text vectorization
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)
X_pad = tf.keras.preprocessing.sequence.pad_sequences(X_seq, maxlen=500)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

# Model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=500),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    LSTM(32),
    Dense(64, activation='relu'),
    Dense(3, activation='linear')  
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)
