from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import google.generativeai as genai
import os

def index_pdf_elements(elements, api_key: str, index_dir: str = "./faiss_db"):
    genai.configure(api_key=api_key)
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="models/embedding-001",
    #     google_api_key=api_key,
    # )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docs = [
        Document(
            page_content=el["text"],
            metadata={"id": el["id"], "page": el["page"], "doc": el["doc"]},
        )
        for el in elements
    ]
    if os.path.exists(index_dir):
        vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(index_dir)

    return vectorstore.as_retriever(search_kwargs={"k": 20})
