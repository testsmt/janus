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

from src.parsing.Ast import Expr, StringConst, Const, Var

import random
import string
import copy
from inspect import signature

import src.mutators.ImplicationBasedWeakeningStrengthening.regex_meta as regex_meta
from src.mutators.ImplicationBasedWeakeningStrengthening.Rule import Rule
from src.mutators.ImplicationBasedWeakeningStrengthening.common import *


class RegexRule(Rule):
    def is_applicable(self, expression, direction):
        return expression.op == "str.in_re" and self.is_applicable_regex(
            expression.subterms[1], direction
        )

    def is_applicable_regex(self, re, direction):
        pass

    def get_candidates_regex(self, re, direction, res=False):
        if not res:
            res = []

        if re.type == "RegLan":
            if self.is_applicable_regex(re, direction):
                res.append((re, direction))

        if re.op == "re.comp":
            self.get_candidates_regex(re.subterms[0], -direction, res)
        elif re.op == "re.diff":
            self.get_candidates_regex(re.subterms[0], direction, res)
            self.get_candidates_regex(re.subterms[1], -direction, res)
        elif re.subterms:
            for t in re.subterms:
                self.get_candidates_regex(t, direction, res)

        return res

    def apply(self, expression, direction):
        s, re = expression.subterms
        cand = self.get_candidates_regex(re, direction)
        re, direction = random.choice(cand)
        quantify = self.apply_regex(re, direction)

        if quantify:
            quantifier, qvar = quantify
            expression_itself = copy.deepcopy(expression)
            convert_node_to_quantifier(
                expression, quantifier, ([qvar.name], [qvar.type]), expression_itself
            )

    def apply_regex(self, re, direction):
        pass


class RegexOperatorReplacement(RegexRule):
    def __init__(self, opWeak, opStrong):
        self.opWeak = opWeak
        self.opStrong = opStrong
        super().__init__(f"OPREP[{opWeak}][{opStrong}]")

    def is_applicable_regex(self, regex, direction):
        return (direction == WEAKENING and regex.op == self.opStrong) or (
            direction == STRENGTHENING and regex.op == self.opWeak
        )

    def apply_regex(self, regex, direction):
        if direction == WEAKENING:
            regex.op = self.opWeak
        if direction == STRENGTHENING:
            regex.op = self.opStrong


class Regex_add_free_union(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return True

    def apply_regex(self, re, direction):
        re_itself = copy.deepcopy(re)
        re.op = "re.union"
        n = random.randrange(1, 3)
        re.subterms = [re_itself]
        for _ in range(n):
            re.subterms = [self.random_value_node("RegLan")] + re.subterms


class Regex_concat_to_option_power(RegexRule):
    def __init__(self):
        super().__init__("concat_to_option_power")

    def is_applicable_regex(self, regex, direction):
        return regex.op == "re.++" and direction == WEAKENING

    def apply_regex(self, re, direction):
        args = re.subterms
        re.op = Expr("_", [Const("re.^"), Const(str(len(args)), type="Int")])
        re.subterms = [Expr("re.union", args, type="RegLan")]


class Regex_add_plus(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return direction == WEAKENING

    def apply_regex(self, re, direction):
        re_itself = copy.deepcopy(re)
        re.op = "re.+"
        re.subterms = [re_itself]


class Regex_add_opt(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return direction == WEAKENING

    def apply_regex(self, re, direction):
        re_itself = copy.deepcopy(re)
        re.op = "re.opt"
        re.subterms = [re_itself]


class Regex_add_loop(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return direction == WEAKENING

    def apply_regex(self, re, direction):
        re_itself = copy.deepcopy(re)
        n1 = random.randrange(1, 100)
        re.op = f"(_ re.loop 1 {n1})"
        re.subterms = [re_itself]


class Regex_inter_idempotent(RegexRule):
    def is_applicable_regex(self, regex, _):
        return True

    def apply_regex(self, regex, _):
        regex_itself1 = copy.deepcopy(regex)
        regex_itself2 = copy.deepcopy(regex)
        regex.subterms = [regex_itself1, regex_itself2]
        regex.op = "re.inter"


class Regex_union_idempotent(RegexRule):
    def is_applicable_regex(self, regex, _):
        return True

    def apply_regex(self, regex, _):
        regex_itself1 = copy.deepcopy(regex)
        regex_itself2 = copy.deepcopy(regex)
        regex.subterms = [regex_itself1, regex_itself2]
        regex.op = "re.union"


class Regex_change_range(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return regex.op == "re.range" and self.is_random_instantiatable("String")

    def apply_regex(self, re, direction):
        [s1, s2] = re.subterms
        s3 = self.random_value_node("String")
        s3_is_singleton = Expr(
            "=",
            [Expr("str.len", [s3], type="Int"), Const("1", type="Int")],
            type="Bool",
        )
        randomly_choose_upper = random.choice([True, False])
        if randomly_choose_upper:
            args = [s2, s3] if direction == WEAKENING else [s3, s2]
            comparison = Expr("str.<=", args, type="String")
            upper_bound = Expr(
                "ite",
                [Expr("and", [s3_is_singleton, comparison], type="Bool"), s3, s2],
                type="String",
            )

            # Replace upper bound
            re.subterms[1] = upper_bound
        else:
            args = [s3, s1] if direction == WEAKENING else [s1, s3]
            comparison = Expr("str.<=", args, type="String")
            lower_bound = Expr(
                "ite",
                [Expr("and", [s3_is_singleton, comparison], type="Bool"), s3, s1],
                type="String",
            )

            # Replace lower bound
            re.subterms[0] = lower_bound


class Regex_distribute_union_concat(RegexRule):
    def is_applicable_regex(self, regex, direction):
        return regex.op == "re.++" and any(
            map(lambda r: r.op == "re.union", regex.subterms)
        )

    def apply_regex(self, regex, direction):
        beforeUnion = []
        afterUnion = []
        union = None
        for r in regex.subterms:
            if not union and r.op == "re.union":
                union = r
                continue

            if union:
                afterUnion.append(r)
            else:
                beforeUnion.append(r)

        regex.op = "re.union"
        regex.subterms = [
            Expr("re.++", beforeUnion + [u] + afterUnion, type="RegLan")
            for u in union.subterms
        ]
