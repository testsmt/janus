#!/usr/bin/env sh
if [ -z "$1" ]; then
	source ./scripts/source-files.sh
	flake8 --max-line-length 88 $PYTHON_SOURCE_FILES
else
	flake8 --max-line-length 88 "$1"
fi
