from bs4 import BeautifulSoup
import requests
import urllib
from summarize import get_summary

# Function finding most relevant webpage url based on keywords
def get_url(search_sentence : str, domain = None) :
    keywords_split = search_sentence.lower().split()
    search_query = "+".join(keywords_split)
    
    # Adds website name to search query if domain_restriction is given
    if domain :
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
            if link == None or link.startswith("https://accounts.google.com/") or "video" in link.lower() or "scholar.google" in link.lower():
                continue
            elif link.startswith("https://") :
                    if domain :
                        if domain.lower() in link.lower() :
                            count = sum(1 for keyword in keywords_split if keyword.lower() in link.lower())
                            if count >= 3 :
                                links.append(link)
                    else :
                        count = sum(1 for keyword in keywords_split if keyword.lower() in link.lower())
                        if count >= 2 :
                            links.append(link)
        return links[0] if len(links) != 0 else None
    else:
        print(f"Failed to retrieve Google search results. Status code: {response.status_code}")
    
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
        p_output.append(p.get_text())
    return " ".join(p_output)

# Function outputing summary of webpage based on search sentence
def summarize_from_web(search_sentence : str, domain=None) :
    url = get_url(search_sentence, domain)
    text = get_text(url)
    summary = get_summary(text, 6)
    return summary

output_text = summarize_from_web('Meme culture in the 21st century', domain='wikipedia')
print(output_text)