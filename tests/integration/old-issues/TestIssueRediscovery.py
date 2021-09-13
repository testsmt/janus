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

import os
import sys
import subprocess
from pathlib import Path

python = sys.executable

TIME_LIMIT = 180


def run_janus(first_config, second_config, directory, opts):
    timeout = "timeout --signal=INT " + str(timeout_limit) + " "
    cmd = (
        timeout
        + python
        + " bin/janus "
        + '"'
        + first_config
        + '" '
        + opts
        + " "
        + directory
    )
    generated_seeds = 0
    used_seeds = 0
    ignored_issues = 0
    return output, cmd


def get_z3_4_8_10():
    if not Path("tmp/z3-4.8.10/bin/z3").is_file():
        z3_link = "https://github.com/Z3Prover/z3/releases/download/z3-4.8.10/z3-4.8.10-x64-ubuntu-18.04.zip"
        os.system("wget " + z3_link)
        os.system("unzip z3-4.8.10-x64-ubuntu-18.04.zip -d tmp/")
    return os.path.abspath("tmp/z3-4.8.10-x64-ubuntu-18.04/bin/z3")


def cleanup():
    subprocess.getoutput("rm -rf z3*")


# cleanup()
os.system("mkdir -p tmp/")
z3 = get_z3_4_8_10()
first_config = z3
seeds = str(os.path.dirname(os.path.realpath(__file__))) + "/seeds"

# https://github.com/Z3Prover/z3/issues/5491
out = subprocess.getoutput(f"./bin/janus  {z3} {seeds}/z3-5491-seed.smt2")
if "Detected implication incompleteness." not in out:
    exit(1)

cleanup()
