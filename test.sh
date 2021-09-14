#!/usr/bin/env sh

python3 -m unittest tests/RunUnitTests.py &&
python3 tests/integration/detection/TestDetection.py &&
python3 tests/integration/detection/TestCrashes.py &&
python3 tests/integration/old-issues/TestIssueRediscovery.py &&
python3 tests/integration/misc/FileSizeLimit.py &&
python3 tests/integration/misc/NoSolvers.py &&
python3 tests/integration/misc/DirectoryMode.py
