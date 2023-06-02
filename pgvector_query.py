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

embeddings = OpenAIEmbeddings()

store = langchain.vectorstores.pgvector.PGVector(
    embedding_function=embeddings,
    collection_name="cityofchicago",
    connection_string="postgresql://neumark:37IP_C-9L0a@localhost:5432/tunneltestdb",
    distance_strategy=langchain.vectorstores.pgvector.DistanceStrategy.COSINE
)
retriever = store.as_retriever()
docs = retriever.get_relevant_documents("Are gonorrhea cases increasing in the city of Chicago?")
import pprint
pprint.pprint(docs)
