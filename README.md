# Installing dependencies

## PostgreSQL database with the pgvector extension installed
This demo needs a PostgreSQL database with [`pgvector`](https://github.com/pgvector/pgvector) installed.
Many package managers like Homebrew and `apt` have pre-packaged version of `pgvector`.

Don't forget to activate the extension for the database used in the demo:
```sql
CREATE EXTENSION vector;
```

## Installing python dependencies

```bash
# create venv
python3 -m venv venv
# activate venv
. venv/bin/activate
# install deps
pip install langchain openai pgvector tiktoken unstructured psycopg2 tabulate
```

# Env vars

The code in the demo uses the following env vars:

- `OPENAI_API_KEY`, eg: `sk-F9Ci...2J`
- `PG_CONN_STR_LOCAL`, eg: `postgresql://myuser:***@localhost:5432/mydb`
- `PG_CONN_STR_DDN`, eg: `postgresql://4ce270ae3cdd4440aed5d105869949c5:***@data.splitgraph.com:5432/ddn`

# Usage

```bash
# first, index the repositories in namespace 'cityofchicago'
python3 index_repos.py cityofchicago
# query the repositories in the cityofchicago namespace
python query.py cityofchicago 'How many restaurants are there in Chicago?'
```
