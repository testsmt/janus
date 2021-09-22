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
from src.mutators.ImplicationBasedWeakeningStrengthening.rules.all import ALL_RULES

predefined_rule_set_names = {
    'operator-replacement': {
        'OPREP_STR_EQ_LEQ',
        'OPREP_STR_EQ_PREFIX',
        'OPREP_STR_EQ_SUFFIX',
        'OPREP_STR_EQ_CONTAINS',
        'OPREP_STR_LE_LEQ',
        'OPREP_STR_LE_DIST',
        'OPREP_STR_PREFIX_LEQ',
        'OPREP_STR_PREFIX_CONTAINS',
        'OPREP_STR_SUFFIX_CONTAINS',
        'OPREP_RE_PLUS_STAR',
        'OPREP_RE_INTER_UNION',
        'OPREP_NUM_EQ_GEQ',
        'OPREP_NUM_GE_GEQ',
        'OPREP_NUM_LE_LEQ',
        'OPREP_NUM_EQ_LEQ',
        'OPREP_NUM_GE_DIST',
        'OPREP_NUM_LE_DIST',
        'OPREP_AND_OR',
        'OPREP_XOR_OR',
    },
    'core-logic': {
        'ORTOIMP',
        'ADDDISJ',
        'DROPCONJ',
        'INSTQUANT',
        'IMPLIFTTOFORALL',
        'IMPTOITEFALSE',
        'IMPTOITETRUE',
        'ITETOIMPFALSE',
        'ITETOIMPTRUE',
        'ORTOITE',
        'QUANTSWP',
        'OPREP_AND_OR',
        'OPREP_XOR_OR',
    },
    'reglan': {
        'REGEXAPP',
        'OPREP_RE_PLUS_STAR',
        'OPREP_RE_INTER_UNION',
        'RE_DISTRIBUTE_UNION_CONCAT',
        'RE_CHANGE_RANGE',
        'RE_UNION_IDEMPOTENT',
        'RE_INTER_IDEMPOTENT',
        'RE_ADD_LOOP',
        'RE_ADD_OPT',
        'RE_ADD_PLUS',
        'RE_CONCAT_TO_OPTION_POWER',
        'RE_ADD_FREE_UNION',
    },
}

predefined_rule_set_names['basic'] = (
    predefined_rule_set_names['operator-replacement']
    | predefined_rule_set_names['core-logic']
) - {'INSTQUANT'}

# Returns a set of strings to be used as keys into 'RuleSet'
def parseRuleSet(rule_set):
    if not rule_set:
        return set(RuleSet.keys())

    rule_set = rule_set.strip()
    if rule_set == 'all':
        return set(RuleSet.keys())

    if rule_set in predefined_rule_set_names:
        return predefined_rule_set_names[rule_set]

    if rule_set in RuleSet.keys():
        return {rule_set}

    raise Exception(f'Not a valid rule set: {rule_set}')
