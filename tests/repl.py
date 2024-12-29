from src.helpers import MockBigQueryClient
from src.bqcli import repl


if __name__ == "__main__":
    repl(bq_client=MockBigQueryClient())
