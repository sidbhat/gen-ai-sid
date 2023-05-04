import os

import streamlit as st
from langchain.llms import AzureOpenAI
from open_ai_service import OpenAIService
from llama_index import download_loader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://azure-openai-serv-i057149.cfapps.sap.hana.ondemand.com"
os.environ["OPENAI_API_KEY"] = OpenAIService.get_token()

doc_path = './data/'
index_file = 'index.json'
chat_history = []

if 'response' not in st.session_state:
    st.session_state.response = ''

def send_click():
    with st.spinner("Fetching response..."):
##       st.session_state.response  = OpenAIService.open_ai_query(st.session_state.prompt)
# Adapt if needed
        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:""")

        qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                           retriever=db.as_retriever(),
                                           condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                           return_source_documents=True,
                                           verbose=False)
        st.session_state.response =  qa({"question": st.session_state.prompt, "chat_history": chat_history})

index = None
st.set_page_config(page_title="PDF Chatbot with Open AI", page_icon=':bar_chart:', layout='wide')
st.title("👋 Enterprise document(pdf) chat with Open AI")

sidebar_placeholder = st.sidebar.container()
uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

loader = DirectoryLoader('data/', glob="*.txt", loader_cls=TextLoader)

documents = loader.load()
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1)

db = FAISS.from_documents(documents=docs, embedding=embeddings)



st.text_input("Ask something: ", key='prompt')
st.button("Send", on_click=send_click)
if st.session_state.response:
     st.subheader("Response: ")
     st.success(st.session_state.response, icon= "🤖")

