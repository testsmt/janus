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

from src.mutators.ImplicationBasedWeakeningStrengthening.common import (
    WEAKENING,
    STRENGTHENING,
    convert_to_node,
    fresh_var,
    convert_node_to_quantifier,
    convert_node_to_single_subterm,
)
from src.mutators.ImplicationBasedWeakeningStrengthening.Rule import Rule
import src.mutators.ImplicationBasedWeakeningStrengthening.regex_meta as regex_meta
from src.parsing.Ast import Expr, StringConst, Const, Var
from inspect import signature
import string
import random
import copy


class LHS_RHS_Rule(Rule):

    """
    INTERFACE TO IMPLEMENT

    to_RHS() will only be called on expressions for which matches_LHS() returns True and vice versa.
    Thus, if a rule is too cumbersome to apply in one direction it can be omitted or only specified for special cases
    by only matching a subset of expression to which it is theoretically applicable.

    And rules that are only feasible in one direction can completely omit the other match_*/to_* methods since
    the defaults here will remove this case.
    """

    def matches_LHS(self, expression):
        return False

    def matches_RHS(self, expression):
        return False

    def to_RHS(self, expression):
        pass

    def to_LHS(self, expression):
        pass


class Equivalence(LHS_RHS_Rule):

    """
    A rule of the form:

        φ1 <==> φ2
    """

    def is_applicable(self, expression, direction):
        return self.matches_LHS(expression) or self.matches_RHS(expression)

    def apply(self, expression, direction):
        if self.matches_LHS(expression):
            self.to_RHS(expression)
        elif self.matches_RHS(expression):
            self.to_LHS(expression)


class Implication(LHS_RHS_Rule):

    """
    A rule of the form:

        φ1 ==> φ2
    """

    def is_applicable(self, expression, direction):
        return (direction == WEAKENING and self.matches_LHS(expression)) or (
            direction == STRENGTHENING and self.matches_RHS(expression)
        )

    def apply(self, expression, direction):
        if direction == WEAKENING:
            self.to_RHS(expression)
        elif direction == STRENGTHENING:
            self.to_LHS(expression)


