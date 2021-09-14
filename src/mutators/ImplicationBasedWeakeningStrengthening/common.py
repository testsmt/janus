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

SAT = 1
UNSAT = -1
POSITIVE = 1
NEGATIVE = -1
WEAKENING = 1
STRENGTHENING = -1

from src.parsing.Ast import Const
import copy


def fresh_var(expression, not_in=None):
    if not not_in:
        not_in = set()
    fv = expression.free_variables().keys()
    counter = 0
    while f"x{counter}" in fv | not_in:
        counter += 1

    return f"x{counter}"


def convert_node_to_quantifier(node, quantifier, quantified_vars, body):
    # reset all defaults
    node.__init__()

    # set quantifier fields
    node.quantifier = quantifier
    node.quantified_vars = quantified_vars
    node.subterms = [body]
    node.type = "Bool"


def convert_node_to_single_subterm(node):
    node.__dict__ = node.subterms[0].__dict__.copy()


def convert_to_node(target, source):
    target.__dict__ = copy.deepcopy(source.__dict__.copy())
