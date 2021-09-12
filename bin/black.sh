#!/usr/bin/env sh
source ./bin/source-files.sh
black --skip-string-normalization $PYTHON_SOURCE_FILES
