import unittest
import os
import subprocess
import sys

sys.path.append("../../")

import shutil
import random

from src.parsing.Ast import *
from src.parsing.Typechecker import typecheck
from src.parsing.Parse import *
from src.mutators.ImplicationBasedWeakeningStrengthening.ImplicationBasedWeakeningStrengthening import *
from src.mutators.ImplicationBasedWeakeningStrengthening.rules import *

z3 = shutil.which("z3") or os.environ.get("Z3_EXE", None)

if z3 == None:
    print("z3 not found, cannot run tests.")
    exit(1)

tests = [  # filename, rule, oracle, number of candidates per formula in order of file, chosen candidate for each formula or None
    ("phi1", "OPREP[>=][=][['Int', 'Real']]", "sat", [1, 0, 0], [0, None, None]),
    ("phi2", "OPREP[<=][=][['Int', 'Real']]", "sat", [0, 1], [None, 0]),
    (
        "Primes_true-unreach-call.c_127",
        "OPREP[<=][=][['Int', 'Real']]",
        "unsat",
        [3, 0],
        [2, None],
    ),
    (
        "z3-issue-4891-mod",
        "OPREP[distinct][>][['Int', 'Real']]",
        "sat",
        [0, 0, 1, 0, 0, 0],
        [None, None, None, None, None, None],
    ),
    ("z3-issue-4804-mod", "OPREP[<=][=][['Int', 'Real']]", "unsat", [0, 3], [None, 2]),
    ("formula_101_another", "QUANTSWP", "sat", [5], [3]),
    ("prefixof", "PREFIXLEN", "sat", [1], [0]),
    ("suffixof", "SUFFIXLEN", "sat", [1], [0]),
    ("contains", "CONTAINSLEN", "sat", [1], [0]),
    ("str-eq-1", "STREQPREFIXSUFFIX", "sat", [1], [0]),
    ("str-eq-2", "STREQPREFIXPREFIX", "sat", [1], [0]),
    ("str-eq-3", "STREQSUFFIXSUFFIX", "sat", [1], [0]),
    ("str-contains", "STRCONTAINSPRESUF", "sat", [1], [0]),
    ("unintfun-minus-regression", "UNINFUNEQ", "unsat", [0, 0], [None, None]),
    ("unintfun-minus-regression-mod", "UNINFUNEQ", "unsat", [1, 0], [0, None]),
    ("prefix_to_exists", "STRPRETOEX", "sat", [1], [0]),
    ("suffix_to_exists", "STRSUFTOEX", "sat", [1], [0]),
    ("or_to_ite", "ORTOITE", "sat", [1], [0]),
    ("or_to_ite2", "ORTOITE", "sat", [1], [0]),
    ("ite_to_imp_true", "ITETOIMPTRUE", "sat", [1], [0]),
    ("ite_to_imp_false", "ITETOIMPFALSE", "sat", [1], [0]),
    ("imp_to_ite_true", "IMPTOITETRUE", "sat", [1, 1], [0, 0]),
    ("imp_to_ite_false", "IMPTOITEFALSE", "sat", [1, 1], [0, 0]),
    ("imp_lift_to_forall", "IMPLIFTTOFORALL", "sat", [1, 1], [0, 0]),
    (
        "prefix-contains",
        "OPREP[str.contains][str.prefixof][['String']]",
        "sat",
        [1],
        [0],
    ),
    ("instantiate-quantifier", "INSTQUANT", "sat", [1, 1], [0, 0]),
    ("instantiate-quantifier-string", "INSTQUANT", "sat", [1], [0]),
    ("instantiate-quantifier-string2", "INSTQUANT", "sat", [1], [0]),
    ("re1", "REGEXMOD[concat_to_option_power]", "sat", [1], [0]),
    ("re2", "REGEXMOD[OPREP[re.*][re.+]]", "sat", [1], [0]),
    ("re3", "REGEXMOD[add_plus]", "sat", [1], [0]),
    ("re4", "REGEXMOD[OPREP[re.union][re.inter]]", "sat", [1], [0]),
    ("re5", "REGEXMOD[add_free_union]", "sat", [1], [0]),
    ("regex-app1", "REGEXAPP", "sat", [1], [0]),
    ("regex-app2", "REGEXAPP", "sat", [1], [0]),
    ("free-variables-regression", "INSTQUANT", "sat", [2, 1], [0, 0]),
    ("regex-change-range", "REGEXMOD[change_range]", "sat", [1, 1], [0, 0]),
    ("regex-change-range2", "REGEXMOD[change_range]", "sat", [1, 1], [0, 0]),
    ("inter-idempotent", "REGEXMOD[inter_idempotent]", "sat", [1], [0]),
    ("add_plus", "REGEXMOD[add_plus]", "sat", [1], [0])
    #        , ('distribute_union_over_concat', "REGEXMOD[distribute_union_concat]", 'sat', [1], [0])
    ,
    ("instantiate-quantifier-regression", "INSTQUANT", "unsat", [1], [0]),
    ("number-relation-shift-1", "NUMRELSHIFTSKEWED", "unsat", [3], [1]),
    (
        "number-relation-shift-2",
        "NUMRELSHIFTBALANCED",
        "sat",
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ),
    ("quantifier-instantiation-let-regression-2", "INSTQUANT", "sat", [1], [0]),
    ("drop-conj", "DROPCONJ", "sat", [1, 1], [0, 0]),
    ("add-disj", "ADDDISJ", "sat", [3], [1]),
    ("or-to-imp", "ORTOIMP", "sat", [1, 1], [0, 0]),
    ("string-leq-app", "STRLEQAPP", "sat", [1, 1], [0, 0]),
    ("string-leq-substr", "STRLEQSUBSTR", "sat", [0, 1, 1], [None, 0, 0]),
    ("random-value-global", "INSTQUANT", "sat", [1], [0]),
    ("relprevaut-1", "EQ-ABS-INT", "sat", [1], [0]),
    ("relprevaut-2", "GEQ-ADD-INT-R", "sat", [1], [0]),
    ("homomorphism-1", "PREFIX-STRLEN", "sat", [1], [0]),
    ("homomorphism-2", "INT-LEQ-SUBSTR-PREFIX", "sat", [1, 0], [0, None]),
    ("homomorphism-3", "INT-GEQ-SUBSTR-SUFFIX", "sat", [1], [0]),
    (
        "substr-homomorphism-regression",
        "INT-GE-SUBSTR-SUFFIX",
        "sat",
        [0, 1],
        [None, 0],
    ),
    ("str-distinct", "STREQDIST", "sat", [1], [0]),
    ("number-relation-shift-3", "NUMRELSHIFTSKEWED", "sat", [1], [0])
    # TODO waiting on https://github.com/wintered/formula-weaking-strengthening/issues/3
    # , ('quantifier-instantiation-let-regression', lambda formulas: InstantiateQuantifier(formulas), 'sat', [1], [0])
    ,
    ("leq-substr-homomorphism-regression", "INT-LEQ-SUBSTR-PREFIX", "sat", [1], [0]),
    ("str-isdigit", "STR-EQ-ISDIGIT-EQ", "sat", [1], [0]),
    ("fromint-distinct", "INT-LE-FROM_INT-DISTINCT", "sat", [1], [0]),
    ("regex-add-plus", "REGEXMOD[add_plus]", "sat", [1], [0]),
    ("regex-add-opt", "REGEXMOD[add_opt]", "sat", [1], [0]),
    ("regex-add-loop", "REGEXMOD[add_loop]", "sat", [1], [0]),
    ("empty-string-replace", "EQUAL[EMPTYSTRREP]", "sat", [2, 3, 1], [0, 0, 0]),
    ("str-prepend-to-empty-replace", "EQUAL[STRPRETOEMPTREP]", "sat", [1, 1], [0, 0]),
    ("str-to-int", "EQUAL[STRTOINT]", "sat", [1, 2], [0, 1])
    # , ('reactivity-lemma-node2938', lambda formulas: NumberRelationConstantShift('Real', 1), 'sat', [12], [4])
    # , ('ETCS-essentials-live-range2.proof-node1046', lambda formulas: NumberRelationConstantShift('Real', 7.4), 'sat', [14], [12])
    # , ('z3-issue-5042-mod', lambda formulas: NumberRelationSkewedShift('Real', 1), 'sat', [2], [1])
]


