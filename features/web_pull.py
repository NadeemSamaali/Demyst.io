from bs4 import BeautifulSoup
import requests
import urllib

# Function finding most relevant webpage url based on keywords
def get_url(search_words : str, domain_restriction = None ) :
    keywords_split = search_words.lower().split()
    search_query = "+".join(keywords_split)
    
    # Adds website name to search query if domain_restriction is given
    if domain_restriction :
        search_query += f'+{domain_restriction}'
    
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
            if link == None or link.startswith("https://accounts.google.com/") or "video" in link.lower():
                continue
            elif link.startswith("https://") :
                    if domain_restriction :
                        if domain_restriction.lower() in link.lower() :
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
    
# TO-BUILD : Function to extract bodies of text from url
def get_text(url : str) -> str :
    pass

url_to_check = get_url('Meme culture in the 21st century', domain_restriction='Wikipedia')
print(url_to_check)