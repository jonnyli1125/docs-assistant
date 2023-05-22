from typing import List
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings

def get_retrieval_qa_chain(db_dir: str) -> RetrievalQA:
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    lm = OpenAI()
    qa = RetrievalQA.from_chain_type(llm=lm, chain_type='stuff', retriever=db.as_retriever(), return_source_documents=True)
    return qa

def embed_docs(db_dir: str, documents: List[Document]) -> Chroma:
    embeddings = OpenAIEmbeddings()
    db = Chroma(embedding_function=embeddings, persist_directory=db_dir)
    db.add_documents(documents)
    db.persist()
    return db