class PolymorphicHomomorphism(Implication):

    """
    A template for rules of the following form:

        (R t1:r ... tn:r) : Bool   ==>   (=> (P t1 ... tn) (S (f t1):s ... (f tn):s)) : Bool

    The logical parameters are:
        * r,s:str               sort symbols
        * R:str                 A predicate symbol with n arguments of sort r
        * S:str                 A predicate symbol with n arguments of sort s
        * f:str|function        A function of sort r^n -> s satisfying the law above (for all t_1,...,t_n). See below.
        * P:option(function)    A predicate which allows specification of a side condition on the arguments, i.e. restriction of the domain.
                                If omitted, the implication is not produced which means the rule applies to all of r^n.
        * n:option(int)         The number of arguments. If omitted the rule applies to any n > 0.

    The specification of 'f' can be given in two ways:

        1. str: Pass the name of a defined SMT-function to be applied, e.g. 'abs' for absolute value of 'Int's.
           The special string 'id' is reserved for the identity function, e.g. lambda x: x.

        2. function: Pass a function of the form

                lambda r1,...,rn,t : t'

           Here, t is the AST of ti in the description above. t' should be the AST of (f t1).
           r1,..,rn is an arbitrary (also zero) number of random arguments which will be randomly instantiated for every rule application,
           e.g. ri has the same value for every function application in one rule application but (most likely) not in two different rule applications.
           The sort of the random values must be specified in its name as follows:

                lambda Int_x, Int_y, String_1234, t : t'

    The specification of 'P' must be given as a function:

        lambda args: t'

    Here args is a list of ASTs of all ti's above and t' should be the AST of (P t1 ... tn).

    TODO: Update docs with Π, rs, ss
    """

    def __init__(self, R, rs, S, ss, f, name, Π=None, n=None, P=None, formulas=None):
        self.name = name
        self.R = R
        self.S = S
        self.sortMap = {r: s for r, s in zip(rs, ss)}
        self.P = P
        self.Π = Π
        self.n = n
        self.predefinedFunctions = {"__ID__": lambda x: x}
        self.predefinedFunctionSymbol = None
        super().__init__(formulas)

        # PREDEFINED FUNCTION
        if f in self.predefinedFunctions:
            self.predefinedFunctionSymbol = f
            f = self.predefinedFunctions[f]

        if callable(f):
            self.f = f
            self.randomParamSorts = [
                rArgName.split("_")[0]
                for rArgName in list(signature(f).parameters.keys())[:-1]
            ]
            self.randomParams = signature(f).parameters.keys()
        elif isinstance(f, str):
            """NOTE
            If 'self.f' is applied to a node of a type not in 'self.rs',
            it will result in an untyped AST node.
            """
            self.f = lambda t: Expr(f, [t], type=self.sortMap.get(t.type, None))
            self.randomParamSorts = []
        else:
            raise RuntimeError("Unsupported type of Homomorphism.f given") from exc

    def matches_LHS(self, expression):

        # Ensure there are subterms
        if not expression.has_subterms():
            return False

        # Check whether this type is supported and remember it
        if expression.subterms[0].type in self.sortMap:
            r = expression.subterms[0].type
            return (
                expression.is_type("Bool")
                and expression.is_operator(self.R)
                and all([t.is_type(r) for t in expression.subterms])
                and (not self.n or expression.has_n_subterms(self.n))
            )

        return False

    def to_RHS(self, expression):
        randomParams = []
        for s in self.randomParamSorts:
            randomParams.append(self.random_value_node(s))

        fApps = [self.f(*randomParams, t) for t in expression.subterms]

        if self.Π:
            fApps = list(self.Π(fApps))

        if self.P is None:
            expression.op = self.S
            expression.subterms = fApps
        else:
            convert_to_node(
                expression,
                Expr(
                    "=>",
                    [
                        self.P(copy.deepcopy(expression.subterms)),
                        Expr(self.S, fApps, type="Bool"),
                    ],
                    type="Bool",
                ),
            )

    def matches_RHS(self, expression):
        if (
            self.predefinedFunctionSymbol == "__ID__"
            and self.Π in [reversed, None]
            and self.P is None
        ):

            # Ensure there are subterms
            if not expression.has_subterms():
                return False

            # Check whether this type is supported and remember it
            if expression.subterms[0].type in self.sortMap.values():
                s = expression.subterms[0].type
                return (
                    expression.is_type("Bool")
                    and expression.is_operator(self.S)
                    and all([t.is_type(s) for t in expression.subterms])
                )

        return False

    def to_LHS(self, expression):
        expression.op = self.R
        if self.Π:
            expression.subterms = list(self.Π(expression.subterms))


class Homomorphism(PolymorphicHomomorphism):
    def __init__(self, R, r, S, s, f, name, Π=None, n=None, P=None, formulas=None):
        super().__init__(
            R=R, rs=[r], S=S, ss=[s], f=f, name=name, Π=Π, n=n, P=P, formulas=formulas
        )


class OperatorReplacement(PolymorphicHomomorphism):
    def __init__(self, opWeak, opStrong, supportedSorts, reverseArguments=False):
        Π = reversed if reverseArguments else None
        name = f"OPREP[{opWeak}][{opStrong}][{str(supportedSorts)}]"
        super().__init__(
            S=opWeak,
            R=opStrong,
            rs=supportedSorts,
            ss=supportedSorts,
            f="__ID__",
            Π=Π,
            name=name,
        )

    def is_applicable(self, expression, direction):
        x = super().is_applicable(expression, direction)
        return x


