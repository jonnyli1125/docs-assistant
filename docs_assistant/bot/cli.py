import os
import argparse
from ..chain import get_retrieval_qa_chain, ask

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
