from flask import Request
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr


def run_code(request: Request):
    # capture stdout and stderr

    stdout = StringIO()
    stderr = StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        # run the code passed in the request
        exec(request.json["code"])

    stdout_value = stdout.getvalue()
    stderr_value = stderr.getvalue()
    return {
        "stdout": stdout_value,
        "stderr": stderr_value,
    }
