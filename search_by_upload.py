import os

import streamlit as st
from open_ai_service import OpenAIService
from llama_index import download_loader
import streamlit_analytics

doc_path = './data/'
index_file = 'index.json'

if 'response' not in st.session_state:
    st.session_state.response = ''
if 'file_contents' not in st.session_state:
    st.session_state.file_contents = ''
def send_click():
    with st.spinner("Fetching response..."):
       st.session_state.response = OpenAIService.open_ai_query(f"{st.session_state.prompt} {st.session_state.file_contents}",model="anthropic-claude-v2")



st.set_page_config(page_title="PDF Chatbot with Anthropic", page_icon=':bar_chart:', layout='wide')
st.title("👋 Document(pdf) chat with Anthropic")

sidebar_placeholder = st.sidebar.container()
uploaded_file = st.file_uploader("Choose a file (upto 4MB)", type=['pdf'])

if uploaded_file is not None:

    doc_files = os.listdir(doc_path)
    for doc_file in doc_files:
        os.remove(doc_path + doc_file)

    bytes_data = uploaded_file.read()
    with open(f"{doc_path}{uploaded_file.name}", 'wb') as f:
        f.write(bytes_data)

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

    loader = SimpleDirectoryReader(doc_path, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    sidebar_placeholder.header('Current Processing Document:')
    sidebar_placeholder.subheader(uploaded_file.name)
    sidebar_placeholder.write(documents[0].get_text()[:1000]+'...')

    st.session_state.file_contents = documents[0].get_text()

with streamlit_analytics.track():
    st.text_input("Ask something: ", key='prompt')
    st.button("Send", on_click=send_click)
if st.session_state.response:
    st.subheader("Response: ")
    st.success(st.session_state.response, icon= "🤖")
