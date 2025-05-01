
from datasets import load_dataset
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import os

def get_vector_store(persist_dir="./mental_health_vectorstore"):
    # Load embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # If already exists, load it
    if os.path.exists(persist_dir):
        vector_store = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
    else:
        # Otherwise, create and save it
        dataset = load_dataset("Amod/mental_health_counseling_conversations", split="train")
        texts = [
            f"Context: {row['Context']} | Response: {row['Response']}"
            for row in dataset.select(range(1500))
        ]
        documents = [Document(page_content=text) for text in texts]
        vector_store = Chroma.from_documents(documents, embedding_model, persist_directory=persist_dir)
        vector_store.persist()

    return vector_store, embedding_model
