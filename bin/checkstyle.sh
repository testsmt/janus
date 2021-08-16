#! /bin/bash
flake8  --exclude "*SMTLIBv2*,*runtests.py*,__init__.py" src tests config bin/toolname --select=E --ignore=E402 --statistics 
