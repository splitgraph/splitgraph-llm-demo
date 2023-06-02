# based on: https://python.langchain.com/en/latest/modules/chains/examples/sqlite.html
import json
from typing import List, NamedTuple, Optional
import requests

from typing import TypedDict

# The constructor of the SQLDatabase base class calls SQLAlchemy's inspect()
# which fails on the DDN since some of the required introspection tables are
# not available.
# Creating a child class doesn't solve the issue, since the base constructor
# is still called, and for typing, we need an instance of SQLDatabase.
#
# The currents solution is to mock out the inspect() function to return a
# SplitgraphInspector instance

GQL_API_URL = "https://api.splitgraph.com/gql/cloud/unified/graphql"

GET_REPO_LIST_QUERY = """
query GetNamespaceRepos($namespace: String!) {
  namespace(namespace: $namespace) {
    namespace
    repositoriesByNamespace {
      nodes {
        repository
        namespace
        externalMetadata
        repoProfileByNamespaceAndRepository {
          readme
          metadata
        }
        latestTables {
          nodes {
            tableName
            tableSchema
          }
        }
      }
    }
  }
}
"""


class TableColumn(NamedTuple):
    ordinal: int
    name: str
    pg_type: str
    is_pk: bool
    comment: Optional[str] = None


class TableInfo(TypedDict):
    name: str
    schema: List[TableColumn]


class RepositoryInfo(TypedDict):
    namespace: str
    repository: str
    tables: List[TableInfo]
    readme: str


def get_repo_list(namespace: str) -> List[RepositoryInfo]:
    repo_results = requests.post(
        GQL_API_URL,
        headers={
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://api.splitgraph.com",
        },
        data=json.dumps(
            {
                "operationName": "GetNamespaceRepos",
                "query": GET_REPO_LIST_QUERY,
                "variables": {"namespace": namespace},
            }
        ),
    ).json()["data"]["namespace"]["repositoriesByNamespace"]["nodes"]
    return [
        {
            "namespace": namespace,
            "repository": repo["repository"],
            "readme": repo["repoProfileByNamespaceAndRepository"]["readme"],
            "tables": [
                {
                    "name": table["tableName"],
                    "schema": [TableColumn(*column) for column in table["tableSchema"]],
                }
                for table in repo["latestTables"]["nodes"]
            ],
        }
        for repo in repo_results
    ]
