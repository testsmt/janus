# Solver commands
Z3_NEW = 'z3 -smt2'
Z3_OLD = '/home/mauro/desktop/scrap/z3-4.8.10-x64-ubuntu-18.04/bin/z3 -smt2'
CVC5_NEW = '/home/mauro/opensource/cvc5/build/bin/cvc5 -q --strings-exp --lang=smt2'
CVC5_OLD = '/home/mauro/opensource/cvc4-1.8 -q --strings-exp --lang=smt2'

# Path to seeds directory, can have any hierarchy inside.
# We try to determine satisfiability based on the path, e.g. 'SEED_DIR/.../sat/.../file.smt2 will be labelled as satisfiable.
SEED_DIR = '/home/mauro/desktop/semantic-fusion-seeds'

# Each instance will run at most one solver as subprocess at any time,
# so this option roughly produces in 2*MAX_NUM_INSTANCES processes.
MAX_NUM_INSTANCES = 0

# This produces roughly MAX_NUM_REDUCERS*NUM_PROCS_PER_REDUCER processes.
MAX_NUM_REDUCERS = 1
NUM_PROCS_PER_REDUCER = 1

# Janus parameters
ITERATIONS = 300
WALK_LENGTH = 20
RULE_SET = 'all'

# Solver timeout used for fuzzing and reducing
SOLVER_TIMEOUT = 10
TIMEOUT_PER_INSTANCE = f"{str(ITERATIONS*SOLVER_TIMEOUT)}s"
TIMEOUT_PER_REDUCER = '1h'


