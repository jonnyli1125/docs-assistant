import argparse
from langchain.text_splitter import CharacterTextSplitter
from ..chain import embed_docs

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

    embed_docs(args.db_dir, documents)

if __name__ == '__main__':
    main()
