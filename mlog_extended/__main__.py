import argparse
import sys
from . import BasicCompiler
from . import ExtendedCompiler
from . import ProceduralCompiler
from . import BasicDecompiler

parser = argparse.ArgumentParser(description="Extended Minductry Logic Compiler.",
        epilog="- stands for standard input/output")
parser.add_argument('input_file', type=str,
        help="Input file, like source code.")
parser.add_argument('output_file', type=str,
        help="Output file, usually vanilla mindustry logic code.")
parser.add_argument('--basic', '-b', action='store_true',
        help="Use basic compiler only (xjump instruction)")
parser.add_argument('--extended', '-e', action='store_true',
        help="Use extended compiler")
parser.add_argument('--procedural', '-p', action='store_true',
        help="Use procedural compiler (default)")
parser.add_argument('--dump', '-D', action='store_true',
        help="For procedural compiler, process if-else and while-wend only.")
parser.add_argument('--decompile', '-d', action='store_true',
        help="Decompile vanilla Mindustry logic to MlogExtended code")


def openfile(filename: str, mode: str, default=None):
    if filename == "-":
        if default is None:
            raise ValueError
        return default
    return open(filename, mode, encoding="utf-8")

if __name__ == '__main__':
    args = parser.parse_args()
    CompilerClass = ProceduralCompiler
    if args.basic:
        CompilerClass = BasicCompiler
    elif args.extended:
        CompilerClass = ExtendedCompiler
    elif args.decompile:
        CompilerClass = BasicDecompiler
    compiler = CompilerClass()

    with openfile(args.input_file, 'r', sys.stdin) as f_in:
        source_code = f_in.read()
        result = ""
        if args.dump:
            result = compiler.compile_to_backend(source_code)
        else:
            result = compiler.compile(source_code)
        with openfile(args.output_file, 'w', sys.stdout) as f_out:
            f_out.write(result)
