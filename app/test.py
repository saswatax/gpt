from dotenv import load_dotenv

load_dotenv()

import os
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma

from langchain.retrievers import PineconeHybridSearchRetriever

import pinecone

import tiktoken

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"],
)

index_name = "langchain-demo"
embeddings = OpenAIEmbeddings()


pinecone.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    pod_type="s1",
)

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=0
)

loader = TextLoader("./app/data/state_of_the_union.txt")
documents = loader.load()
docs = text_splitter.split_documents(documents)
db = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# index = pinecone.Index(index_name)
# retriever = db.as_retriever()
retriever = PineconeHybridSearchRetriever(embeddings=embeddings, index=db, tokenizer=tiktoken)

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
# query = "Tell me all the holidays"
query = "What did the president say about Ketanji Brown Jackson"
print(qa.run(query))


# croma - local db
# loader = PyPDFLoader("./app/data/VenturePact Team Handbook.pdf")
# documents = loader.load_and_split()
# db = Chroma.from_documents(docs, embeddings)


# from langchain.document_loaders import TextLoader
# from langchain.indexes import VectorstoreIndexCreator


# def train():
#     global index
#     loader = TextLoader("./app/data/state_of_the_union.txt")
#     index = VectorstoreIndexCreator().from_loaders([loader])


# def query():
#     global inedex
#     query = "What did the president say about Ketanji Brown Jackson"
#     answer = index.query(query)
#     print(answer)


# if __name__ == "__main__":
#     train()
#     query()
