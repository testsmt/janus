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

import random

import logging
import copy

from src.mutators.Mutator import Mutator

# from src.parsing.typechecker import Context, typecheck_expr
from src.parsing.Parse import *

from src.parsing.Ast import Assert

from src.mutators.ImplicationBasedWeakeningStrengthening.common import *
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.rule_set import (
    RuleSet,
    parseRuleSet,
)


class ImplicationBasedWeakeningStrengthening(Mutator):
    def __init__(self, script, glbls, args):
        self.glbls = glbls
        self.script = script
        assert args.oracle in ["sat", "unsat"]
        self.oracle = SAT if args.oracle == "sat" else UNSAT

        self.rules = parseRuleSet(args.rule_set)

        formulas = copy.deepcopy(self.get_formulas(script))
        for rule in self.rules:
            RuleSet[rule].glbls = glbls
            RuleSet[rule].formula_pool = formulas

    """
    Returns a list of AST node references paired with their parity
    """

    def get_candidates(self, term, rule, parity):

        res = []
        if rule.is_applicable(term, self.oracle * parity):
            res.append((term, parity))

        if term.op == "not":
            res.extend(self.get_candidates(term.subterms[0], rule, -parity))

        elif term.op == "and":
            for arg in term.subterms:
                res.extend(self.get_candidates(arg, rule, parity))

        elif term.op == "or":
            for arg in term.subterms:
                res.extend(self.get_candidates(arg, rule, parity))

        elif term.op == "implies" or (
            term.op == "=>" and term.subterms[0].type == "Bool"
        ):
            lhses = term.subterms[:-1]
            rhs = term.subterms[-1]
            for lhs in lhses:
                res.extend(self.get_candidates(lhs, rule, -parity))
            res.extend(self.get_candidates(rhs, rule, parity))

        elif term.op == "ite":
            [b, t1, t2] = term.subterms
            # Note that we ignore 'b' because its parity is ambiguous in 'ite'
            res.extend(self.get_candidates(t1, rule, parity))
            res.extend(self.get_candidates(t2, rule, parity))

        elif term.let_terms is not None:

            for arg in term.subterms:
                res.extend(self.get_candidates(arg, rule, parity))

        elif term.quantifier is not None:
            for arg in term.subterms:
                res.extend(self.get_candidates(arg, rule, parity))

        return res

    def get_formulas(self, script):
        return list(
            map(
                lambda assrt: assrt.term,
                filter(lambda cmd: isinstance(cmd, Assert), script.commands),
            )
        )

    def mutate(self):

        formulas = self.get_formulas(self.script)

        success = False
        candidates = []
        number_of_modifications_done = 0
        chosen_rule = None

        if logging.getLogger().isEnabledFor(logging.INFO):
            applicableRules = 0
            for rule_name in self.rules:
                rule = RuleSet[rule_name]
                candidates = []
                for formula in formulas:
                    candidates.extend(self.get_candidates(formula, rule, 1))

                if len(candidates) > 0:
                    applicableRules += 1
            logging.info(f"Number of applicable rules: {applicableRules}")

        rules_in_random_order = list(self.rules)
        random.shuffle(rules_in_random_order)

        for rule_name in rules_in_random_order:
            rule = RuleSet[rule_name]

            candidates = []

            # Go through all formulas in script and get candidates for 'rule'
            for formula in formulas:
                candidates.extend(self.get_candidates(formula, rule, 1))

            # This rule is applicable to some subformula, so we pick it
            if len(candidates) > 0:

                # Apply the rule to a random candidate
                to_replace, parity = random.choice(candidates)
                rule.apply(to_replace, parity * self.oracle)
                number_of_modifications_done += 1
                logging.info(f"Chosen rule: {rule_name}")
                chosen_rule = rule_name

                # We successfully modified the script
                success = True
                break

        if not success:
            logging.info("No rule applies.")

        return self.script, success, chosen_rule