class NumberRelationShiftSkewed(Implication):
    def __init__(self):
        self.name = "NUMRELSHIFTSKEWED"
        super().__init__()

    def matches_LHS(self, expression):
        return (
            expression.is_operator(">", ">=", "<", "<=")
            and expression.has_subterms()
            and expression.subterms[0].is_type("Int")
        )

    def to_RHS(self, expression):
        sort = expression.subterms[0].type

        shift_amount_node = self.random_value_node(sort)
        shift_amount_node_nonneg = Expr("abs", [shift_amount_node], type=sort)
        shift_amount_node_nonpos = Expr(
            "-", [Expr("abs", [shift_amount_node], type=sort)], type=sort
        )

        shift_operator = random.choice(["-", "+"])

        split = random.randrange(1, len(expression.subterms))
        modify_low = random.choice([True, False])
        left, right = expression.subterms[0:split], expression.subterms[split:]

        if expression.op in [">", ">="]:
            # reverse low and high
            low, high = right, left
        else:
            low, high = left, right

        if shift_operator == "+":
            if modify_low:
                # add non-positive to the low
                low = list(
                    map(
                        lambda t: Expr(
                            shift_operator, [t, shift_amount_node_nonpos], type=sort
                        ),
                        low,
                    )
                )
            else:
                # add non-negative to the high
                high = list(
                    map(
                        lambda t: Expr(
                            shift_operator, [t, shift_amount_node_nonneg], type=sort
                        ),
                        high,
                    )
                )
        if shift_operator == "-":
            if modify_low:
                # subtract non-negative from low
                low = list(
                    map(
                        lambda t: Expr(
                            shift_operator, [t, shift_amount_node_nonneg], type=sort
                        ),
                        low,
                    )
                )
            else:
                # subtract non-positive from high
                high = list(
                    map(
                        lambda t: Expr(
                            shift_operator, [t, shift_amount_node_nonpos], type=sort
                        ),
                        high,
                    )
                )

        if expression.op in [">", ">="]:
            expression.subterms[0:split], expression.subterms[split:] = high, low
        else:
            expression.subterms[0:split], expression.subterms[split:] = low, high

    def random_shift_parameters(self, expression):
        sort = expression.subterms[0].type
        shift_amount_node = self.random_value_node(sort)
        shift_amount_node_nonneg = Expr("abs", [shift_amount_node], type=sort)
        shift_amount_node_nonpos = Expr(
            "-", [Expr("abs", [shift_amount_node], type=sort)], type=sort
        )
        shift_operator = random.choice(["-", "+"])
        split = random.randrange(1, len(expression.subterms))
        modify_low = random.choice([True, False])
        low, high = expression.subterms[0:split], expression.subterms[split:]
        if expression.op in [">", ">="]:
            # reverse low and high
            low, high = high, low

        return (
            shift_amount_node_nonpos,
            shift_amount_node_nonneg,
            shift_operator,
            low,
            high,
            modify_low,
        )

    def matches_RHS(self, expression):
        # TODO extend this class to support Reals
        return (
            expression.is_operator(">", ">=", "<", "<=")
            and expression.has_subterms()
            and expression.subterms[0].is_type("Int")
        )

    def to_LHS(self, expression):
        (
            shift_amount_node_nonpos,
            shift_amount_node_nonneg,
            shift_operator,
            low,
            high,
            modify_low,
        ) = self.random_shift_parameters(expression)

        # Determine target and shift amount sign based on random parameters chosen above
        target = low if modify_low else high
        choose_nonnegative = (modify_low and shift_operator == "+") or (
            not modify_low and shift_operator == "-"
        )
        shift_amount = (
            shift_amount_node_nonneg if choose_nonnegative else shift_amount_node_nonpos
        )

        for t in target:
            convert_to_node(t, Expr(shift_operator, [t, shift_amount], type=t.type))

    def matches_LHS(self, expression):
        # TODO extend this class to support Reals
        return (
            expression.is_operator(">", ">=", "<", "<=")
            and expression.has_subterms()
            and expression.subterms[0].is_type("Int")
        )

    def to_RHS(self, expression):
        (
            shift_amount_node_nonpos,
            shift_amount_node_nonneg,
            shift_operator,
            low,
            high,
            modify_low,
        ) = self.random_shift_parameters(expression)

        # Determine target and shift amount sign based on random parameters chosen above
        target = low if modify_low else high
        shift_amount = (
            shift_amount_node_nonpos
            if (
                (modify_low and shift_operator == "+")
                or (not modify_low and shift_operator == "-")
            )
            else shift_amount_node_nonneg
        )

        for t in target:
            convert_to_node(t, Expr(shift_operator, [t, shift_amount], type=t.type))


