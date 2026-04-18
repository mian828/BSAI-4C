
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, jsonify
import numpy as np
from gensim.models import Word2Vec
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

app = Flask(__name__)

# 🔹 Training Data (simple intents)
sentences = [
    ["hello"], ["hi"],
    ["library", "timing"],
    ["issue", "book"],
    ["fine"],
    ["return", "book"],
    ["bye"]
]

responses = [
    "Hello! Welcome to Library 📚",
    "Hello! Welcome to Library 📚",
    "Library is open from 9 AM to 5 PM.",
    "You can issue 3 books for 14 days.",
    "Fine is Rs.10 per day.",
    "Return books before due date.",
    "Goodbye!"
]

# 🔹 Word2Vec Model
w2v_model = Word2Vec(sentences, vector_size=10, min_count=1)

# Convert sentence to vector
def sentence_vector(sentence):
    words = sentence.split()
    vec = np.zeros(10)
    for word in words:
        if word in w2v_model.wv:
            vec += w2v_model.wv[word]
    return vec / len(words) if len(words) > 0 else vec

# Prepare training data
X = np.array([sentence_vector(" ".join(s)) for s in sentences])
y = np.array(range(len(responses)))

# 🔹 ANN Model
model = Sequential()
from keras import Sequential, Input
model = Sequential([
    Input(shape=(10,)),
    Dense(64, activation='relu')
])
model.add(Dense(len(responses), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=10, verbose=0)


# 🔹 Chatbot Response
def get_response(user_input):
    vec = sentence_vector(user_input)
    pred = model.predict(np.array([vec]), verbose=0)
    index = np.argmax(pred)
    return responses[index]

# 🔹 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_text = request.form["msg"]
    response = get_response(user_text.lower())
    return jsonify({"response": response})


    
if __name__ == "__main__":
    model.fit(X, y, epochs=10, verbose=0)
    app.run(debug=True)
