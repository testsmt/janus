#! /bin/bash
source ./bin/source-files.sh
black --skip-string-normalization --check $PYTHON_SOURCE_FILES
