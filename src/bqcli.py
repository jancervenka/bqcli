import sys
import time
import warnings
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest, NotFound

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer

BOLD = "\033[1m"
ENDC = "\033[0m"
HEADER_COLOR = "\033[92m"
ROW_COLOR = "\033[94m"
WHITE = "\033[97m"
EXIT_COMMANDS = (":exit", ":quit")


def _add_query_to_history(session: PromptSession, query: str) -> None:
    session.history.append_string(query)


def _evaluate_query(query: str, bq_client: bigquery.Client) -> pd.DataFrame | None:
    print(f"{WHITE}Evaluating the query...{ENDC}", end=" ", flush=True)
    try:
        t_0 = time.time()
        result = bq_client.query(query).to_dataframe()
        t_1 = time.time()
        message = f"{WHITE}took {(t_1 - t_0):.2f} seconds to finish.{ENDC}\n"
    except (BadRequest, NotFound) as exc:
        result = None
        error_message = exc.errors[0]["message"]
        message = f"{WHITE}error: {error_message}.{ENDC}\n"

    print(message)
    return result


def _format_row(row_number: int, row: str) -> str:
    if row_number == 0:
        return BOLD + HEADER_COLOR + row + ENDC + "\n" + "-" * len(row)

    if row_number % 2 == 0:
        return ROW_COLOR + row + ENDC

    return row


def _format_result(result: pd.DataFrame) -> str:

    rows = result.to_string(index=False, justify="center").split("\n")

    return "\n".join(
        _format_row(row_number, row) for row_number, row in enumerate(rows)
    )


def _exit() -> None:
    print("Have a nice day!")
    sys.exit()


def _read_query(session: PromptSession) -> str:
    query = ""
    while True:
        try:
            segment = session.prompt(">" if not query else "", lexer=PygmentsLexer(SqlLexer))
            if segment in EXIT_COMMANDS:
                _exit()
            segment = segment if segment.endswith(";") else segment + " "            
            query += segment
            if query and query[-1] == ";":
                break

        except KeyboardInterrupt:
            _exit()
    return query


def repl(bq_client: bigquery.Client | None) -> None:
    warnings.simplefilter("ignore", UserWarning)
    bq_client = bq_client if bq_client is not None else bigquery.Client()
    session = PromptSession()
    print("Happy BigQuerying!")
    while True:
        query = _read_query(session)
        _add_query_to_history(session, query)
        result = _evaluate_query(query, bq_client)
        if result is not None:
            print(_format_result(result))


if __name__ == "__main__":
    repl()
