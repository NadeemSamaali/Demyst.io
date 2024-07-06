import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import wikipedia
from urllib.parse import unquote, urlparse

import requests
from bs4 import BeautifulSoup

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def summarize_text(text, summary_ratio=0.1):
    # Step 1: Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Calculate the number of sentences for the summary
    num_sentences = int(len(sentences) * summary_ratio)
    if num_sentences < 1:
        num_sentences = 1  # Ensure at least one sentence in summary

    # Step 2: Tokenize the text into words
    words = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Step 3: Compute word frequency distribution
    freq_dist = FreqDist(words)
    
    # Step 4: Score each sentence based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        score = sum(freq_dist[word] for word in sentence_words if word in freq_dist)
        sentence_scores[sentence] = score
    
    # Step 5: Select the top-ranked sentences for the summary
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(summary_sentences)
    
    return summary

# URL of the webpage
url = "https://en.wikipedia.org/wiki/Morocco"

def get_text_from_url(url) :
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from the webpage
        return soup.get_text()
    else:
        raise ValueError(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print(get_text_from_url(url))


# Example usage
text = """
Your large body of text goes here. The text can be multiple paragraphs long, 
and the library will attempt to extract the most important sentences to create a summary.
Make sure your text is representative of the content you want summarized.
Summarizing text can help in understanding the key points without reading through the entire document.
This example demonstrates how to use NLTK for simple extractive summarization.
"""

#summary = summarize_text(text, summary_ratio=0.2)  # Adjust the ratio as needed
#print(summary)
