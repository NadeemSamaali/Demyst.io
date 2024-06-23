import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

import random
import json
import pickle
import numpy as np

# Nltk setup
import nltk
nltk.download('punkt', quiet = True)
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet', quiet = True)

# Keras setup
from keras.src.saving.saving_api import load_model

# Lemmatizer setup
lemmatizer = WordNetLemmatizer()

# Loading intents json file
with open('intents.json') as file :
    intents = json.load(file)
    
# Loading pickle files
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Loading model
model = load_model('chatbot_model.h5')

# Function to clean up sentences
def clean_up_sentence(sentence) :
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence.split()]
    return sentence_words

# Function converting sentence into bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words : 
        for i, word in enumerate(words) :
            if word == w :
                bag[i] = 1
    return np.array(bag)

# Function to predict the class of a sentence
def predict_class(sentence) :
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]), verbose = None)[0]
    percent_error = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > percent_error]
    results.sort(key = lambda x : x[1], reverse = True)
    return_list = []
    for r in results :
        return_list.append({'intent' : classes[r[0]], 'probability' : str(r[1])})
    return return_list

# Function getting the tag with highest likely hood from a sentence
def get_tag(sentence) :
    prediction = predict_class(sentence)
    return prediction[0]#['intent']

# Fucntion printing a random response based on the inputted tag
def get_response(tag) :
    #print(tag)
    class_type = tag['intent']
    responses = intents['intents'][classes.index(class_type)]['responses']
    if float(tag['probability']) >= 0.9 :
        return responses[random.randint(0, len(responses)-1)]
    else :
        return "I'm not sure I understand what you're saying ..."

# Chatbot
while True :
    sentence = input('# ')
    tag = get_tag(sentence)
    response = get_response(tag)
    print(f"> {response}")
        
    