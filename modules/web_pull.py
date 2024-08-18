import os
import json
import re
from bs4 import BeautifulSoup
import requests
from modules.summarize import get_summary
from nltk.stem import WordNetLemmatizer
import wikipedia

with open(os.path.join(os.path.dirname(__file__), '../assets/web_pull/url_class.json')) as file:
    url_list = json.load(file)

# Lemmatizer setup
lemmatizer = WordNetLemmatizer()

# TO BUILD : Function to clean up the search sentence into keywords
def cleanup_search_sentence(search_sentence : str) -> str :
    # Loading the intents json file into a dictionary
    with open(os.path.join(os.path.dirname(__file__), '../assets/chatbot/intents.json')) as file :
        intents = json.load(file)
        
    # Extracting non-useful words in search sentence based on the intents pattern
    patterns_internet_search = intents['intents'][6]['patterns']
    patterns_internet_search = [pattern.lower() for pattern in patterns_internet_search]
    to_ignore = []
    for pattern in patterns_internet_search :
        to_ignore += pattern.split()
    to_ignore = list(set(to_ignore))
    to_ignore.remove('history')
    
    # Cleaning up the search sentence
    search_sentence = [lemmatizer.lemmatize(word.lower()) for word in search_sentence.split() if word.lower() not in to_ignore]
    return " ".join(search_sentence)

# Function finding most relevant webpage url based on keywords
def get_url_list(search_sentence : str, url_class = None) :
    
    keywords_split = cleanup_search_sentence(search_sentence).lower().split()
    # print(keywords_split)
    search_query = "+".join(keywords_split)
    
    # Adds website name to search query if domain_restriction is given
    if url_class in url_list.keys() :
        for domain in url_list[url_class] :
            search_query += f'+{domain}'
    
    url = f"https://www.google.com/search?q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Send a GET request to Google
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        search_results = soup.find_all("a")
        links = []
        for result in search_results:
            link = result.get("href")
            # Ignore google account webpages and links containing the keyword video
            if link == None or "google" in link.lower() :
                continue
            elif link.startswith("https://") :
                relevancy = sum(1 for keyword in keywords_split if keyword in link.lower())
                #if relevancy >= 2 or url_class == "video":
                links.append((relevancy, link))
        sorted_links = sorted(links, key=lambda x: x[0], reverse=True)
        return sorted_links
    else:
        print(f"Failed to retrieve Google search results. Status code: {response.status_code}")
        
# Function isolating domain link from a URL
def isolate_domain_url(url : str) -> str :
    domain_output = ''
    counter = 0
    for i in range(len(url)) :
        if url[i] == '/' :
            counter += 1
        domain_output += url[i]
        if counter == 3 or i == len(url)-1 :
            return domain_output
            break
    
# Function to extract bodies of text from url
def get_text(url : str) -> str :
    response = requests.get(url)
    p_output = []
    
    # Getting the components of the url into a beautiful soup object
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove figcaption elements
    for figcaption in soup.find_all('figcaption'):
        figcaption.decompose()

    # Remove img alt attributes (if necessary)
    for img in soup.find_all('img'):
        if 'alt' in img.attrs:
            del img['alt']

    # Remove div or span elements with specific classes (example)
    for caption in soup.find_all(['div', 'span'], class_='caption-class'):
        caption.decompose()
    
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        p_output.extend(re.sub(r'\[\d+\]', '', p.get_text()))
    
    return "".join(p_output)

# Function outputing summary of webpage based on search sentence
def summarize_from_web(search_sentence : str, url_class=None) :
    url = get_url_list(search_sentence, url_class)
    if "khanacademy" in url[0][1] :
        return "Here's a webpage I found on Khan Academy which can help answer your question !"
    elif "wikipedia" in url[0][1] :
        article_title = f"'{url[0][1].split('/')[-1]}'"
        print(url[0][1], article_title)
        summary = wikipedia.summary(article_title)
        return '\n\n'.join(summary.split('\n'))
    else :
        text = get_text(url[0][1])
        summary = get_summary(text)
        return summary

# print(get_url('Can you tell about gravitational forces of blackholes', domain='wikipedia'))