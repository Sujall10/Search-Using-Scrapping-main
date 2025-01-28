import requests
from bs4 import BeautifulSoup
import urllib.parse  # For decoding URLs

def get_search_results(query):
    # Define Search Query and URL
    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract URLs
    results = []
    links = soup.find_all("a", class_="result__a")
    for link in links[:15]:  # Limit 
        href = link.get("href")
        if href and "uddg=" in href:
            # Extract and decode the actual URL
            parsed_url = urllib.parse.urlparse(href)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            actual_url = query_params.get("uddg", [None])[0]
            if actual_url:
                results.append(actual_url)
    return results