class NumberRelationShiftBalanced(Equivalence):
    def __init__(self):
        self.name = "NUMRELSHIFTBALANCED"
        super().__init__()

    def matches_LHS(self, expression):
        return (
            expression.is_operator(">", ">=", "=", "<", "<=", "distinct")
            and expression.has_subterms()
            and expression.subterms[0].is_type("Int")
        )

    def to_RHS(self, expression):
        sort = expression.subterms[0].type
        shift = self.random_value_node(sort)
        shift_operator = random.choice(["-", "+"])
        expression.subterms = list(
            map(
                lambda t: Expr(shift_operator, [t, shift], type=sort),
                expression.subterms,
            )
        )

    def matches_RHS(self, expression):
        return (
            expression.is_operator(">", ">=", "<", "<=")
            and expression.has_subterms()
            and expression.subterms[0].is_type("Int")
        )

    def to_LHS(self, expression):
        pass


class QuantifierSwap(Implication):
    def __init__(self):
        self.name = "QUANTSWP"
        super().__init__()

    def matches_LHS(self, expression):
        return expression.quantifier == "forall"

    def matches_RHS(self, expression):
        return expression.quantifier == "exists"

    def to_RHS(self, expression):
        expression.quantifier = "exists"

    def to_LHS(self, expression):
        expression.quantifier = "forall"


class UninterpretedFunctionEquality(Implication):
    def __init__(self):
        self.name = "UNINFUNEQ"
        super().__init__()

    def matches_LHS(self, expression):
        # TODO For cases with a sensible way of finding a random function to apply on the RHS we could do this case too
        # Probably most interesting if we take the AST-with-holes approach.
        return False

    def matches_RHS(self, expression):
        if expression.is_operator("=") and expression.has_subterms():
            f = expression.subterms[0].op
            if f and expression.subterms[0].has_subterms():
                fArity = len(expression.subterms[0].subterms)
                return all(
                    map(
                        lambda eqArg: eqArg.op == f and eqArg.has_n_subterms(fArity),
                        expression.subterms,
                    )
                )

        return False

    def to_LHS(self, expression):
        fArgSets = map(lambda eqArg: eqArg.subterms, expression.subterms)
        expression.op = "and"
        expression.subterms = list(
            map(lambda arg_ns: Expr("=", arg_ns), map(list, zip(*fArgSets)))
        )


class StringEqualityPrefixSuffix(Implication):
    def matches_LHS(self, expression):
        return (
            expression.is_operator("=")
            and expression.has_n_subterms(2)
            and expression.subterms[0].is_type("String")
        )

    def to_RHS(self, expression):
        expression.op = "and"
        expression.type = "Bool"
        [s1, s2] = expression.subterms
        expression.subterms = [
            Expr("str.prefixof", [s1, s2], type="Bool"),
            Expr("str.suffixof", [s1, s2], type="Bool"),
        ]


class StringEqualityPrefixPrefix(Equivalence):
    def matches_LHS(self, expression):
        return (
            expression.is_operator("=")
            and expression.has_n_subterms(2)
            and expression.subterms[0].type == "String"
        )

    def to_RHS(self, expression):
        expression.op = "and"
        expression.type = "Bool"
        [s1, s2] = expression.subterms
        expression.subterms = [
            Expr("str.prefixof", [s1, s2], type="Bool"),
            Expr("str.prefixof", [s2, s1], type="Bool"),
        ]


class StringEqualitySuffixSuffix(Equivalence):
    def matches_LHS(self, expression):
        return (
            expression.is_operator("=")
            and expression.has_n_subterms(2)
            and expression.subterms[0].type == "String"
        )

    def to_RHS(self, expression):
        expression.op = "and"
        expression.type = "Bool"
        [s1, s2] = expression.subterms
        expression.subterms = [
            Expr("str.suffixof", [s1, s2], type="Bool"),
            Expr("str.suffixof", [s2, s1], type="Bool"),
        ]


