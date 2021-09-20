# Solver commands
Z3_NEW = 'PATH_TO_Z3_NEW -smt2'
Z3_OLD = 'PATH_TO_Z3_OLD -smt2'
CVC5_NEW = 'PATH_TO_CVC5_NEW -q --strings-exp --lang=smt2'
CVC5_OLD = 'PATH_TO_CVC5_OLD -q --strings-exp --lang=smt2'

# Path to seeds directory, can have any hierarchy inside.
# We try to determine satisfiability based on the path, e.g. 'SEED_DIR/.../sat/.../file.smt2 will be labelled as satisfiable.
SEED_DIR = ''

# Each instance will run at most one solver as subprocess at any time,
# so this option roughly produces in 2*MAX_NUM_INSTANCES processes.
MAX_NUM_INSTANCES = 40

# This produces roughly MAX_NUM_REDUCERS*NUM_PROCS_PER_REDUCER processes.
MAX_NUM_REDUCERS = 5
NUM_PROCS_PER_REDUCER = 10

# Janus parameters
ITERATIONS = 300
WALK_LENGTH = 20
RULE_SET = 'all'

# Solver timeout used for fuzzing and reducing
SOLVER_TIMEOUT = 10
TIMEOUT_PER_INSTANCE = f"{str(ITERATIONS*SOLVER_TIMEOUT)}s"
TIMEOUT_PER_REDUCER = '1h'


