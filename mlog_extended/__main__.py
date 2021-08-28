import argparse
import sys
from . import BasicCompiler
from . import ExtendedCompiler

parser = argparse.ArgumentParser(description="Extended Minductry Logic Compiler.",
        epilog="- stands for standard input/output")
parser.add_argument('input_file', type=str,
        help="Input file, like source code.")
parser.add_argument('output_file', type=str,
        help="Output file, usually vanilla mindustry logic code.")
parser.add_argument('--basic', '-b', action='store_true',
        help="Use basic compiler only (xjump instruction)")
parser.add_argument('--extended', '-e', action='store_true',
        help="Use extended compiler (default)")

def openfile(filename: str, mode: str, default=None):
    if filename == "-":
        if default is None:
            raise ValueError
        return default
    return open(filename, mode, encoding="utf-8")

if __name__ == '__main__':
    args = parser.parse_args()
    CompilerClass = ExtendedCompiler
    if args.basic:
        CompilerClass = BasicCompiler
    compiler = CompilerClass()

    with openfile(args.input_file, 'r', sys.stdin) as f_in:
        with openfile(args.output_file, 'w', sys.stdout) as f_out:
            source_code = f_in.read()
            f_out.write(compiler.compile(source_code))
