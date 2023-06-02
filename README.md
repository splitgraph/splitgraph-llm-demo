# Installing dependencies

- pgvector

```bash
pip install langchain
pip install openai
pip install faiss-cpu
pip install pgvector
pip install tiktoken
pip install unstructured
pip install tabulate
```

# Getting list of REPOS
```bash
curl 'https://api.splitgraph.com/gql/cloud/unified/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.splitgraph.com' --data-binary '{"query":"query {\n  namespace(namespace: \"cityofchicago\") {\n    namespace\n    repositoriesByNamespace {\n      nodes {\n        repository\n        namespace\n        externalMetadata\n        repoProfileByNamespaceAndRepository {\n          readme\n          metadata\n        }\n        latestTables {\n          nodes {\n            tableName\n            tableSchema\n          }\n        }\n      }\n    }\n  }\n}\n"}' --compressed > cityofchicago-repos.json
```

# Env vars

- `OPENAI_API_KEY`
- `PG_CONN_STR`
