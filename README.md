# Janus
<p align="center"><a><img width="160" alt="portfolio_view" align="center" src="misc/logo.png"></a></p>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)

Janus is a testing tool for SMT solvers like
[Z3](https://www.github.com/z3prover/z3)
and
[CVC5](https://www.github.com/z3prover/z3),
focusing on *incompleteness bugs*.
It mutates SMT-LIB formulas in a satisfiability-preserving way, i.e. given a (un)satisfiable seed formula it produces mutated formulas which are (un)satisfiable by construction.
The codebase is based on a fork of the SMT solver testing framework [YinYang](https://www.github.com/testsmt/yinyang),
developed as part of Mauro Bringolf's master thesis with the [AST Lab](https://ast.ethz.ch/) at ETH Zurich.

## Usage

```
bin/janus "z3" -o sat examples/phi1.smt2
```
