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
from keras.src.models import Sequential
from keras.src.layers import Dense, Activation, Dropout
from keras.src.optimizers import SGD

# Lemmatizer setup
lemmatizer = WordNetLemmatizer()

# Load json file
with open('intents.json') as file :
    intents = json.load(file)

# Unpacking data into tokens
words = []
classes = []
documents = []
to_ignore = ['?', '!', '.', ',']
 
for intent in intents['intents'] :
    for pattern in intent['patterns'] :
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        if intent['tag'] not in classes : classes.append(intent['tag'])
        documents.append((word_list, intent['tag']))
        
# Lemmatizing the tokens in the words list
words = [lemmatizer.lemmatize(word) for word in words if word not in to_ignore]
words = sorted(set(words))

# Serializing the words and classes list into pickle files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Initializing training data
training = []
out_empty = [0] * len(classes)

# Creating the training data
for document in documents : 
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word).lower() for word in word_patterns]
    for word in words :
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(out_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Preparing the training data
random.shuffle(training)
training = np.array(training, dtype=object)  # Keep training as a NumPy array with dtype=object

# Extracting train_x and train_y from the NumPy array
train_x = np.array([element[0] for element in training])
train_y = np.array([element[1] for element in training])

# Setting up the model
model = Sequential()
model.add(Dense(128, input_shape =(len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics=['accuracy'])

# Training the model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')