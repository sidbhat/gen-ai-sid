import os
os.environ["OPENAI_API_KEY"] = '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'

import streamlit as st
from llama_index import download_loader
from llama_index.node_parser import SimpleNodeParser
from llama_index import GPTSimpleVectorIndex
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper, ServiceContext
from langchain import OpenAI
from open_ai_service import OpenAIService
from llama_index import download_loader

doc_path = './data/'
index_file = 'index.json'

if 'response' not in st.session_state:
    st.session_state.response = ''

def send_click():
    with st.spinner("Fetching response..."):
##       st.session_state.response  = OpenAIService.open_ai_query(st.session_state.prompt)
        st.session_state.response = index.query(st.session_state.prompt,response_mode="compact" )

index = None
st.set_page_config(page_title="PDF Chatbot with Open AI", page_icon=':bar_chart:', layout='wide')
st.title("👋 Enterprise document(pdf) chat with Open AI")

sidebar_placeholder = st.sidebar.container()
uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

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

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="da-vinci-003"))

    max_input_size = 2049
    num_output = 256
    max_chunk_overlap = 20
    CHUNK_SIZE_LIMIT = 600
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap,chunk_size_limit=CHUNK_SIZE_LIMIT)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context
    )

    index.save_to_disk(index_file)

elif os.path.exists(index_file):
    print (index_file+" exists ")
    index = GPTSimpleVectorIndex.load_from_disk(index_file)

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader(doc_path, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    doc_filename = os.listdir(doc_path)[0]
    sidebar_placeholder.header('Current Processing Document:')
    sidebar_placeholder.subheader(doc_filename)
    sidebar_placeholder.write(documents[0].get_text()[:1000]+'...')

if index != None:
    st.text_input("Ask something: ", key='prompt')
    st.button("Send", on_click=send_click)
    if st.session_state.response:
        st.subheader("Response: ")
        st.success(st.session_state.response, icon= "🤖")
