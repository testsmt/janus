import random

import logging
import copy

from src.mutators.Mutator import Mutator

# from src.parsing.typechecker import Context, typecheck_expr
from src.parsing.Parse import *

from src.parsing.Ast import Assert

from src.mutators.ImplicationBasedWeakeningStrengthening.common import *
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.regex import *
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.lhs_rhs import (
    OperatorReplacement,
    RelationPreservingAutomorphism,
    Homomorphism,
    PolymorphicHomomorphism,
    NumberRelationShiftSkewed,
    NumberRelationShiftBalanced,
    QuantifierSwap,
    UninterpretedFunctionEquality,
    StringContainsLength,
    StringPrefixLength,
    StringSuffixLength,
    StringEqualityPrefixSuffix,
    StringEqualityPrefixPrefix,
    StringEqualitySuffixSuffix,
    StringContainsPrefixSuffix,
    StringEqualityDistinctAppend,
    StringPrefixToExists,
    StringSuffixToExists,
    StringLeqApp,
    StringLeqSubstr,
    RegexAppend,
    OrToIte,
    IteToImpTrue,
    IteToImpFalse,
    ImpToIteTrue,
    ImpToIteFalse,
    ImpLiftToForall,
    InstantiateQuantifier,
    OrToImp,
    AddDisjunct,
    DropConjunct,
)


