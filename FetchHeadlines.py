from Query_search import get_search_results
from bs4 import BeautifulSoup
import spacy
import pandas as pd
import requests

def fetch_headlines(query):
    urls = get_search_results(query)
    data = []

    for url in urls:
        try:
            # st.write(f"Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find_all('h1')

            if not headlines:
                # st.write("No headlines found. Adjust the selector.")
                continue
            for headline in headlines:
                data.append({"URL": url, "Headline": headline.text.strip()})

        except requests.exceptions.RequestException as e:
            # st.write(f"Error fetching data from {url}: {e}")
            continue
    return pd.DataFrame(data)