import os
import subprocess
from fuzzing_configuration import *

# results from fuzzing
BUG_DIR = './bugs/'

# for temporary files created during reduction
REDUCING_DIR = './reducing/'

class Reducer():

    def __init__(self, bug_file_name):
        self.original_bug_file_path = f"{BUG_DIR}/{bug_file_name}"
        self.reducing_file_path = f"{REDUCING_DIR}/{bug_file_name}"
        self.proc = None
        self.reducer_proc_desc = None

    def start(self):
        os.rename(self.original_bug_file_path, self.original_bug_file_path + ".orig")
        self.proc = subprocess.Popen([ 'timeout', TIMEOUT_PER_REDUCER ] + self.reducer_proc_desc, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def is_finished(self):
        return self.proc is not None and self.proc.poll() is not None

    # Return type is reducer specific
    def get_result(self):
        pass

class RegressionReducer(Reducer):

    def __init__(self, original_bug_file, solver_new, solver_old):
        super().__init__(original_bug_file)
        self.solver_new = solver_new
        self.solver_old = solver_old
        self.reducer_proc_desc = ['ddsmt', '-j', str(NUM_PROCS_PER_REDUCER), '-v', '--ignore-output', self.original_bug_file_path + ".orig", self.reducing_file_path, './bin/check-regression.py', str(SOLVER_TIMEOUT), self.solver_old, self.solver_new ]



class ImplicationReducer(Reducer):

    # original_bug_file = Decided formula from an implication incompleteness,
    #                     i.e. from which an incompleteness can be derived in one step.
    def __init__(self, original_bug_file, solver, rule_name):
        super().__init__(original_bug_file)
        self.rule_name = rule_name
        self.solver = solver
        self.rule_name = rule_name

        self.reducer_proc_desc = ['ddsmt', '-j', str(NUM_PROCS_PER_REDUCER), '-v', '--ignore-output', self.original_bug_file_path + ".orig", self.reducing_file_path, './bin/check-implication.py', str(SOLVER_TIMEOUT), self.solver, self.rule_name ]



