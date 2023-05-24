import os
import argparse
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter
from ..chain import embed_docs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-dir')
    parser.add_argument('--url')
    parser.add_argument('--space-keys', nargs='+')
    parser.add_argument('--username')
    parser.add_argument('--api-key')
    args = parser.parse_args()

    loader = ConfluenceLoader(
        url=args.url or os.environ['CONFLUENCE_URL'],
        username=args.username or os.environ.get('CONFLUENCE_USERNAME'),
        api_key=args.api_key or os.environ.get('CONFLUENCE_API_KEY')
    )
    documents = []
    for space_key in args.space_keys or os.environ['CONFLUENCE_SPACE_KEYS'].split(','):
        print('loading docs from space:', space_key)
        documents += loader.load(space_key=space_key)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)

    embed_docs(args.db_dir or os.environ['CHROMA_DB_DIR'], documents)

if __name__ == '__main__':
    main()
