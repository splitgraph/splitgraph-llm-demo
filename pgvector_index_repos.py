# from: https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/pgvector.html

from io import StringIO
from typing import List, Tuple
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
# from: https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/markdown.html
from langchain.document_loaders import UnstructuredFileIOLoader
from langchain.docstore.document import Document
import langchain.vectorstores.pgvector
import json
from unstructured.__version__ import __version__ as __unstructured_version__
from unstructured.partition.md import partition_md
import os

REPOSITORY_DESCRIPTION = """
# Repository: {namespace}/{repository}

## description
{readme}

## tables
{tables}
""".lstrip()

TABLE_DESCRIPTION="""
### {tablename}
The table named {tablename} includes the following columns:
{columns}
""".lstrip()

def column_info_to_markdown(column_info):
    return f"* {column_info[1]} (type {column_info[2]}) {column_info[4]}"

def table_info_to_markdown(table_info):
    return TABLE_DESCRIPTION.format(
        tablename=table_info["tableName"],
        columns="\n".join([column_info_to_markdown(c) for c in table_info["tableSchema"]])
    )

def repository_info_to_markdown(repository_info):
    result = REPOSITORY_DESCRIPTION.format(
        namespace=repository_info['namespace'],
        repository=repository_info['repository'],
        readme=repository_info['repoProfileByNamespaceAndRepository']['readme'],
        tables="\n\n".join([table_info_to_markdown(table) for table in repository_info['latestTables']['nodes']])
    )
    return result

all_repos = json.loads(open("cityofchicago-repos.json").read())["data"]["namespace"]["repositoriesByNamespace"]["nodes"]
repo_mds = dict([(f"{r['namespace']}/{r['repository']}", repository_info_to_markdown(r)) for r in all_repos])

# Based on UnstructuredMarkdownLoader
class UnstructuredMarkdownIOLoader(UnstructuredFileIOLoader):
    """Loader that uses unstructured to load markdown files."""

    def _get_elements(self) -> List:

        # NOTE(MthwRobinson) - enables the loader to work when you're using pre-release
        # versions of unstructured like 0.4.17-dev1
        _unstructured_version = __unstructured_version__.split("-")[0]
        unstructured_version = tuple([int(x) for x in _unstructured_version.split(".")])

        if unstructured_version < (0, 4, 16):
            raise ValueError(
                f"You are on unstructured version {__unstructured_version__}. "
                "Partitioning markdown files is only supported in unstructured>=0.4.16."
            )

        return partition_md(file=self.file, **self.unstructured_kwargs)

def save_embedding(name, md):
    loader = UnstructuredMarkdownIOLoader(StringIO(md))
    documents = loader.load()
    # add metadata to documents
    for d in documents:
        d.metadata['repository'] = name
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # The PGVector Module will try to create a table with the name of the collection. So, make sure that the collection name is unique and the user has the
    # permission to create a table.

    langchain.vectorstores.pgvector.PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name="cityofchicago",
        connection_string=os.environ['PG_CONN_STR'],
    )
    print(f"saved embeddings for {len(docs)} document fragments in {name}")

    #query = "Are gonorrhea cases increasing in the city of Chicago?"
    #docs_with_score: List[Tuple[Document, float]] = db.similarity_search_with_score(query)

    #for doc, score in docs_with_score:
    #    print("-" * 80)
    #    print("Score: ", score)
    #    print(doc.page_content)
    #    print("-" * 80)

[save_embedding(name, md) for (name, md) in repo_mds.items()]
