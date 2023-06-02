from .repo_info import RepositoryInfo, TableColumn, TableInfo


REPOSITORY_DESCRIPTION = """
# Repository: {namespace}/{repository}

## description
{readme}

## tables
{tables}
""".lstrip()

TABLE_HEADER = """
### {tablename}
""".lstrip()

TABLE_DESCRIPTION = """
The table named "{namespace}/{repository}"."{tablename}" includes the following columns:
{columns}
""".lstrip()


def column_info_to_markdown(column_info: TableColumn) -> str:
    return f"* {column_info[1]} (type {column_info[2]}) {column_info[4]}"


def table_info_to_markdown(
    namespace: str, repository: str, table_info: TableInfo, emit_header=False
) -> str:
    return (
        TABLE_HEADER.format(tablename=table_info["name"])
        if emit_header
        else ""
        + TABLE_DESCRIPTION.format(
            namespace=namespace,
            repository=repository,
            tablename=table_info["name"],
            columns="\n".join(
                [column_info_to_markdown(c) for c in table_info["schema"]]
            ),
        )
    )


def repository_info_to_markdown(repo_info: RepositoryInfo) -> str:
    result = REPOSITORY_DESCRIPTION.format(
        namespace=repo_info["namespace"],
        repository=repo_info["repository"],
        readme=repo_info["readme"],
        tables="\n\n".join(
            [
                table_info_to_markdown(
                    repo_info["namespace"],
                    repo_info["repository"],
                    table,
                    emit_header=True,
                )
                for table in repo_info["tables"]
            ]
        ),
    )
    return result
