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

from src.parsing.Ast import Expr
import copy


def APP(re, s):
    if re.op == "str.to_re":
        re.subterms = [Expr("str.++", [re.subterms[0], s], type="String")]
    elif re.op in ["re.union", "re.inter", "re.diff", "re.opt"]:
        for t in re.subterms:
            APP(t, s)
    elif re.op == "re.++":
        APP(re.subterms[-1], s)
    else:
        """CASES
        re.+
        re.*
        re.comp
        re.^
        re.loop
        """
        re_itself = copy.deepcopy(re)
        re.op = "re.++"
        re.subterms = [re_itself, Expr("str.to_re", [s], type="RegLan")]
