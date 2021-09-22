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

from typing import Dict
from src.mutators.ImplicationBasedWeakeningStrengthening.Rule import Rule
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.lhs_rhs import *
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.regex import *

ALL_RULES: Dict[str, Rule] = {
    'SUFFIXLEN': Homomorphism(
        r="String", R="str.suffixof", s="Int", S="<=", f="str.len"
    ),
    'PREFIXLEN': Homomorphism(
        r="String", R="str.prefixof", s="Int", S="<=", f="str.len"
    ),
    'CONTAINSLEN': Homomorphism(
        r="String", R="str.contains", s="Int", S=">=", f="str.len"
    ),
    'STRLEQSUBSTR': StringLeqSubstr(),
    'STRLEQAPP': StringLeqApp(),
    'ORTOIMP': OrToImp(),
    'ADDDISJ': AddDisjunct(),
    'DROPCONJ': DropConjunct(),
    'REGEXAPP': RegexAppend(),
    'INSTQUANT': InstantiateQuantifier(),
    'IMPLIFTTOFORALL': ImpLiftToForall(),
    'IMPTOITEFALSE': ImpToIteFalse(),
    'IMPTOITETRUE': ImpToIteTrue(),
    'ITETOIMPFALSE': IteToImpFalse(),
    'ITETOIMPTRUE': IteToImpTrue(),
    'ORTOITE': OrToIte(),
    'STRCONTOEX': StringContainsToExists(),
    'STRSUFTOEX': StringSuffixToExists(),
    'STRPRETOEX': StringPrefixToExists(),
    'STREQDISTAPP': StringEqualityDistinctAppend(),
    'STRCONTAINSPRESUF': StringContainsPrefixSuffix(),
    'STREQSUFFIXSUFFIX': StringEqualitySuffixSuffix(),
    'STREQPREFIXPREFIX': StringEqualityPrefixPrefix(),
    'STREQPREFIXSUFFIX': StringEqualityPrefixSuffix(),
    'UNINFUNEQ': UninterpretedFunctionEquality(),
    'QUANTSWP': QuantifierSwap(),
    'NUMRELSHIFTBALANCED': NumberRelationShiftBalanced(),
    'NUMRELSHIFTSKEWED': NumberRelationShiftSkewed(),
    'OPREP_STR_EQ_LEQ': OperatorReplacement("=", "str.<=", ["String"]),
    'OPREP_STR_EQ_PREFIX': OperatorReplacement("=", "str.prefixof", ["String"]),
    'OPREP_STR_EQ_SUFFIX': OperatorReplacement("=", "str.suffixof", ["String"]),
    'OPREP_STR_EQ_CONTAINS': OperatorReplacement("=", "str.contains", ["String"]),
    'OPREP_STR_LE_LEQ': OperatorReplacement("str.<", "str.<=", ["String"]),
    'OPREP_STR_LE_DIST': OperatorReplacement("str.<", "distinct", ["String"]),
    'OPREP_STR_PREFIX_LEQ': OperatorReplacement("str.prefixof", "str.<=", ["String"]),
    'OPREP_STR_PREFIX_CONTAINS': OperatorReplacement(
        "str.prefixof", "str.contains", ["String"], reverseArguments=True
    ),
    'OPREP_STR_SUFFIX_CONTAINS': OperatorReplacement(
        "str.suffixof", "str.contains", ["String"], reverseArguments=True
    ),
    'OPREP_RE_PLUS_STAR': RegexOperatorReplacement("re.+", "re.*"),
    'OPREP_RE_INTER_UNION': RegexOperatorReplacement("re.inter", "re.union"),
    'OPREP_NUM_EQ_GEQ': OperatorReplacement("=", ">=", ["Int", "Real"]),
    'OPREP_NUM_GE_GEQ': OperatorReplacement(">", ">=", ["Int", "Real"]),
    'OPREP_NUM_LE_LEQ': OperatorReplacement("<", "<=", ["Int", "Real"]),
    'OPREP_NUM_EQ_LEQ': OperatorReplacement("=", "<=", ["Int", "Real"]),
    'OPREP_NUM_GE_DIST': OperatorReplacement(">", "distinct", ["Int", "Real"]),
    'OPREP_NUM_LE_DIST': OperatorReplacement("<", "distinct", ["Int", "Real"]),
    'OPREP_AND_OR': OperatorReplacement("and", "or", ["Bool"]),
    'OPREP_XOR_OR': OperatorReplacement("xor", "or", ["Bool"]),
    'RE_DISTRIBUTE_UNION_CONCAT': Regex_distribute_union_concat(),
    'RE_CHANGE_RANGE': Regex_change_range(),
    'RE_UNION_IDEMPOTENT': Regex_union_idempotent(),
    'RE_INTER_IDEMPOTENT': Regex_inter_idempotent(),
    'RE_ADD_LOOP': Regex_add_loop(),
    'RE_ADD_OPT': Regex_add_opt(),
    'RE_ADD_PLUS': Regex_add_plus(),
    'RE_CONCAT_TO_OPTION_POWER': Regex_concat_to_option_power(),
    'RE_ADD_FREE_UNION': Regex_add_free_union(),
    'HOM_PREFIX_STRLEN': Homomorphism(
        R="str.prefixof",
        r="String",
        S="<=",
        s="Int",
        f="str.len",
    ),
    'SUFFIX-STRLEN': Homomorphism(
        R="str.suffixof",
        r="String",
        S="<=",
        s="Int",
        f="str.len",
    ),
    'CONTAINS-STRLEN': Homomorphism(
        R="str.contains",
        r="String",
        S=">=",
        s="Int",
        f="str.len",
    ),
    'INT-LEQ-SUBSTR-PREFIX': Homomorphism(
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
    ),
    'INT-GEQ-SUBSTR-SUFFIX': Homomorphism(
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
    ),
    'NT-LE-SUBSTR-PREFIX': Homomorphism(
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
    ),
    'INT-GE-SUBSTR-SUFFIX': Homomorphism(
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
    ),
    'STR-EQ-ISDIGIT-EQ': PolymorphicHomomorphism(
        R="=",
        rs=["String"],
        S="=",
        ss=["Bool"],
        f="str.is_digit",
    ),
    'STR-EQ-TOCODE-EQ': PolymorphicHomomorphism(
        R="=",
        rs=["String"],
        S="=",
        ss=["Int"],
        f="str.to_code",
    ),
    'STR-EQ-TOINT-EQ': PolymorphicHomomorphism(
        R="=",
        rs=["String"],
        S="=",
        ss=["Int"],
        f="str.to_int",
    ),
    'INT-EQ-FROM_CODE-EQ': PolymorphicHomomorphism(
        R="=",
        rs=["Int"],
        S="=",
        ss=["String"],
        f="str.from_code",
    ),
    'INT-EQ-FROM_INT-EQ': PolymorphicHomomorphism(
        R="=",
        rs=["Int"],
        S="=",
        ss=["String"],
        f="str.from_int",
    ),
    'INT-LE-FROM_INT-DISTINCT': PolymorphicHomomorphism(
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
    ),
    'INT-GE-FROM_INT-DISTINCT': PolymorphicHomomorphism(
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
    ),
    'EQ-ABS-INT': RelationPreservingAutomorphism("=", "abs", "Int"),
    "EQ-NEG-INT": RelationPreservingAutomorphism(
        "=",
        "-",
        "Int",
    ),
    "EQ-SUB-INT-L": RelationPreservingAutomorphism(
        "=",
        lambda Int_1, t: Expr("-", [Int_1, t], type="Int"),
        "Int",
    ),
    "EQ-SUB-INT-R": RelationPreservingAutomorphism(
        "=",
        lambda Int_1, t: Expr("-", [t, Int_1], type="Int"),
        "Int",
    ),
    "EQ-ADD-INT-L": RelationPreservingAutomorphism(
        "=",
        lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
        "Int",
    ),
    "EQ-ADD-INT-R": RelationPreservingAutomorphism(
        "=",
        lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
        "Int",
    ),
    "LEQ-ADD-INT-L": RelationPreservingAutomorphism(
        "<=",
        lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
        "Int",
    ),
    "GEQ-ADD-INT-R": RelationPreservingAutomorphism(
        ">=",
        lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
        "Int",
    ),
    "LE-ADD-INT-L": RelationPreservingAutomorphism(
        "<",
        lambda Int_1, t: Expr("+", [Int_1, t], type="Int"),
        "Int",
    ),
    "GE-ADD-INT-R": RelationPreservingAutomorphism(
        ">",
        lambda Int_1, t: Expr("+", [t, Int_1], type="Int"),
        "Int",
    ),
    "EQ-NEG-REAL": RelationPreservingAutomorphism(
        "=",
        "-",
        "Real",
    ),
    "EQ-STR-CONCAT-L": RelationPreservingAutomorphism(
        "=",
        lambda String_1, t: Expr("str.++", [String_1, t], type="String"),
        "String",
    ),
    "EQ-STR-CONCAT-R": RelationPreservingAutomorphism(
        "=",
        lambda String_1, t: Expr("str.++", [t, String_1], type="String"),
        "String",
    ),
    "EQ-STR-SUBSTR": RelationPreservingAutomorphism(
        "=",
        lambda Int_1, Int_2, t: Expr("str.substr", [t, Int_1, Int_2], type="String"),
        "String",
    ),
    "EQ-STR-REP": RelationPreservingAutomorphism(
        "=",
        lambda String_1, String_2, t: Expr(
            "str.replace", [t, String_1, String_2], type="String"
        ),
        "String",
    ),
    "EQ-STR-REPALL": RelationPreservingAutomorphism(
        "=",
        lambda String_1, String_2, t: Expr(
            "str.replace_all", [t, String_1, String_2], type="String"
        ),
        "String",
    ),
    "EQ-STR-REPRE": RelationPreservingAutomorphism(
        "=",
        lambda RegLan_1, String_2, t: Expr(
            "str.replace_re", [t, RegLan_1, String_2], type="String"
        ),
        "String",
    ),
    "EQ-STR-REPREALL": RelationPreservingAutomorphism(
        "=",
        lambda RegLan_1, String_2, t: Expr(
            "str.replace_re_all", [t, RegLan_1, String_2], type="String"
        ),
        "String",
    ),
    "PRE-STR-CONCAT": RelationPreservingAutomorphism(
        "str.prefixof",
        lambda String_1, t: Expr("str.++", [String_1, t], type="String"),
        "String",
    ),
    "SUF-STR-CONCAT": RelationPreservingAutomorphism(
        "str.suffixof",
        lambda String_1, t: Expr("str.++", [t, String_1], type="String"),
        "String",
    ),
}
