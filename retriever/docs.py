import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import chroma


def load_pdf_document(file_path):
    loader = PyPDFLoader(file_path=file_path)
    doc = loader.load()
    return doc


def create_chunks(document):
    text_splitter = CharacterTextSplitter()
    chunked_docs = text_splitter.split_documents(document)
    return chunked_docs


def load_document_embeddings(chunked_docs, persist_path=None):
    # a workaround hack to get things running in containers
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    embeddings = OllamaEmbeddings(base_url=base_url)
    db = chroma.Chroma(persist_directory=persist_path)
    vectors = db.from_documents(chunked_docs, embeddings)

    return vectors
