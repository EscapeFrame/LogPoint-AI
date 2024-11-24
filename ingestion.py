from os.path import split

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    path = "/Users/pdh/Desktop/프로젝트/LogPoint-RAG/mouse_article.pdf"
    loadder = PyPDFLoader(file_path=path)
    documment = loadder.load()
    spliter = CharacterTextSplitter(chunk_size=2581, chunk_overlap=200, separator="\n")
    text = spliter.split_documents(documment)
    embedder = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    PineconeVectorStore.from_documents(documents=text, embedding=embedder, index_name=os.getenv("INDEX_NAME"))