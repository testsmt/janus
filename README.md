# Janus

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)

*Incompleteness Testing of SMT Solvers*

Janus is a testing tool for SMT solvers like
[Z3](https://www.github.com/z3prover/z3)
and
[CVC5](https://www.github.com/z3prover/z3),
focusing on incompleteness bugs.
It mutates SMT-LIB formulas in a satisfiability-preserving way, i.e. a (un)satisfiable seed formula produces mutants which are (un)satisfiable by construction.
The codebase is based on a fork of the SMT solver testing framework [YinYang](https://www.github.com/testsmt/yinyang),
developed as part of Mauro Bringolf's master thesis at ETH Zurich.
Since then, we have reported NUM_REPORTS of `unknown` formulas in Z3 and CVC5 of which NUM_FIXED have already been fixed.

## Incompleteness bugs


