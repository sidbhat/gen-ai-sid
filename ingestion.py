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
from langchain.document_loaders import WebBaseLoader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter


index_name = 'demo-index'

# initialize connection (get API key at app.pinecone.io)
pinecone.init(
    api_key="5e6a8cb6-f036-4a23-9b34-c95aec8e317f",
    environment="us-west1-gcp-free"  # find next to API key
)

# connect to index
if index_name not in pinecone.list_indexes():
    # if does not exist, create index
    pinecone.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric='cosine',
    )
index = pinecone.Index(index_name)
print(index.describe_index_stats())


def load_knowledge_base(str_: str):
    #Load PDFS
    loader = PyPDFLoader(str_)
    documents = loader.load()
    print(documents[:5])
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

    llm = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], model_name="gpt-3.5-turbo", model_kwargs={'max_tokens':500})
    chain = load_qa_chain(llm, chain_type="stuff")

    query = "Summarize the document " + str_

    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    docs = docsearch.similarity_search(query, include_metadata=True)
    print(len(docs))
    char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    d = char_text_splitter.split_documents(docs)
    print(len(d))
    response = chain.run(input_documents=d[:1], question=query)
    print(response)
    print("done")