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
    node.type = 'Bool'


def convert_node_to_single_subterm(node):
    node.__dict__ = node.subterms[0].__dict__.copy()

def convert_to_node(target, source):
    target.__dict__ = copy.deepcopy(source.__dict__.copy())

