from src.parsing.Ast import Expr
import copy

def APP(re, s):
    if re.op == 'str.to_re':
        re.subterms = [Expr('str.++', [re.subterms[0], s], type='String')]
    elif re.op in ['re.union', 're.inter', 're.diff', 're.opt']:
        for t in re.subterms:
            APP(t,  s)
    elif re.op == 're.++':
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
        re.op = 're.++'
        re.subterms = [re_itself, Expr('str.to_re', [s], type='RegLan')]
