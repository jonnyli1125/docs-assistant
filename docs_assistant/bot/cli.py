import os
import argparse
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from ..chain import get_retrieval_qa_chain, ask

def retrieval_qa_chain(db_dir: str) -> RetrievalQA:
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    lm = OpenAI()
    qa = RetrievalQA.from_chain_type(llm=lm, chain_type='stuff', retriever=db.as_retriever(), return_source_documents=True)
    return qa

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-dir')
    args = parser.parse_args()

    qa = get_retrieval_qa_chain(args.db_dir or os.environ['CHROMA_DB_DIR'])

    while True:
        query = input('question: ')
        answer = ask(qa, query)
        print(answer)

if __name__ == '__main__':
    main()
