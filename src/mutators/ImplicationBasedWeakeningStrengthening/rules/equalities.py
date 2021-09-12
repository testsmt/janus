from src.mutators.ImplicationBasedWeakeningStrengthening.rules.lhs_rhs import (
    Equivalence,
)
from src.mutators.ImplicationBasedWeakeningStrengthening.common import convert_to_node
from src.parsing.Ast import Const, Expr, StringConst


class Equality(Equivalence):

    nonBool = True

    def __init__(self, name):
        self.name = f"EQUAL[{name}]"
        super().__init__()

    def matches_LHS(self, expression):
        False

    def matches_RHS(self, expression):
        False


class EmptyStringReplace(Equality):
    """
    "" = (str.replace "" _ "")
    """

    def __init__(self):
        super().__init__("EMPTYSTRREP")

    def matches_LHS(self, expression):
        if expression.name == '""':
            return True

    def matches_RHS(self, expression):
        if expression.is_operator("str.replace"):
            if expression.has_n_subterms(3):
                if expression.subterms[0].name == '""':
                    if expression.subterms[2].name == '""':
                        return True

    def to_LHS(self, expression):
        convert_to_node(expression, Const('""', type="String"))

    def to_RHS(self, expression):
        s = self.random_value_node("String")
        e = Expr(
            "str.replace",
            [Const('""', type="String"), s, Const('""', type="String")],
            type="String",
        )
        convert_to_node(expression, e)


class StringPrependToEmptyReplace(Equality):
    """
    (str.++ s1 s2) = (str.replace s2 "" s1)
    """

    def __init__(self):
        super().__init__("STRPRETOEMPTREP")

    def matches_LHS(self, expression):
        return expression.is_operator("str.++") and expression.has_at_least_n_subterms(
            2
        )

    def matches_RHS(self, expression):
        return (
            expression.is_operator("str.replace")
            and expression.subterms[1].is_const
            and expression.subterms[1].name == '""'
        )

    def to_RHS(self, expression):
        [s1, s2, *sRest] = expression.subterms
        s1s2 = Expr("str.replace", [s2, Const('""', type="String"), s1], type="String")
        if len(sRest) == 0:
            convert_to_node(expression, s1s2)
        else:
            convert_to_node(expression, Expr("str.++", [s1s2] + sRest, type="String"))

    def to_LHS(self, expression):
        [s2, _, s1] = expression.subterms
        convert_to_node(expression, Expr("str.++", [s1, s2], type="String"))


class StringToInt(Equality):
    """
    For any a sequence of digits N:

        N = (str.to_int "N")
    """

    def __init__(self):
        super().__init__("STRTOINT")

    def matches_LHS(self, expression):
        if expression.is_const:
            return expression.name.isdigit()

    def matches_RHS(self, expression):
        return (
            expression.is_operator("str.to_int")
            and expression.subterms[0].is_const
            and expression.subterms[0].name[1:-1].isdigit()
        )

    def to_RHS(self, expression):
        convert_to_node(
            expression,
            Expr("str.to_int", [StringConst(expression.name)], type="String"),
        )

    def to_LHS(self, expression):
        convert_to_node(
            expression, Const(expression.subterms[0].name[1:-1], type="Int")
        )
