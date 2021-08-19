# MIT License
#
# Copyright (c) [2020 - 2021] The yinyang authors
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

from src.base.Version import VERSION

header = (
    "toolname -- some description [version: "
    + VERSION + "]"
)

usage = """ toolname [options] solver_clis seed_file   [optionally, more seed files]
       toolname [options] solver_clis seed_folder [optionally, more seed folders]
       solver_clis := "solver_cli1;solver_cli2;...;solver_clik"
"""

short_description = """TODO: short description"""   # noqa: E501

long_description = """
TODO: long description
"""  # noqa: E501


options = """
options:
    -i <N>,  --iterations <N>
            iterations per seed (default: 300)
    -m <N>,  --modulo <N>
            the number of times the seed will be forwarded to the solvers
            For example, with 300 iterations and 2 as a modulo, 150 mutants
            per seed file will be passed to the SMT solvers. (default: 2)
    -l <path>, --logfolder <path>
            log folder (default: ./logs)
    -t <secs>, --timeout <secs>
            timeout per SMT solver call in seconds (default: 8)
    -b <path>, --bugsfolder <path>
            set bug folder (default: ./bugs)
    -s <path>, --scratchfolder <path>
            temp folder to dump mutants. (default: ./scratch)
    -c <file>, --config <file>
            set custom operator mutation config file
    -L <bytes>, --limit <bytes>
            file size limit on seed formula in bytes (default: 100000)
    -n, --no-log    disable logging
    -q, --quiet     do not print statistics and other output
    -v, --version   show version number and exit
    -h, --help      show this help message and exit
"""
