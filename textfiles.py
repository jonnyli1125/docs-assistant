import os
import argparse
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db_dir')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    texts = []
    for file in args.files:
        with open(file, 'r') as f:
            texts.append(f.read())
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.create_documents(texts, metadatas=[{'source': file} for file in args.files])
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=args.db_dir)
    db.persist()

if __name__ == '__main__':
    main()
