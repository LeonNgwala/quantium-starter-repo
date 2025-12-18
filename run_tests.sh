#!/bin/bash

# Activate the project virtual environment
source ./.venv/bin/activate

# Execute the test suite
./.venv/bin/pytest

# Pytest returns exit code 0 if all tests passed, or non-zero if something went wrong.
# The script will naturally inherit this exit code.