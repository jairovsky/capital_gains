import sys
from typing import TextIO
import io
from capital_gains.solution import solve


# https://docs.python.org/3/library/os.html#os.linesep
# Do not use os.linesep as a line terminator when writing files
# opened in text mode (the default);
# use a single '\n' instead, on all platforms.
LINE_TERMINATOR = '\n'

def run(reader: TextIO) -> TextIO:

    result = io.StringIO(newline=LINE_TERMINATOR)

    for line in reader.readlines():
        result.write(solve(line) + LINE_TERMINATOR)
    
    result.seek(0)

    return result