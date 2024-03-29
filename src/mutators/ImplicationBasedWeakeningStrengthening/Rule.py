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

import copy
import random
import string

from src.parsing.Ast import StringConst, Const, Expr


class Rule:
    def __init__(self, formula_pool=None):
        if not formula_pool:
            self.formula_pool = []
        else:
            self.formula_pool = copy.deepcopy(formula_pool)

        self.glbls = None

        self.random_value_generator = {
            func[4:]: getattr(Rule, func)(self)
            for func in dir(Rule)
            if callable(getattr(Rule, func)) and func.startswith("GEN_")
        }
        self.random_instantiatable_sorts = self.random_value_generator.keys()

    def is_random_instantiatable(self, sort):
        return sort in self.random_instantiatable_sorts

    def random_value_node(self, qsort, qvar=None):
        candidates = self.get_candidates(qsort, qvar)
        candidates += [Const(x, type=s) for x, s in self.glbls.items() if s == qsort]
        if len(candidates) > 0:
            return random.choice(candidates)
        else:
            return self.random_value_generator[qsort]()

    def get_candidates(self, sort, unfree_variable):

        res = []

        def go(term):
            free_variable_names = term.free_variables().keys()
            if (
                term.type == sort
                and (not unfree_variable or unfree_variable not in free_variable_names)
                and set(free_variable_names).issubset(set((self.glbls.keys())))
            ):
                res.append(term)
            if term.subterms:
                for t in term.subterms:
                    go(t)

        for f in self.formula_pool:
            go(f)

        return res

    """
    INTERFACE TO IMPLEMENT
    """

    def is_applicable(self, expression, direction):
        pass

    def apply(self, expression, direction):
        pass

    """
    RANDOM VALUE GENERATORS
    """

    def GEN_Bool(self):
        return lambda: random.choice(
            [Const("true", type="Bool"), Const("false", type="Bool")]
        )

    def GEN_String(self):
        return lambda: StringConst(
            "".join(
                random.choice(string.ascii_letters) for _ in range(random.randrange(10))
            )
        )

    def GEN_RegLan(self):
        return lambda: Expr(
            "re.union",
            [
                Expr("str.to_re", [self.random_value_node("String")], type="RegLan")
                for _ in range(3)
            ],
            type="RegLan",
        )

    def GEN_Int(self):
        return lambda: random.choice(
            [
                self.generate_random_nonneg_int_node(),
                self.generate_random_nonpos_int_node(),
            ]
        )

    def GEN_Real(self):
        return lambda: Const(
            str(random.uniform(1.5, 1.9) * (10 ** random.randrange(10))), type="Real"
        )

    def generate_random_nonneg_int_node(self):
        return Const(str(random.randrange(0, 10000)), type="Int")

    def generate_random_nonpos_int_node(self):
        return Expr(
            "-", [Const(str(random.randrange(0, 10000)), type="Int")], type="Int"
        )
