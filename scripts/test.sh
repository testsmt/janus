#!/usr/bin/env sh

set -e

./scripts/black-check.sh
python3 -m unittest tests/RunUnitTests.py

echo python3 tests/integration/detection/TestDetection.py
python3 tests/integration/detection/TestDetection.py

echo python3 tests/integration/detection/TestCrashes.py
python3 tests/integration/detection/TestCrashes.py

echo python3 tests/integration/old-issues/TestIssueRediscovery.py
python3 tests/integration/old-issues/TestIssueRediscovery.py

echo python3 tests/integration/misc/FileSizeLimit.py
python3 tests/integration/misc/FileSizeLimit.py

echo python3 tests/integration/misc/NoSolvers.py
python3 tests/integration/misc/NoSolvers.py

echo python3 tests/integration/misc/DirectoryMode.py
python3 tests/integration/misc/DirectoryMode.py
