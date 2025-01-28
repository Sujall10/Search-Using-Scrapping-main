import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from Query_search import get_search_results

def fetch_headlines(query):
    urls = get_search_results(query)
    data = []

    for url in urls:
        try:
            st.write(f"Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find_all('h1')

            if not headlines:
                st.write("No headlines found. Adjust the selector.")

            for headline in headlines:
                data.append({"URL": url, "Headline": headline.text.strip()})

        except Exception as e:
            st.write(f"Error fetching data from {url}: {e}")

    return pd.DataFrame(data)

# Streamlit UI
st.title("Web Scraping")

query = st.text_input("Enter what you want to search:")

if st.button("Fetch Headlines"):
    if query:
        df = fetch_headlines(query)

        if not df.empty:
            st.write("### Fetched Data:")
            st.dataframe(df)
        else:
            st.write("No data fetched. Try another query.")
    else:
        st.write("Please enter a search query.")