class StringContainsPrefixSuffix(Implication):
    def matches_RHS(self, expression):
        return expression.is_operator("str.contains")

    def to_LHS(self, expression):
        expression.op = "or"
        expression.type = "Bool"
        [s2, s1] = expression.subterms
        expression.subterms = [
            Expr("str.prefixof", [s1, s2], type="Bool"),
            Expr("str.suffixof", [s1, s2], type="Bool"),
        ]


class StringEqualityDistinctAppend(Implication):
    def matches_LHS(self, expression):
        return (
            expression.is_operator("=")
            and expression.has_n_subterms(2)
            and expression.subterms[0].is_type("String")
        )

    def to_RHS(self, expression):
        expression.op = "distinct"
        s1, s2 = expression.subterms
        x = StringConst(random.choice(string.ascii_letters))
        expression.subterms = [
            s1,
            Expr("str.++", [s2, self.random_value_node("String"), x], type="String"),
        ]


class StringPrefixToExists(Implication):
    def __init__(self):
        self.name = "STRPRETOEX"
        super().__init__()

    def matches_LHS(self, expression):
        return expression.is_operator("str.prefixof")

    def to_RHS(self, expression):
        [s1, s2] = expression.subterms

        var = fresh_var(expression)

        convert_node_to_quantifier(
            expression,
            "exists",
            ([var], ["Int"]),
            Expr(
                "=",
                [
                    Expr(
                        "str.substr",
                        [s2, Const("0", type="Int"), Var(var, type="Int")],
                        type="String",
                    ),
                    s1,
                ],
                type="Bool",
            ),
        )


class StringSuffixToExists(Implication):
    def matches_LHS(self, expression):
        return expression.is_operator("str.suffixof")

    def to_RHS(self, expression):
        [s1, s2] = expression.subterms

        var = fresh_var(expression)

        convert_node_to_quantifier(
            expression,
            "exists",
            ([var], ["Int"]),
            Expr(
                "=",
                [
                    Expr(
                        "str.substr",
                        [
                            s2,
                            Var(var, type="Int"),
                            Expr(
                                "-",
                                [
                                    Expr("str.len", [s2], type="Int"),
                                    Var(var, type="Int"),
                                ],
                                type="Int",
                            ),
                        ],
                        type="String",
                    ),
                    s1,
                ],
                type="Bool",
            ),
        )


class StringContainsToExists(Implication):
    def matches_LHS(self, expression):
        return expression.is_operator("str.contains")

    def to_RHS(self, expression):
        [s1, s2] = expression.subterms

        var1 = fresh_var(expression)
        var2 = fresh_var(expression, {var1})

        convert_node_to_quantifier(
            expression,
            "exists",
            ([var1, var2], ["Int", "Int"]),
            Expr(
                "=",
                [
                    Expr(
                        "str.substr",
                        [s1, Var(var1, type="Int"), Var(var2, type="Int")],
                        type="String",
                    ),
                    s2,
                ],
                type="Bool",
            ),
        )


class OrToIte(Implication):
    def __init__(self):
        self.name = "ORTOITE"

    def matches_LHS(self, expression):
        return expression.is_operator("or") and expression.has_at_least_n_subterms(2)

    def to_RHS(self, expression):
        split_index = random.randrange(1, len(expression.subterms))
        phis1, phis2 = (
            expression.subterms[:split_index],
            expression.subterms[split_index:],
        )
        phi1 = phis1[0] if len(phis1) == 1 else Expr("or", phis1, type="Bool")
        phi2 = phis2[0] if len(phis2) == 1 else Expr("or", phis2, type="Bool")
        var = fresh_var(expression)
        convert_node_to_quantifier(
            expression,
            "exists",
            ([var], ["Bool"]),
            Expr("ite", [Var(var, type="Bool"), phi1, phi2], type="Bool"),
        )


class IteToImpTrue(Implication):
    def __init__(self):
        self.name = "ITETOIMPTRUE"

    def matches_LHS(self, expression):
        return (
            expression.is_operator("ite")
            and expression.has_n_subterms(3)
            and expression.subterms[1].is_type("Bool")
        )

    def to_RHS(self, expression):
        b, phi1, phi2 = expression.subterms
        expression.op = "=>"
        expression.subterms = [b, phi1]


