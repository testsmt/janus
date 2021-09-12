#!/usr/bin/env sh
source ./bin/source-files.sh
flake8 --max-line-length 88 $PYTHON_SOURCE_FILES
