import os
import io
import argparse
import sys
import subprocess
import codecontest as cc
import itertools

def cpp_compile(source_file, debug=False):
    out_program = cc.cpp_binary_file(source_file)
    cmd = f'clang++ -std=c++20 -O2 -I{cc.cpp_include_path()} -o {out_program} {source_file}'
    if debug:
        cmd = f'clang++ -g -std=c++20 -Wall -DDEBUG -fsanitize=address -I{cc.cpp_include_path()} -o {out_program} {source_file}'
    subprocess.run(cmd.split(), check=True)
    return out_program

def cpp_run(out_program, input_str, capture_output, timeout=10, tic_name='cpp', tic_enable=False):
    try:
        with cc.Timer(tic_name, tic_enable):
            prun = subprocess.run([f'{out_program}'], check=True, input=input_str, encoding='utf-8', capture_output=capture_output, timeout=timeout)
    # except subprocess.TimeoutExpired: # -O2 may substitue some dead loop with signal trap on macos clang
    except Exception as e:
        cc.err_msg(e)
        return ''
    return prun.stdout

# def cpp_compile_and_run(source_file, input_str=None, debug=False, capture_output=True, is_main=True):
#     out_program = cpp_compile(source_file, debug=debug)
#     if is_main:
#         with cc.Timer():
#             out = cpp_run(out_program, input_str, capture_output)
#     else:
#             out = cpp_run(out_program, input_str, capture_output)
#     return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    source_file = os.path.abspath(args.source_file)
    # input_str = ''.join((input_line for input_line in sys.stdin))
    out_program = cpp_compile(source_file=source_file, debug=args.debug)
    cpp_run(out_program=out_program, input_str=None, capture_output=False, tic_name=source_file, tic_enable=True)