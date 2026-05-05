### This script runs a vector embedding on service manual data and saves the results to a file
## This is a one time run and the results are saved to a file for later use

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def create_vector_embeddings(pdf_path, index_path):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vector store
    vector_store = FAISS.from_documents(texts, embeddings)

    # Save vector store to disk
    vector_store.save_local(index_path)
    print(f"✅ Vector embeddings created and saved to {index_path}")

if __name__ == "__main__":
    pdf_path = 'service_mode_user_guide.pdf'  # Path to your service manual PDF
    index_path = 'vector_index'      # Directory to save the vector index
    os.makedirs(index_path, exist_ok=True)
    create_vector_embeddings(pdf_path, index_path)