class IteToImpFalse(Implication):
    def __init__(self):
        self.name = "ITETOIMPFALSE"

    def matches_LHS(self, expression):
        return (
            expression.is_operator("ite")
            and expression.has_n_subterms(3)
            and expression.subterms[1].is_type("Bool")
        )

    def to_RHS(self, expression):
        b, phi1, phi2 = expression.subterms
        expression.op = "=>"
        expression.subterms = [Expr("not", [b], type="Bool"), phi2]


class ImpToIteTrue(Implication):
    def __init__(self):
        self.name = "IMPTOITETRUE"
        super().__init__()

    def matches_LHS(self, expression):
        return expression.is_operator(
            "implies", "=>"
        ) and expression.has_at_least_n_subterms(2)

    def to_RHS(self, expression):
        phi1, phi2, *phis = expression.subterms

        true = Const("true", type="Bool")

        expression.op = "ite"

        if len(phis) > 0:
            expression.subterms = [phi1, Expr("=>", [phi2, *phis], type="Bool"), true]
        else:
            expression.subterms = [phi1, phi2, true]


class ImpToIteFalse(Implication):
    def __init__(self):
        self.name = "IMPTOITEFALSE"

    def matches_LHS(self, expression):
        return expression.is_operator(
            "implies", "=>"
        ) and expression.has_at_least_n_subterms(2)

    def to_RHS(self, expression):
        phi1, phi2, *phis = expression.subterms

        true = Const("true", type="Bool")
        not_phi1 = Expr("not", [phi1], type="Bool")

        expression.op = "ite"

        if len(phis) > 0:
            expression.subterms = [
                not_phi1,
                true,
                Expr("=>", [phi2, *phis], type="Bool"),
            ]
        else:
            expression.subterms = [not_phi1, true, phi2]


class ImpLiftToForall(Implication):
    def __init__(self):
        self.name = "IMPLIFTTOFORALL"
        super().__init__()

    def matches_LHS(self, expression):
        return expression.is_operator(
            "implies", "=>"
        ) and expression.has_at_least_n_subterms(2)

    def to_RHS(self, expression):
        phis = expression.subterms

        b = fresh_var(expression)
        b_node = Var(b, type="Bool")

        body = Expr(
            "=>",
            list(map(lambda phi: Expr("and", [b_node, phi], type="Bool"), phis)),
            type="Bool",
        )

        convert_node_to_quantifier(expression, "forall", ([b], ["Bool"]), body)


class InstantiateQuantifier(Implication):
    def matches_LHS(self, expression):
        return expression.quantifier == "forall" and any(
            map(self.is_random_instantiatable, expression.quantified_vars[1])
        )

    def matches_RHS(self, expression):
        return expression.quantifier == "exists" and any(
            map(self.is_random_instantiatable, expression.quantified_vars[1])
        )

    """REMARK
    For this rule 'to_RHS' and 'to_LHS' are exactly the same, so we can just overwrite 'apply' instead.
    """

    def apply(self, expression, direction):

        body = expression.subterms[0]

        instantiatable_variables = [
            (var, sort, i)
            for i, (var, sort) in enumerate(zip(*expression.quantified_vars))
            if self.is_random_instantiatable(sort)
        ]

        qv, qsort, i = instantiatable_variables.pop()

        qv_nodes = body.free_variables().get(qv, [])

        replacee = self.random_value_node(qsort, qv)

        for qv_node in qv_nodes:
            convert_to_node(qv_node, replacee)

        expression.quantified_vars = (
            expression.quantified_vars[0][0:i] + expression.quantified_vars[0][i + 1 :],
            expression.quantified_vars[1][0:i] + expression.quantified_vars[1][i + 1 :],
        )

        if len(expression.quantified_vars[0]) == 0:
            convert_node_to_single_subterm(expression)


class RegexAppend(Implication):
    def matches_LHS(self, expression):
        return expression.op == "str.in_re"

    def to_RHS(self, expression):
        [s, re] = expression.subterms
        s_app = self.random_value_node("String")
        regex_meta.APP(re, s_app)
        expression.subterms = [Expr("str.++", [s, s_app], type="String"), re]


