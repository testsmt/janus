#!/usr/bin/env python3

import sys
import subprocess

if not len(sys.argv) == 5:
    print("Wrong number of arguments. Usage: check-regression.py SOLVER_TIMEOUT OLD_SOLVER_CMD NEW_SOLVER_CMD REGRESSION_FILE")
    exit(1)

[_, solver_timeout, old_solver, new_solver, regression_file] = sys.argv

old_result, old_err = subprocess.Popen( [*old_solver.split(" "), regression_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(solver_timeout)
new_result, new_err = subprocess.Popen([*new_solver.split(" "), regression_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(solver_timeout)

if not old_err.decode('ascii').strip() == "" or not new_err.decode('ascii').strip() == "":
    print("Unexpected errors returned by solvers")
    exit(2)


if old_result.decode('ascii').strip() in ["sat", "unsat"] and new_result.decode('ascii').strip() == "unknown":
    print("Input is a regression incompleteness.")
    exit(0)

print("Input is not a regression incompleteness.")
exit(3)
