# app.py
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Set up Flask and enable CORS
app = Flask(__name__)
CORS(app)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# Print load message
print('Loading packages. This may take a few seconds ...')

import random
import json
import pickle
import numpy as np
from features.linspace import arithmetics as ln
import features.web_pull as wp

# Nltk setup
import nltk
# nltk.download('punkt', quiet=True)
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet', quiet=True)

# Keras setup
from keras.src.saving.saving_api import load_model

# Lemmatizer setup
lemmatizer = WordNetLemmatizer()

# Loading intents json file
with open('assets/chatbot/intents.json') as file:
    intents = json.load(file)
    
# Loading pickle files
words = pickle.load(open('assets/chatbot/words.pkl', 'rb'))
classes = pickle.load(open('assets/chatbot/classes.pkl', 'rb'))

# Loading model
model = load_model('assets/chatbot/chatbot_model.h5', compile=False)

# Function to clean up sentences
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence.split()]
    return sentence_words

# Function converting sentence into bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Function to predict the class of a sentence
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose=None)[0]
    percent_error = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > percent_error]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Function getting the tag with highest likely hood from a sentence
def get_tag(sentence):
    prediction = predict_class(sentence)
    return prediction[0]

# Function printing a random response based on the inputted tag
def get_response(tag):
    class_type = tag['intent']
    responses = intents['intents'][classes.index(class_type)]['responses']
    if float(tag['probability']) >= 0.8:
        return responses[random.randint(0, len(responses)-1)]
    else:
        return "I'm not sure I understand what you're saying ..."

# Function running the chatbot
def run_chatbot(user_input: str):
    tag = get_tag(user_input)
    intent = tag['intent']
    
    # Performing arithmetical expressions
    if intent == 'arithmetics':
        matches = [user_input[i] for i in range(len(user_input)) if user_input[i] in ['0','1','2','3','4','5','6','7','8','9','(',')','+','-','*','/']]
        if len(matches) == 0:
            raise ValueError("No arithmetical expression found")
        expression = "".join(matches)
        result = ln.parse_and_evaluate(expression)
        return f'{get_response(tag)} {expression} is equal to {result} !'
    
    elif intent == 'internet_search':
        print(f'> {get_response(tag)}')
        url = wp.get_url_list(user_input, url_class='academic')
        summary = wp.summarize_from_web(user_input, url_class='academic')
        return f'Here is a short summary of what I was able to find on the web! \n\n {summary} \n\nSource: {url[0]} '
    
    # Other interactions with chatbot
    else:
        response = get_response(tag)
        return f"{response}"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get("message")
    if user_input:
        response = run_chatbot(user_input)
        return jsonify({"response": response})
    return jsonify({"response": "Invalid input"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
