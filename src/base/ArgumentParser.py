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

import argparse

from src.base.Exitcodes import ERR_USAGE
from src.base.Version import VERSION, COMMIT


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("usage:" + self.usage, flush=True)
        self.exit(
            ERR_USAGE,
            "error: %s\nFor a listing of options, use %s --help.\n"
            % (message, self.prog),
        )


def add_args(parser, rootpath, current_dir):
    parser.add_argument(
        "SOLVER_CLIS",
        metavar="solver_clis",
    )
    parser.add_argument(
        "PATH_TO_SEEDS",
        nargs="+",
        metavar="seed_file/seed_folder",
    )
    parser.add_argument(
        "-l",
        "--logfolder",
        metavar="path_path_to_folder",
        default=current_dir + "/logs",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=8,
        metavar="secs",
        type=int,
    )
    parser.add_argument(
        "-b",
        "--bugsfolder",
        metavar="path_to_folder",
        default=current_dir + "/bugs",
    )
    parser.add_argument(
        "-s",
        "--scratchfolder",
        metavar="path_to_folder",
        default=current_dir + "/scratch",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--no-log",
        action="store_true",
    )
    parser.add_argument(
        "-L",
        "--file-size-limit",
        metavar="num_bytes",
        default=100000,
    )
    parser.add_argument(
        "-i", "--iterations",
        default=100,
    )
    parser.add_argument(
        "-o",
        "--oracle",
        default="sat",
        metavar="{sat,unsat}",
        type=str,
    )
    parser.add_argument(
        "-ss", "--step-size",
        type=int,
        default=1,
        help="[impbased] Target number of strengthening/weakening rules to apply in a single mutation step (default: 1)",
    )
    parser.add_argument(
        "-wl", "--walk-length",
        type=int,
        default=1,
        help="[impbased] Number of incremental steps before restarting on the seed (default: 1). \
        This corresponds to a fully non-incremental solver and a fully incremental generator is obtained by setting \
        '--walk-length' equal to '--iterations'.",
    )
    parser.add_argument(
        "-cr", "--completeness-regressions",
        type=str,
        default="",
        help="[impbased] Pass a single solver command to search for completeness regressions against. (default: 1).\
              This disables soundness testing and instead searches for completeness regressions in any configured solver\
              against the solver passed here.\
              A standard setup is to use the latest release of a solver here and configure trunk version(s) as solver(s)\
              to be tested.",
    )
    parser.add_argument(
        "-rs", "--rule-set",
        default=None,
        help="Restrict rule set to a fixed subset (default: None)",
    )


def build_toolname_parser(rootpath, current_dir, usage):
    parser = ArgumentParser(
        description="",
        usage=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    add_args(parser, current_dir, rootpath)
    
    return parser