class DropConjunct(Implication):
    def matches_LHS(self, expression):
        return expression.is_operator("and") and expression.has_at_least_n_subterms(2)

    def to_RHS(self, expression):
        drop_index = random.randrange(len(expression.subterms))
        expression.subterms = (
            expression.subterms[0:drop_index] + expression.subterms[drop_index + 1 :]
        )

        if len(expression.subterms) == 1:
            convert_node_to_single_subterm(expression)

    def matches_RHS(self, expression):
        return True

    def to_LHS(self, expression):
        new_conj = self.random_value_node("Bool")
        expression_itself = copy.deepcopy(expression)
        convert_to_node(
            expression, Expr("and", [expression_itself, new_conj], type="Bool")
        )


class AddDisjunct(Implication):
    def __init__(self, formula_pool=None):
        self.name = "ADDDISJ"
        super().__init__(formula_pool)

    def matches_LHS(self, expression):
        return True

    def to_RHS(self, expression):
        new_disj = self.random_value_node("Bool")
        expression_itself = copy.deepcopy(expression)
        convert_to_node(
            expression, Expr("or", [expression_itself, new_disj], type="Bool")
        )

    def matches_RHS(self, expression):
        return expression.is_operator("or") and expression.has_at_least_n_subterms(2)

    def to_LHS(self, expression):
        drop_index = random.randrange(len(expression.subterms))
        expression.subterms = (
            expression.subterms[0:drop_index] + expression.subterms[drop_index + 1 :]
        )

        if len(expression.subterms) == 1:
            convert_node_to_single_subterm(expression)


class OrToImp(Implication):
    def matches_LHS(self, expression):
        return expression.has_n_subterms(2) and expression.is_operator("or")

    def matches_RHS(self, expression):
        return expression.has_n_subterms(2) and expression.is_operator("=>", "implies")

    def to_RHS(self, expression):
        expression.op = "=>"
        expression.subterms[0] = Expr("not", [expression.subterms[0]], type="Bool")

    def to_LHS(self, expression):
        expression.op = "or"
        expression.subterms[0] = Expr("not", [expression.subterms[0]], type="Bool")


class StringLeqApp(Implication):
    def __init__(self, formula_pool=None):
        self.name = "STRLEQAPP"
        super().__init__(formula_pool)

    def matches_LHS(self, expression):
        return expression.is_operator("str.<=")

    def to_RHS(self, expression):
        appendee = self.random_value_node("String")
        split = random.randrange(1, len(expression.subterms))
        expression.subterms = expression.subterms[0:split] + [
            Expr("str.++", [t, appendee], type="String")
            for t in expression.subterms[split:]
        ]


class StringLeqSubstr(Implication):
    def __init__(self, formula_pool=None):
        super().__init__(formula_pool)

    def matches_LHS(self, expression):
        return expression.is_operator("str.<=")

    def to_RHS(self, expression):
        split = random.randrange(1, len(expression.subterms))

        substr_index_maybe = self.random_value_node("Int")
        slen = lambda s: Expr("str.len", [s], type="Int")
        valid_substr_index = lambda s: Expr(
            "ite",
            [
                Expr(
                    "<=",
                    [
                        Const("0", type="Int"),
                        substr_index_maybe,
                        Expr("-", [slen(s), Const("1", type="Int")], type="Int"),
                    ],
                    type="Bool",
                ),
                substr_index_maybe,
                slen(s),
            ],
            type="Int",
        )

        expression.subterms = [
            Expr(
                "str.substr",
                [t, Const("0", type="Int"), valid_substr_index(t)],
                type="String",
            )
            for t in expression.subterms[:split]
        ] + expression.subterms[split:]


# ========================================================================
# TODO move these instantiations directly into the generator


def RelationPreservingAutomorphism(R, f, r):
    """
    A relation preserving automorphism is a homomorphism f:r|R -> s|S with:

    * R = S
    * r = s
    """
    return Homomorphism(R=R, r=r, S=R, s=r, f=f)