class ImplicationBasedWeakeningStrengthening(Mutator):
    def __init__(self, script, glbls, args):
        self.glbls = glbls
        self.script = script
        assert args.oracle in ["sat", "unsat"]
        self.oracle = SAT if args.oracle == "sat" else UNSAT

        self.op_rep_rules = [
            OperatorReplacement("str.<=", "=", ["String"]),
            OperatorReplacement("str.prefixof", "=", ["String"]),
            OperatorReplacement("str.suffixof", "=", ["String"]),
            OperatorReplacement("str.contains", "=", ["String"]),
            OperatorReplacement("str.<=", "str.<", ["String"]),
            OperatorReplacement("str.<", "distinct", ["String"]),
            OperatorReplacement("str.<=", "str.prefixof", ["String"]),
            OperatorReplacement(
                "str.contains", "str.prefixof", ["String"], reverseArguments=True
            ),
            OperatorReplacement(
                "str.contains", "str.suffixof", ["String"], reverseArguments=True
            ),
            RegexOperatorReplacement("re.+", "re.*"),
            RegexOperatorReplacement("re.inter", "re.union"),
            OperatorReplacement(">=", "=", ["Int", "Real"]),
            OperatorReplacement(">=", ">", ["Int", "Real"]),
            OperatorReplacement("<=", "<", ["Int", "Real"]),
            OperatorReplacement("<=", "=", ["Int", "Real"]),
            OperatorReplacement("distinct", ">", ["Int", "Real"]),
            OperatorReplacement("distinct", "<", ["Int", "Real"]),
            OperatorReplacement("or", "and", ["Bool"]),
            OperatorReplacement("or", "xor", ["Bool"]),
        ]

        self.string_rules = [
            OperatorReplacement("str.<=", "=", ["String"]),
            OperatorReplacement("str.prefixof", "=", ["String"]),
            OperatorReplacement("str.suffixof", "=", ["String"]),
            OperatorReplacement("str.contains", "=", ["String"]),
            StringEqualityDistinctAppend(),
            OperatorReplacement("str.<=", "str.<", ["String"]),
            OperatorReplacement("str.<", "distinct", ["String"]),
            OperatorReplacement("str.<=", "str.prefixof", ["String"]),
            OperatorReplacement(
                "str.contains", "str.prefixof", ["String"], reverseArguments=True
            ),
            OperatorReplacement(
                "str.contains", "str.suffixof", ["String"], reverseArguments=True
            ),
            StringPrefixToExists(),
            StringSuffixToExists(),
            StringEqualityPrefixSuffix(),
            StringEqualityPrefixPrefix(),
            StringEqualitySuffixSuffix(),
            StringContainsPrefixSuffix(),
            StringLeqApp(),
            StringLeqSubstr(),
            StringSuffixLength(),
            StringPrefixLength(),
            StringContainsLength(),
        ]

        self.regex_rules = [
            Regex_add_plus(),
            Regex_add_loop(),
            Regex_add_opt(),
            Regex_concat_to_option_power(),
            Regex_add_free_union(),
            Regex_change_range(),
            Regex_inter_idempotent(),
            Regex_union_idempotent()
            # , Regex_distribute_union_concat()
            ,
            RegexOperatorReplacement("re.*", "re.+"),
            RegexOperatorReplacement("re.union", "re.inter"),
            RegexAppend(),
        ]

        self.number_relation_rules = [
            OperatorReplacement(">=", "=", ["Int", "Real"]),
            OperatorReplacement(">=", ">", ["Int", "Real"]),
            OperatorReplacement("<=", "<", ["Int", "Real"]),
            OperatorReplacement("<=", "=", ["Int", "Real"]),
            OperatorReplacement("distinct", ">", ["Int", "Real"]),
            OperatorReplacement("distinct", "<", ["Int", "Real"]),
            NumberRelationShiftSkewed(),
            NumberRelationShiftBalanced(),
        ]

        self.core_logic_rules = [
            OperatorReplacement("or", "and", ["Bool"]),
            OperatorReplacement("or", "xor", ["Bool"]),
            QuantifierSwap(),
            UninterpretedFunctionEquality(),
            OrToIte(),
            IteToImpTrue(),
            IteToImpFalse(),
            ImpToIteTrue(),
            ImpToIteFalse(),
            ImpLiftToForall(),
            InstantiateQuantifier(),
            OrToImp(),
            AddDisjunct(),
            DropConjunct(),
        ]

        self.homomorphisms = [
            Homomorphism(
                R="str.prefixof",
                r="String",
                S="<=",
                s="Int",
                f="str.len",
                name="PREFIX-STRLEN",
            ),
            Homomorphism(
                R="str.suffixof",
                r="String",
                S="<=",
                s="Int",
                f="str.len",
                name="SUFFIX-STRLEN",
            ),
            Homomorphism(
                R="str.contains",
                r="String",
                S=">=",
                s="Int",
                f="str.len",
                name="CONTAINS-STRLEN",
            ),
            Homomorphism(
                R="<=",
                r="Int",
                S="str.prefixof",
                s="String",
                f=lambda String_1, t: Expr(
                    "str.substr", [String_1, Const("0", type="Int"), t], type="String"
                ),
                n=2,
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                name="INT-LEQ-SUBSTR-PREFIX",
            ),
            Homomorphism(
                R=">=",
                r="Int",
                S="str.suffixof",
                s="String",
                f=lambda String_1, Int_1, t: Expr(
                    "str.substr",
                    [String_1, t, Expr("str.len", [String_1], type="String")],
                    type="String",
                ),
                n=2,
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                name="INT-GEQ-SUBSTR-SUFFIX",
            ),
            Homomorphism(
                R="<",
                r="Int",
                S="str.prefixof",
                s="String",
                f=lambda String_1, t: Expr(
                    "str.substr", [String_1, Const("0", type="Int"), t], type="String"
                ),
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                n=2,
                name="INT-LE-SUBSTR-PREFIX",
            ),
            Homomorphism(
                R=">",
                r="Int",
                S="str.suffixof",
                s="String",
                f=lambda String_1, Int_1, t: Expr(
                    "str.substr",
                    [String_1, t, Expr("str.len", [String_1], type="String")],
                    type="String",
                ),
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                n=2,
                name="INT-GE-SUBSTR-SUFFIX",
            ),
            PolymorphicHomomorphism(
                R="=",
                rs=["String"],
                S="=",
                ss=["Bool"],
                f="str.is_digit",
                name="STR-EQ-ISDIGIT-EQ",
            ),
            PolymorphicHomomorphism(
                R="=",
                rs=["String"],
                S="=",
                ss=["Int"],
                f="str.to_code",
                name="STR-EQ-TOCODE-EQ",
            ),
            PolymorphicHomomorphism(
                R="=",
                rs=["String"],
                S="=",
                ss=["Int"],
                f="str.to_int",
                name="STR-EQ-TOINT-EQ",
            ),
            PolymorphicHomomorphism(
                R="=",
                rs=["Int"],
                S="=",
                ss=["String"],
                f="str.from_code",
                name="INT-EQ-FROM_CODE-EQ",
            ),
            PolymorphicHomomorphism(
                R="=",
                rs=["Int"],
                S="=",
                ss=["String"],
                f="str.from_int",
                name="INT-EQ-FROM_INT-EQ",
            ),
            PolymorphicHomomorphism(
                R="<",
                rs=["Int"],
                S="distinct",
                ss=["String"],
                f="str.from_int",
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                name="INT-LE-FROM_INT-DISTINCT",
            ),
            PolymorphicHomomorphism(
                R=">",
                rs=["Int"],
                S="distinct",
                ss=["String"],
                f="str.from_int",
                P=lambda ts: Expr(
                    "and",
                    [Expr(">=", [t, Const("0", type="Int")], type="Bool") for t in ts],
                    type="Bool",
                ),
                name="INT-GE-FROM_INT-DISTINCT",
            ),
        ]

        self.relation_preserving_automorphisms = [
            RelationPreservingAutomorphism("=", "abs", "Int", "EQ-ABS-INT"),
            RelationPreservingAutomorphism("=", "-", "Int", "EQ-NEG-INT"),
            RelationPreservingAutomorphism(
                "=",
                lambda Int_1, t: Expr("-", [Int_1, t], type="Int"),
                "Int",
                "EQ-SUB-INT-L",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda Int_1, t: Expr("-", [t, Int_1], type="Int"),
                "Int",
                "EQ-SUB-INT-R",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
                "Int",
                "EQ-ADD-INT-L",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
                "Int",
                "EQ-ADD-INT-R",
            ),
            RelationPreservingAutomorphism(
                "<=",
                lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
                "Int",
                "LEQ-ADD-INT-L",
            ),
            RelationPreservingAutomorphism(
                ">=",
                lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
                "Int",
                "GEQ-ADD-INT-R",
            ),
            RelationPreservingAutomorphism(
                "<",
                lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
                "Int",
                "LE-ADD-INT-L",
            ),
            RelationPreservingAutomorphism(
                ">",
                lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
                "Int",
                "GE-ADD-INT-R",
            ),
            RelationPreservingAutomorphism("=", "-", "Real", "EQ-NEG-REAL"),
            RelationPreservingAutomorphism(
                "=",
                lambda String_1, t: Expr("str.++", [String_1, t], type="String"),
                "String",
                "EQ-STR-CONCAT-L",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda String_1, t: Expr("str.++", [t, String_1], type="String"),
                "String",
                "EQ-STR-CONCAT-R",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda Int_1, Int_2, t: Expr(
                    "str.substr", [t, Int_1, Int_2], type="String"
                ),
                "String",
                "EQ-STR-SUBSTR",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda String_1, String_2, t: Expr(
                    "str.replace", [t, String_1, String_2], type="String"
                ),
                "String",
                "EQ-STR-REP",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda String_1, String_2, t: Expr(
                    "str.replace_all", [t, String_1, String_2], type="String"
                ),
                "String",
                "EQ-STR-REPALL",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda RegLan_1, String_2, t: Expr(
                    "str.replace_re", [t, RegLan_1, String_2], type="String"
                ),
                "String",
                "EQ-STR-REPRE",
            ),
            RelationPreservingAutomorphism(
                "=",
                lambda RegLan_1, String_2, t: Expr(
                    "str.replace_re_all", [t, RegLan_1, String_2], type="String"
                ),
                "String",
                "EQ-STR-REPREALL",
            ),
            RelationPreservingAutomorphism(
                "str.prefixof",
                lambda String_1, t: Expr("str.++", [String_1, t], type="String"),
                "String",
                "PRE-STR-CONCAT",
            ),
            RelationPreservingAutomorphism(
                "str.suffixof",
                lambda String_1, t: Expr("str.++", [t, String_1], type="String"),
                "String",
                "SUF-STR-CONCAT",
            ),
        ]

        self.custom_rule_set_1 = (
            self.regex_rules + self.string_rules + [InstantiateQuantifier()]
        )

        self.custom_rule_set_2 = self.regex_rules + [InstantiateQuantifier()]

        self.custom_rule_set_3 = [NumberRelationShiftSkewed()]

        if args.rule_set:
            self.rules = getattr(self, args.rule_set)
        else:
            self.rules = (
                self.string_rules
                + self.number_relation_rules
                + self.core_logic_rules
                + self.regex_rules
                + self.relation_preserving_automorphisms
                + self.homomorphisms
            )

        for rule in self.rules:
            rule.glbls = glbls
            formulas = self.get_formulas(script)
            rule.formula_pool = copy.deepcopy(formulas)

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
            for rule in self.rules:
                candidates = []
                for formula in formulas:
                    candidates.extend(self.get_candidates(formula, rule, 1))

                if len(candidates) > 0:
                    applicableRules += 1
            logging.info(f"Number of applicable rules: {applicableRules}")

        random.shuffle(self.rules)

        for rule in self.rules:

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
                logging.info(f"Chosen rule: {rule.name}")
                chosen_rule = rule.name

                # We successfully modified the script
                success = True
                break

        if not success:
            logging.info("No rule applies.")

        return self.script, success, chosen_rule
