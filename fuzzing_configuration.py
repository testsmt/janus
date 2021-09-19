Z3_NEW = '/local/home/maurob/impbased-fuzzing-experiments/solvers/z3/build/z3 -smt2'
Z3_OLD = '/local/home/maurob/impbased-fuzzing-experiments/solvers/z3-4.8.12/build/z3 -smt2'
CVC5_NEW = '/local/home/maurob/impbased-fuzzing-experiments/solvers/cvc4/build/bin/cvc5 -q --strings-exp --lang=smt2'
CVC5_OLD = '/local/home/maurob/impbased-fuzzing-experiments/solvers/cvc4-1.8 -q --strings-exp --lang=smt2'

SEED_DIR = '/local/home/maurob/impbased-fuzzing-experiments/semantic-fusion-seeds/'
MAX_NUM_INSTANCES = 40
MAX_NUM_REDUCERS = 5
NUM_PROCS_PER_REDUCER = 10
SOLVER_TIMEOUT = 10
ITERATIONS = 300
WALK_LENGTH = 20
TIMEOUT_PER_INSTANCE = f"{str(ITERATIONS*SOLVER_TIMEOUT)}s"
TIMEOUT_PER_REDUCER = '1h'
RULE_SET = 'all'
OUTPUT_WIDTH = 80
