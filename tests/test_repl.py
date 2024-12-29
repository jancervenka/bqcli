import pexpect
from src.bqcli import _format_result, mock_data


def test_repl():
    child = pexpect.spawn(".venv/bin/python -m tests.repl")

    child.expect("Happy BigQuerying.+")  # Wait for the prompt
    query = "select x, y, hello from test_table;"
    child.sendline(query)  # Send a command
    child.sendline(":exit")
    child.expect(pexpect.EOF)
    output = child.before.decode()
    child.close()

    assert "C 4.5  test" in output
    assert "Have a nice day!" in output


def test_format_result():
    output = _format_result(mock_data())
    expected_output = """\x1b[1m\x1b[92mx   y hello\x1b[0m
-----------
A 1.0  test
\x1b[94mB 2.3  test\x1b[0m
C 4.5  test"""

    assert expected_output == output
