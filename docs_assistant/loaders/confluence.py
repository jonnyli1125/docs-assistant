import os
import argparse
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter
from ..chain import embed_docs

from requests import HTTPError
from atlassian.errors import ApiValueError
from atlassian.confluence import Confluence

# langchain source is broken here so we have to override the cql() function
# original function copied from confluence python package source
# https://github.com/atlassian-api/atlassian-python-api/blob/6580cf39c04bedf2a5d656385ff590423eb3370f/atlassian/confluence.py#L2379
def cql_fix(
    self,
    cql,
    start=0,
    limit=None,
    expand=None,
    include_archived_spaces=None,
    excerpt=None,
):
    """
    Get results from cql search result with all related fields
    Search for entities in Confluence using the Confluence Query Language (CQL)
    :param cql:
    :param start: OPTIONAL: The start point of the collection to return. Default: 0.
    :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                    fixed system limits. Default by built-in method: 25
    :param excerpt: the excerpt strategy to apply to the result, one of : indexed, highlight, none.
                    This defaults to highlight
    :param expand: OPTIONAL: the properties to expand on the search result,
                    this may cause database requests for some properties
    :param include_archived_spaces: OPTIONAL: whether to include content in archived spaces in the result,
                                this defaults to false
    :return:
    """
    params = {}
    if start is not None:
        params["start"] = int(start)
    if limit is not None:
        params["limit"] = int(limit)
    if cql is not None:
        params["cql"] = cql
    if expand is not None:
        params["expand"] = expand
    if include_archived_spaces is not None:
        params["includeArchivedSpaces"] = include_archived_spaces
    if excerpt is not None:
        params["excerpt"] = excerpt

    try:
        # fix: use rest/api/content/search here instead
        # for some reason rest/api/search doesn't accept expand, but rest/api/content/search does
        response = self.get("rest/api/content/search", params=params)
    except HTTPError as e:
        if e.response.status_code == 400:
            raise ApiValueError("The query cannot be parsed", reason=e)

        raise

    # fix: return sub-dict at result key for langchain ConfluenceLoader to parse this properly
    return response['results']

Confluence.cql = cql_fix

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cql')
    parser.add_argument('--db-dir')
    parser.add_argument('--url')
    parser.add_argument('--username')
    parser.add_argument('--api-key')
    args = parser.parse_args()

    loader = ConfluenceLoader(
        url=args.url or os.environ['CONFLUENCE_URL'],
        username=args.username or os.environ.get('CONFLUENCE_USERNAME'),
        api_key=args.api_key or os.environ.get('CONFLUENCE_API_KEY')
    )
    documents = loader.load(cql=args.cql)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)

    embed_docs(args.db_dir or os.environ['CHROMA_DB_DIR'], documents)

if __name__ == '__main__':
    main()
