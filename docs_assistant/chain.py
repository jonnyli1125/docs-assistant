from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings

def get_retrieval_qa_chain(db_dir: str) -> RetrievalQA:
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    #db._similarity_search_with_relevance_scores = db.similarity_search_with_score  # missing method in langchain source?
    #ret = db.as_retriever(search_type='similarity_score_threshold', search_kwargs={'score_threshold': 0.3})
    ret = db.as_retriever()
    lm = OpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=lm, chain_type='stuff', retriever=ret, return_source_documents=True)
    return qa

def ask(qa: RetrievalQA, query: str) -> str:
    result = qa({'query': query})
    answer = result['result']
    sources = sorted({doc.metadata['source'] for doc in result['source_documents']})
    if 'i don\'t know' in answer.lower() or not sources:
        return answer
    sources_formatted = 'Relevant documents:\n' + '\n'.join(f'- {source}' for source in sources)
    return f'{answer}\n\n{sources_formatted}'

def embed_docs(db_dir: str, documents: list[Document]) -> Chroma:
    embeddings = OpenAIEmbeddings()
    db = Chroma(embedding_function=embeddings, persist_directory=db_dir)
    db.add_documents(documents)
    db.persist()
    return db
