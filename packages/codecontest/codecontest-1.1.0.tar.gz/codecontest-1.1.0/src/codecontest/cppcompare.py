import os
import io
import pandas as pd
import argparse
import sys
import codecontest as cc
import itertools
import signal

def cpp_compare():
    outs = []
    n = 0

    def ctrl_c_handler(sig, frame):
        cc.err_msg(f'All {n} tests passed.')
        sys.exit(0)
    signal.signal(signal.SIGINT, ctrl_c_handler)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('baseline')
    parser.add_argument('generator', nargs='?')
    args = parser.parse_args()
    source = os.path.abspath(args.source_file)
    baseline = os.path.abspath(args.baseline)

    if args.generator is not None:
        generator = os.path.abspath(args.generator)
        generator, source, baseline = map(cc.cpp_compile, [generator, source, baseline])
        while True:
            input_str = cc.cpp_run(generator, input_str=None, capture_output=True)
            out = cc.cpp_run(source, input_str, True, tic_name=source, tic_enable=True)
            out_baseline = cc.cpp_run(baseline, input_str, True, tic_name=baseline, tic_enable=True)
            out_verdict, ok = result_compare(out, out_baseline)
            outs.clear()
            outs += out_verdict
            if not ok:
                cc.err_msg('======INPUT=====')
                cc.err_msg(input_str)
                cc.err_msg('======END=======')
                break
            n += 1
            if (n % 100 == 0):
                cc.err_msg(f'{n} tests passed.')

    else:
        input_str = ''.join((input_line for input_line in sys.stdin))
        out_program = cc.cpp_compile(source_file=source, debug=False)
        out = cc.cpp_run(out_program=out_program, input_str=input_str, capture_output=True, tic_name=source, tic_enable=True)
        out_baseline = None
        if baseline.endswith('.cpp'):
            out_program_baseline = cc.cpp_compile(source_file=baseline, debug=False)
            out_baseline = cc.cpp_run(out_program=out_program_baseline, input_str=input_str, capture_output=True, tic_name=baseline, tic_enable=True)
        else:
            with open(baseline) as f:
                out_baseline = f.read()
        outs += result_compare(out, out_baseline)[0]
    
    df = pd.DataFrame(outs, columns=['Verdict', 'Output', 'Expected'])
    cc.err_msg(df.to_string())
    cc.err_msg(f'Total {len(df[df["Verdict"] == "AC"])}/{len(outs)} lines passed.')

class str_tokens:
    def __init__(self, str):
        self.tokens = str.split() if str is not None else None
    def __iter__(self):
        return self
    def __next__(self):
        if not self.tokens:
            raise StopIteration
        return self.tokens.pop(0)

class file_lines:
    def __init__(self, file):
        self.file = file
        self.line = ''
    def __iter__(self):
        return self
    def __next__(self):
        self.line = self.file.readline()
        if not self.line:
            raise StopIteration
        return self.line

def result_compare(out, out_baseline):
    def ok_str(ok):
        return 'AC' if ok else 'WA'
    def out_str(s):
        return '' if s is None else s.rstrip()
    res = []
    all_ok = True
    if out is None:
        all_ok = False
        res.append((ok_str(False), out_str(out), out_str(out_baseline)))
    elif out_baseline is None:
        all_ok = True
        res.append((ok_str(True), out_str(out), out_str(out_baseline)))
    else:
        with io.StringIO(out) as out, io.StringIO(out_baseline) as out_baseline:
            for line, line_baseline in itertools.zip_longest(file_lines(out), file_lines(out_baseline)):
                line_ok = True
                for token, token_baseline in itertools.zip_longest(str_tokens(line), str_tokens(line_baseline)):
                    token = cc.ifnull(token, '')
                    token_baseline = cc.ifnull(token_baseline, '')
                    if '.' in token and not token.startswith('"') and not token.endswith('"'):
                        line_ok &= abs(float(token), float(token_baseline))
                    else:
                        line_ok &= token == token_baseline
                    if not line_ok:
                        all_ok = False
                res.append((ok_str(line_ok), out_str(line), out_str(line_baseline)))     
                        # break
    return res, all_ok

