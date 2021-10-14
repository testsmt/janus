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

from pathlib import Path
import sys

#path = Path(__file__)
#rootpath = str(path.parent.absolute().parent)
#sys.path.append(rootpath)
sys.path.append("./")

from src.parsing.Parse import parse_file
from src.parsing.Typechecker import typecheck, TypeCheckError
from src.mutators.ImplicationBasedWeakeningStrengthening.ImplicationBasedWeakeningStrengthening import ImplicationBasedWeakeningStrengthening
import io
import subprocess
from contextlib import redirect_stdout

# TODO this is shared with test_imp_based.py
class MockArgs:
    def __init__(self, oracle, rule_set):
        self.iterations = 1
        self.oracle = oracle
        self.rule_set = rule_set


if not len(sys.argv) == 5:
    print("Wrong number of arguments. Usage: check-implication.py SOLVER_TIMEOUT SOLVER RULE_NAME KNOWN_FILE")
    exit(1)

[_, solver_timeout, solver, rule_name, known_file] = sys.argv

known_result, known_err = subprocess.Popen( [*solver.split(" "), known_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(solver_timeout)

if not known_err.decode('ascii').strip() == "": # or not new_err.decode('ascii').strip() == "":
    print("Solver error on known file")
    exit(1)

if not known_result.decode('ascii').strip() in ['sat', 'unsat']:
    print("Solver did not decide known file")
    exit(1)

oracle = known_result.decode('ascii').strip()

UNKNOWN_FILE=f'{known_file}.unknown'

f = io.StringIO()
with redirect_stdout(f):
    known, glbls = parse_file(known_file)

try:
    typecheck(known, glbls)
except Exception as e:
    print(f.getvalue())
    print(e)
    exit(2)

args = MockArgs(oracle, rule_set=rule_name)

gen = ImplicationBasedWeakeningStrengthening(known, glbls, args)

rule = gen.rules[0]

formulas = gen.get_formulas(known)

candidates = []

for f in formulas:
    candidates.extend(gen.get_candidates(f, rule, 1))

for to_replace, parity in candidates:
    tmp = to_replace.__dict__.copy()
    rule.apply(to_replace, parity * gen.oracle)
    with open(UNKNOWN_FILE, "w") as uf:
        uf.write(str(known))
    unknown_result = subprocess.getoutput(f"{solver} {UNKNOWN_FILE}")
    if unknown_result == "unknown":
        print("Successfully reproduced unknown.")
        exit(0)
    else:
        to_replace.__dict__ = tmp

print("Input is not a regression incompleteness.")
exit(3)
