#!/usr/bin/env python3

# MIT License
#
# Copyright (c) [2020 - 2021] Mauro Bringolf and Dominik Winterer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
