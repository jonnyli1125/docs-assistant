import argparse
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db_dir')
    args = parser.parse_args()

    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=args.db_dir, embedding_function=embeddings)
    lm = OpenAI()
    qa = RetrievalQA.from_chain_type(llm=lm, chain_type='stuff', retriever=db.as_retriever(), return_source_documents=True)

    while True:
        query = input()
        result = qa({'query': query})
        print(result['result'])
        print([doc.metadata for doc in result['source_documents']])

if __name__ == '__main__':
    main()
