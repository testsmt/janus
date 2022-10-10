#! /bin/bash
source ./scripts/source-files.sh
black --skip-string-normalization --verbose --check $PYTHON_SOURCE_FILES
