import os
import openai
import pinecone
import langchain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st

if 'response' not in st.session_state:
    st.session_state.response = ''

st.set_page_config(page_title="Enterprise Knowledge Base Search", page_icon=':bar_chart:', layout='wide')
st.title("👋 Enterprise Knowledge Base Search")
sidebar_placeholder = st.sidebar.container()
sidebar_placeholder.header('Knowledge base document:')
sidebar_placeholder.subheader('[Employee Handbook](https://www.foundation.cpp.edu/content/es/d/nh/employee-handbook.pdf)')
sidebar_placeholder.subheader('[SAP Datasphere](https://help.sap.com/doc/80d2a628f5204ca1a60713ff508c5823/cloud/en-US/SAP_Datasphere_Content.pdf)')


#sidebar_placeholder.write('A subset of first 30 pages of the employee handbook')

os.environ['OPENAI_API_KEY'] = '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'
index_name = 'demo-index'

# initialize connection (get API key at app.pinecone.io)
pinecone.init(
    api_key="5e6a8cb6-f036-4a23-9b34-c95aec8e317f",
    environment="us-west1-gcp-free"  # find next to API key
)

# connect to index
#print(pinecone)
index = pinecone.Index(index_name)
# view index stats
#print(index.describe_index_stats())

#Load PDFS
#loader = PyPDFLoader("data/employee-handbook.pdf")
#documents = loader.load()
#print(documents[:5])
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
#docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
docsearch = Pinecone.from_existing_index(index_name, embeddings)

llm = OpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'])
chain = load_qa_chain(llm, chain_type="stuff")

#query = "Tell me meal periods for employees working less than five hours a day"

def send_click():
    with st.spinner("Fetching response..."):
        query = st.session_state.prompt
        docs = docsearch.similarity_search(query, include_metadata=True)
        response = chain.run(input_documents=docs, question=query)
        st.session_state.response = response

st.text_input("Ask something: ", key='prompt', value='Tell me meal periods for employees working less than five hours a day' )
st.button("Send", on_click=send_click)
if st.session_state.response:
     st.subheader("Response: ")
     st.success(st.session_state.response, icon= "🤖")