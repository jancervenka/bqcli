from src.bqcli import repl, MockBigQueryClient


if __name__ == "__main__":
    repl(bq_client=MockBigQueryClient())
