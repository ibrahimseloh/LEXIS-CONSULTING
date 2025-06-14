from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import google.generativeai as genai

def index_pdf_elements(elements, api_key: str, collection_name: str) -> Chroma:
    genai.configure(api_key=api_key)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    docs = [
        Document(
            page_content=el["text"], 
            metadata={
                "id": el["id"],
                "page": el["page"],
                "doc": el["doc"],
            }
        ) for el in elements
    ]
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=".chroma_db"
    )
    return vectorstore.as_retriever(search_kwargs={"k": 20})