import re 
from typing import List, Dict, Tuple
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import tiktoken
from prompt import main_prompt


def get_final_sources_used(response, docs):
    response = response.replace(",", "")
    lines = response.splitlines()
    source_indices = set()
    final_sources = []

    for line in lines:
        numbers = re.findall(r'\d+', line)
        for n in numbers:
            source_indices.add(int(n))

    for i in sorted(source_indices):
        if 0 < i <= len(docs): 
            doc = docs[i - 1]
            doc['id'] = str(i)
            final_sources.append(doc)

    return final_sources



def get_context(docs: List[Dict]) -> str:
    """Construit le contexte à partir des documents en respectant la limite de tokens"""
    encoder = tiktoken.get_encoding("cl100k_base")
    context = ""
    max_context_size = 12288  
    for idx, doc in enumerate(docs):
        doc_text = f"{idx + 1}. {doc['text']}, \n Number {idx + 1}, \nSource: {doc['doc_name']}, Page {doc['page']}\n\n"
        new_context = context + doc_text
        if len(encoder.encode(new_context)) < max_context_size:
            context = new_context
        else:
            tokens = encoder.encode(doc['text'])
            remaining_tokens = max_context_size - len(encoder.encode(context))
            truncated_text = encoder.decode(tokens[:remaining_tokens]) + " [TRUNCATED]"
            context += f"{idx + 1}. {truncated_text}\nSource: {doc['doc_name']}, Page {doc['page']}\n\n"
            break
    return context

def get_response_with_sources(retriever, query: str, api_key: str) -> tuple[str, List[Document]]:
    """Retourne la réponse générée et les documents sources pertinents"""
    sources = retriever.get_relevant_documents(query)
    docs_for_context = []
    for i, doc in enumerate(sources):
        docs_for_context.append({
            'text': doc.page_content,
            'doc_name': doc.metadata.get('doc', 'Unknown'),
            'page': doc.metadata.get('page', 'N/A')
        })
    context_str = get_context(docs_for_context)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=api_key,
        temperature=0.3,
        max_output_tokens=2048
    )
    chain = (
        {"context": lambda x: context_str, "question": lambda x: x["question"]}
        | main_prompt
        | llm
        | StrOutputParser()
    )
    response = chain.invoke({"question": query})
    docs_sources = [{
        "id": doc.metadata.get("id", "Unknown"),
        "page": doc.metadata.get("page", "N/A"),
        "doc_name": doc.metadata.get("doc", "Unknown"),
        "text": doc.page_content
    } for doc in sources
    ]
    final_sources = get_final_sources_used(response, docs_sources)
    return response, final_sources