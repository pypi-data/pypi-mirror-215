import codecontest as cc
import subprocess
import os, argparse, sys

def cpp_ast(source_file):
    inn_prefix = '#include "'
    sys_prefix = '#include <'
    sys_prefix_list = []
    use_prefix = "using namespace std;\n"
    def concat(source_file, level=0):
        lines = []
        with open(source_file) as f:
            for line in f.readlines():
                if (line.strip().startswith(inn_prefix)):
                    lines += concat(f'{cc.cpp_include_path()}/{line.strip()[len(inn_prefix):-1]}', level + 1)
                elif (line.strip().startswith(sys_prefix)):
                    sys_prefix_list.append(line)
                    continue
                elif (line.strip().startswith(use_prefix)):
                    continue
                else:
                    lines.append(line)
        return lines
    
    concat_file = '/tmp/concat.cpp'
    preprocess_file = '/tmp/preprocess.cpp'
    concat_lines = concat(source_file)
    with open(concat_file, 'w') as f:
        f.write(f'namespace {cc.MAIN_NAMESPACE} '+ '{\n')
        for line in concat_lines:
            f.write(line)
        f.write('\n}\n')

    # with open(concat_file, 'w') as f:
    #     print(f.read())
    # print('------------------------------------------')
    
    # macro substitution (aka. after preprocessing)
    preprocess_cmd = ["clang++", "-E", "-std=c++20", '-o', preprocess_file, concat_file]
    subprocess.run(preprocess_cmd)

    # with open(preprocess_file, 'w') as pf:
    #     print(pf.read())

    with open(concat_file, 'w') as f:
        f.writelines(sys_prefix_list)
        f.write(use_prefix)
        with open(preprocess_file, 'r') as pf:
            f.write(pf.read())

    ast_cmd = ["clang++", f"-I{cc.cpp_include_path()}", "-std=c++20", "-Xclang", "-ast-dump=json", "-Xclang", "-ast-dump-filter", "-Xclang", cc.MAIN_NAMESPACE, concat_file]
    past = subprocess.run(ast_cmd, check=False, capture_output=True)
    str_ast = str(past.stdout, encoding='utf-8')
    # hack...
    if sys.platform == 'darwin':
        str_ast = ''.join(['[', str_ast.replace('}\n{', '},{'), ']'])
    else:
        ast_lines = str_ast.split('\n')
        for (idx, line) in enumerate(ast_lines):
            if (line.startswith('Dumping ')):
                ast_lines[idx] = '[\n' if idx == 0 else ',\n'
        ast_lines.append(']\n')
        str_ast = ''.join(ast_lines)

    return str_ast, concat_file
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    args = parser.parse_args()
    str_ast, _ = cpp_ast(os.path.abspath(args.source_file))
    print(str_ast)