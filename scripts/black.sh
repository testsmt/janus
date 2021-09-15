#!/usr/bin/env sh
source ./scripts/source-files.sh
black --skip-string-normalization $PYTHON_SOURCE_FILES
