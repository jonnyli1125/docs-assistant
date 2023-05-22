import argparse
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import LlamaCppEmbeddings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db_dir')
    parser.add_argument('url')
    parser.add_argument('space_keys', nargs='+')
    parser.add_argument('--username')
    parser.add_argument('--api-key')
    args = parser.parse_args()

    loader = ConfluenceLoader(url=args.url, username=args.username, api_key=args.api_key)
    documents = []
    for space_key in args.space_keys:
        documents += loader.load(space_key=space_key)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    embeddings = LlamaCppEmbeddings(model_path='./models/7B/ggml-model-q4_0.bin')
    db = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=args.db_dir)
    db.persist()

if __name__ == '__main__':
    main()
