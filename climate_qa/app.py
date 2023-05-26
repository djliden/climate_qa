import streamlit as st
from climate_qa.summarization.summary import Summarizer
from climate_qa.search import DocumentSearch
import pandas as pd
import re

@st.cache_resource
def load_data():
    return DocumentSearch(document_dir="../stored_documents/")

@st.cache_resource
def get_summarizer(documents):
    return Summarizer(documents)

def main():
    st.title('Document Summarization')

    documents = load_data()


    user_input = st.text_area("Please enter your query here:")

    if st.button("Generate Summary"):
        with st.spinner('Generating summary...'):
            search_results = documents.vector_search(query = user_input, top_n = 3)
            summarizer = get_summarizer(search_results)
            summary = summarizer.summarize(user_input)
            response_content = re.search('<response>(.*?)</response>', summary, re.DOTALL)
            if response_content:
                st.write(response_content.group(1))
            else:
                st.write("No response tags found in the summary.")

if __name__ == "__main__":
    main()

