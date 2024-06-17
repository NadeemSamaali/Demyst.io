import random
import json
import pickle
import numpy as np

# Nltk setup
import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

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
    res = model.predict(np.array([bow]))[0]
    percent_error = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > percent_error]
    results.sort(key = lambda x : x[1], reverse = True)
    return_list = []
    for r in results :
        return_list.append({'intent' : classes[r[0]], 'probability' : str(r[1])})
    return return_list

while True :
    sentence = input('# ')
    prediction = predict_class(sentence)
    tag = prediction[0]['intent']
    for intent in intents['intents'] :
        if intent['tag'] == tag :
            responses = intent['responses']
    print(f'> {responses[random.randint(0, len(responses) - 1)]}')
    continue

    