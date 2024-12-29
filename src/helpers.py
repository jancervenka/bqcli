import sqlite3
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


def mock_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x": ["A", "B", "C"],
            "y": [1.0, 2.3, 4.5],
            "hello": ["test"] * 3
        }
    )


class MockBigQueryJob(bigquery.QueryJob):

    def __init__(self, result: pd.DataFrame):
        self._result = result

    def to_dataframe(self) -> pd.DataFrame:
        return self._result


class MockBigQueryClient(bigquery.Client):

    def __init__(self):
        self._conn = sqlite3.connect(':memory:')
        mock_data().to_sql("test_table", self._conn)

    def query(self, query: str) -> MockBigQueryJob:
        try:
            result = pd.read_sql(query, self._conn)
            return MockBigQueryJob(result)
        except Exception as e:
            message = "\n" + str(e)
            raise BadRequest(message=message, errors=[{"message": message}])

