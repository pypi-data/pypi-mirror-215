
import subprocess
import os

def main():
    cmd = f'python -m pip install -e /Users/dy/codeforces'
    subprocess.run(cmd.split(), check=True)