class MockArgs:
    def __init__(self, oracle):
        self.iterations = 1
        self.oracle = oracle
        self.rule_set = None


class ImpBasedUnitTest(unittest.TestCase):
    pass


def test_case(name, ruleName, oracle, num_candidates, chosen_candidates):
    def m(self):

        input_file = f"tests/unit/impbased/{name}.smt2"
        expected_file = f"tests/unit/impbased/{name}_expected.smt2"

        out1 = subprocess.getoutput(f"{z3} {input_file}")
        out2 = subprocess.getoutput(f"{z3} {expected_file}")

        self.assertEqual(
            out1, oracle, f"Z3 does not agree with oracle for {name}.smt2."
        )
        self.assertEqual(
            out2, oracle, f"Z3 does not agree with oracle for {name}_expected.smt2"
        )

        script, glbls = parse_file(input_file, silent=True)
        typecheck(script, glbls)

        args = MockArgs(oracle)

        # Some rules contain randomness, so we need to fix a seed in order to deterministically test them.
        random.seed(17)

        generator = ImplicationBasedWeakeningStrengthening(script, glbls, args)
        all_rules = generator.rules
        generator.rules = [r for r in generator.rules if r.name == ruleName]
        if len(generator.rules) != 1:
            print(f"Spelling mistake in operator name: {ruleName}")
            print("Available names:")
            for rule in all_rules:
                print(rule.name)
            exit(1)

        rule = generator.rules[0]

        formulas = generator.get_formulas(script)

        self.assertEqual(len(formulas), len(num_candidates))
        self.assertEqual(len(formulas), len(chosen_candidates))
        for f, n, i in zip(formulas, num_candidates, chosen_candidates):
            candidates = generator.get_candidates(f, rule, 1)
            self.assertEqual(
                len(candidates),
                n,
                f"Expected {n} candidates for {rule.name} for {name}.smt2.",
            )
            if i is not None:
                rule.apply(candidates[i][0], candidates[i][1] * generator.oracle)

        expected, _ = parse_file(expected_file, silent=True)
        self.maxDiff = None
        self.assertEqual(
            str(script),
            str(expected),
            f"Mutation result different from expected for {name}.smt2.",
        )

    return m


for name, rule, oracle, num_candidates, chosen_candidates in tests:
    setattr(
        ImpBasedUnitTest,
        f"test_{name}",
        test_case(name, rule, oracle, num_candidates, chosen_candidates),
    )


if __name__ == "__main__":
    unittest.main()
