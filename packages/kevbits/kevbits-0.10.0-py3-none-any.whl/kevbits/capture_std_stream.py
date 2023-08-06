"""
Context manager to capture stdout/stderr:
https://stackoverflow.com/a/37423224/827548
"""

import sys
import io
import contextlib
from typing import Iterator, Literal


class Data:
    result: str = ""


@contextlib.contextmanager
def capture_stream(stream: Literal["stdout", "stderr"]) -> Iterator[Data]:
    assert stream in ["stdout", "stderr"]
    old = getattr(sys, stream)
    capturer = io.StringIO()
    data = Data()
    try:
        setattr(sys, stream, capturer)
        yield data
    finally:
        setattr(sys, stream, old)
        data.result = capturer.getvalue()


# Usage:
#     with capture_stream("stdout") as capture:
#         print("Hello")
#         print("Goodbye")
#     assert capture.result == "Hello\nGoodbye\n"
