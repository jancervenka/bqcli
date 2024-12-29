import os
import sys
import time
import readline
import warnings
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest

BOLD = "\033[1m"
ENDC = "\033[0m"
HEADER_COLOR = "\033[92m"
ROW_COLOR = "\033[94m"
WHITE = "\033[97m"


def _init_history() -> None:
    history_file = os.path.join(os.path.expanduser("~"), ".bqcli_history")
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        with open(history_file, 'wb') as f:
            f.close()


def _evaluate_query(query: str, bq_client: bigquery.Client) -> pd.DataFrame | None:
    print(f"{WHITE}Evaluating the query...{ENDC}", end=" ", flush=True)
    try:
        t_0 = time.time()
        result = bq_client.query(query).to_dataframe()
        t_1 = time.time()
        message = f"{WHITE}took {(t_1 - t_0):.2f} seconds to finish.{ENDC}\n"
    except BadRequest as exc:
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


def _read_query() -> str:
    query = ""
    while True:
        try:
            segment = input(">" if not query else "")
            segment = segment if segment.endswith(";") else segment + " "            
            query += segment
            if query and query[-1] == ";":
                break

        except KeyboardInterrupt:
            sys.exit()
    return query


def repl() -> None:
    # _init_history()
    warnings.simplefilter("ignore", UserWarning)
    bq_client = bigquery.Client()
    print("Happy BigQuerying!")
    while True:
        query = _read_query()
        result = _evaluate_query(query, bq_client)
        if result is not None:
            print(_format_result(result))


if __name__ == "__main__":
    repl()
