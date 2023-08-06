import os
import codecontest as cc
import shutil as shell

def ccclean():
    for (root, dirs, files) in os.walk(os.path.dirname(cc.__file__)):
        for file in files:
            if file.endswith(('.bin', '.so', 'inlined.cpp')):
                f = os.path.join(root, file)
                os.remove(f)
                print(f'Removed file {f}')
        for d in dirs:
            if d.endswith(('.dSYM',)):
                f = os.path.join(root, d)
                shell.rmtree(f)
                print(f'Removed dir {f}')