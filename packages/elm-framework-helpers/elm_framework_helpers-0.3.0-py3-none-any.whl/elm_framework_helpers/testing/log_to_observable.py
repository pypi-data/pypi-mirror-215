from typing import TextIO
from reactivex.testing import ReactiveTest
import orjson

import logging

def log_file_to_observable(filename: str, first_line_timestamp: int = 0, start_line: int = 0, end_line: int = None) -> list:
    with open(filename, 'r') as f:
        return log_to_observable(f, first_line_timestamp, start_line, end_line)

def log_to_observable(f: TextIO, first_line_timestamp: int = 0, start_line: int = 0, end_line: int = None) -> list:
    if not hasattr(f, 'readlines') or not callable(f.readlines):
        raise ValueError('Parameter f must have a readlines() method')

    if not isinstance(first_line_timestamp, int) or first_line_timestamp < 0:
        raise ValueError('Parameter first_line_timestamp must be a non-negative integer')

    if not isinstance(start_line, int) or start_line < 0:
        raise ValueError('Parameter start_line must be a non-negative integer')

    if end_line is not None and (not isinstance(end_line, int) or end_line <= start_line):
        raise ValueError('Parameter end_line must be a positive integer greater than start_line')

    messages = []

    # Read the log file lines
    lines = f.readlines()
    if end_line is None:
        end_line = len(lines)

    for i, line in enumerate(lines[start_line:end_line]):
        # Parse the timestamp and message content from the log line
        parts = line.strip().split(' | ')
        timestamp = int(parts[0])
        if i == 0:
            first_line_timestamp += timestamp
        content = orjson.loads(parts[1])

        # Calculate the relative timestamp based on the first line timestamp
        relative_timestamp = timestamp - first_line_timestamp

        # Create a new message using the ReactiveTest.on_next method
        message = ReactiveTest.on_next(relative_timestamp, content)
        messages.append(message)

    return messages



def setup_socket_logger(logger_name: str, handler: logging.Handler) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s%(msecs)03d | %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger