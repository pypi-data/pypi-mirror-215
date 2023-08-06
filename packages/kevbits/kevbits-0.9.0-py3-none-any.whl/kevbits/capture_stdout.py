"""
Context manager to capture stdout:
https://stackoverflow.com/a/37423224/827548
"""

import sys
import io
import contextlib
from typing import Iterator


class Data:
    result: str = ""


@contextlib.contextmanager
def capture_stdout() -> Iterator[Data]:
    old = sys.stdout
    capturer = io.StringIO()
    data = Data()
    try:
        sys.stdout = capturer
        yield data
    finally:
        sys.stdout = old
        data.result = capturer.getvalue()


# Usage:
#     with capture_stdout() as capture:
#         print('Hello')
#         print('Goodbye')
#     assert capture.result == 'Hello\nGoodbye\n'
