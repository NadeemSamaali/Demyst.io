import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

import random
import json
import pickle
import numpy as np
from features.linspace.arithmetics import parse_and_evaluate
import re

import features.web_pull as wp

# Nltk setup
import nltk
#nltk.download('punkt', quiet = True)
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet', quiet = True)

# Keras setup
from keras.src.saving.saving_api import load_model

# Lemmatizer setup
lemmatizer = WordNetLemmatizer()

# Loading intents json file
with open('assets/intents.json') as file :
    intents = json.load(file)
    
# Loading pickle files
words = pickle.load(open('assets/words.pkl', 'rb'))
classes = pickle.load(open('assets/classes.pkl', 'rb'))

# Loading model
print(':: Loading the chatbot model ::')
model = load_model('assets/chatbot_model.h5', compile = False)

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
    if float(tag['probability']) >= 0.8 :
        return responses[random.randint(0, len(responses)-1)]
    else :
        return "I'm not sure I understand what you're saying ..."
    
# Function running the chatbot    
def run_chatbot(user_input : str) :
    tag = get_tag(user_input)
    intent = tag['intent']
    
    # Performing arithmetical expressions
    if intent == 'arithmetics' :
        matches = [user_input[i] for i in range(len(user_input)) if user_input[i] in ['0','1','2','3','4','5','6','7','8','9','(',')','+','-','*','/']]
        if len(matches) == 0 :
            raise ValueError("No arithmetical expression found")
        expression = "".join(matches)
        result = parse_and_evaluate(expression)
        return f'> {get_response(tag)} The result of {expression} is {result} !'
    
    elif intent == 'internet_search' :
        print(f'> {get_response(tag)}')
        url = wp.get_url(user_input)
        summary = wp.summarize_from_web(user_input, domain='wikipedia')
        return f'> Here is a short summary of what I was able to find on the web ! \n{'='*10} \n {summary} \n~ Source : {url} \n{'='*10} '
    
    # Other interactions with chatbot
    else :
        response = get_response(tag)
        return f"> {response}"

# Main loop        
if __name__ == "__main__" :
    
    try : 
        while True : 
            user_input = input('# ')
            response = run_chatbot(user_input)
            print(response)
    except ValueError as e :
        print(f'# ERROR : {e}')