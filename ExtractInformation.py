import requests
from bs4 import BeautifulSoup
import spacy
import streamlit as st
# from MatchingQuery import match_query_with_similarity

nlp = spacy.load("en_core_web_sm")

def match_query_with_similarity(query, text, threshold=0.7):
    doc_text = nlp(text)
    doc_query = nlp(query)
    
    # Compute similarity with each sentence in the text
    matches = []
    for sentence in doc_text.sents:
        similarity = doc_query.similarity(sentence)
        if similarity >= threshold:  # Match based on a similarity threshold
            matches.append((sentence.text, similarity))
    
    return matches

def extract_information(query, urls):
    relevant_information = []
    for url in urls:
        try:
            # Scrape the content of each URL
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            doc = nlp(query)
            tokens = [token.text for token in doc]
            # st.write(f"Tokens: {tokens}")
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            # st.write(f"Entities: {entities}")
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]
            # st.write(f"Noun Chunks: {noun_chunks}")

            text_content = ' '.join([p.get_text() for p in soup.find_all('p')])

            # Process text with NLP model
            doc = nlp(text_content)

            matches = match_query_with_similarity(query, text_content)
            if matches :
                for match in matches:
                    st.write(f"- {match[0]} (Similarity: {match[1]:.2f})")
                    relevant_information.append(match[0]) 
            # Use keyword matching or NER to find relevant info
            # if query.lower() in text_content.lower():

                # for entity in doc.ents:
                #     # Focus on extracting only relevant entities like "PERSON" or "ORG"
                #     # if entity.label_ == "PERSON" or entity.label_ == "ORG":
                #     if entity.label_ == "PERSON":
                #         relevant_information.append(entity.text)

        except requests.exceptions.RequestException as e:
            # st.write(f"Error fetching data from {url}: {e}")
            continue

    # Return a list of possible results or best match
    return relevant_information