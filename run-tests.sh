#!/bin/bash

if [ -z "$JENKINS_URL" ]; then
    echo "Running outside Jenkins with"
    . venv/bin/activate
    python -m unittest  tests/runnner.py
else
    CURRENT="$PWD"
    SRC="$CURRENT/tests/runner.py"
    echo "Running inside Jenkins with SRC=$SRC"
    . venv/bin/activate
    python --version
    python -m unittest  tests/runnner.py
fi