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
print(index.describe_index_stats())

#Load PDFS
#loader = PyPDFLoader("data/Markets_Cloud HCM Suites for 1,000+ Employee Enterprises.pdf")
loader = WebBaseLoader(["https://research.nelson-hall.com/blogs-webcasts/nelsonhall-blog/?avpage-views=blog&type=post&post_id=1191","https://redthreadresearch.com/microsoft-viva-glint-2023/","https://redthreadresearch.com/the-state-of-people-analytics-technology-market-2023/","https://www.constellationr.com/blog-news/sap-aims-infuse-generative-ai-throughout-its-applications-heres-everything-sap-sapphire"])
documents = loader.load()
#print(documents[:5])
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
#docsearch = Pinecone.from_existing_index(index_name, embeddings)

llm = OpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], model_name="gpt-3.5-turbo")
chain = load_qa_chain(llm, chain_type="stuff")

# query = "Tell me about sap datasphere"
# docs = docsearch.similarity_search(query, include_metadata=True)
# response = chain.run(input_documents=docs, question=query)
print("done")