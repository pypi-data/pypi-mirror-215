import os
import codecontest as cc
from codecontest.cpprun import *
from codecontest.cppast import *
import sys

def sample_in_file(source_file):
    return os.path.join(os.path.dirname(source_file), 'sample.in')

def sample_out_file(source_file):
    return os.path.join(os.path.dirname(source_file), 'sample.out')

def cpp_source_file(dir=os.getcwd()):
    if os.path.isfile(dir):
        return dir
    return os.path.join(dir, 'sol.cpp')

def cpp_binary_file(source_file):
    return os.path.join(os.path.dirname(source_file), f'{source_file}.bin')

def cpp_include_path():
    return os.path.join(os.path.dirname(cc.__file__), 'include')

def str_shrink(s):
    return ''.join(s.split())

def ifnull(obj, val):
    return val if obj is None else obj

def err_msg(s):
    CRED = '\033[91m'
    CEND = '\033[0m'
    print(f'{CRED}{s}{CEND}', file=sys.stderr)

MAIN_NAMESPACE = "main_namespace"

import time
class Timer(object):
    def __init__(self, name=None, enable=True):
        self.name = name
        self.enable = enable

    def __enter__(self):
        if self.enable:
            self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.enable:
            err_msg(f'Elapsed {(time.time() - self.tstart)}s of {self.name}')

# SAMPLE_INPUT = 'sample_in'
# SAMPLE_OUTPUT = 'sample_out'
# SAMPLE_OUTPUT = os.path.join(os.path.dirname(cc.__file__), 'sample_out')