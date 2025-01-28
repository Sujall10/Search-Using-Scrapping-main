import streamlit as st
import requests
from ExtractInformation import extract_information
from FetchHeadlines import fetch_headlines

# Streamlit UI
st.title("Web Scraping")

query = st.text_input("Enter what you want to search:")

if st.button("Fetch Headlines"):
    if query:
        df = fetch_headlines(query)
        if not df.empty:
            st.write("### Visit the following URLs for more information:")
            st.dataframe(df)

            # Extract information from the URLs found in headlines
            urls = df['URL'].tolist()  # Get the list of URLs from the DataFrame
            result = extract_information(query, urls)

            # Display the extracted information
            if result:
                st.write("### Extracted Information:")
                st.write(result)
            else:
                st.write("No relevant information found.")
        else:
            st.write("No data fetched. Try another query.")
    else:
        st.write("Please enter a search query.")
