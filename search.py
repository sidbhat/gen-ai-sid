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
from langchain.llms import OpenAIChat

if 'response' not in st.session_state:
    st.session_state.response = ''

st.set_page_config(page_title="Enterprise Knowledge Base Search", page_icon=':bar_chart:', layout='wide')
st.title("👋 Enterprise Knowledge Base Search")
sidebar_placeholder = st.sidebar.container()
sidebar_placeholder.header('Knowledge base documents:')
sidebar_placeholder.subheader('[Employee Handbook](https://www.foundation.cpp.edu/content/es/d/nh/employee-handbook.pdf)')
sidebar_placeholder.subheader('[Gartner Cloud HCM Vendor Comparison](https://www.gartner.com/reviews/market/cloud-hcm-suites-for-1000-employees)')
sidebar_placeholder.subheader('[Benefits Guide](https://selecthealth.org/-/media/providerdevelopment/pdfs/manuals/masterprm_120121.ashx)')
sidebar_placeholder.subheader('[HR RFP](http://fresnoeoc.org/files/pdf/180215-hris-rfp.pdf)')


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

llm = OpenAIChat(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'],model_name='gpt-3.5-turbo')
chain = load_qa_chain(llm, chain_type="stuff")

#query = "Tell me meal periods for employees working less than five hours a day"

def send_click():
    with st.spinner("Fetching response..."):
        query = st.session_state.prompt
        docs = docsearch.similarity_search(query, include_metadata=True)
        response = chain.run(input_documents=docs, question=query)
        print(chain)
        # total_tokens = response.get("total_tokens")
        # # pricing logic: https://openai.com/pricing#language-models
        # if st.session_state.model == "gpt-3.5-turbo":
        #     cost = total_tokens * 0.002 / 1000

        st.session_state.response = response
        # st.session_state.response.append(cost)

c1, c2, c3 = st.columns(3)

with c1:
    st.info("What are the vendors listed in the HCM vendor comparison guide?")
with c2:
    st.info("What are the questions listed in the HR RFP guide?")
with c3:
    st.info("Show the reviews provided for Workday Human Capital vendor")

st.text_input("Ask something: ", key='prompt', value='What are the meal periods for employees working less than five hours a day' )
st.button("Send", on_click=send_click)
if st.session_state.response:
     st.subheader("Response: ")
     st.success(st.session_state.response, icon= "🤖")