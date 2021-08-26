"""An Extended basic compiler."""
from .basic_compiler import BasicCompiler
from .extra_instructions import INSTRUCTIONS

class ExtendedCompiler(BasicCompiler):
    """Similar to BasicCompiler, but support more instructions."""
    def __init__(self):
        super().__init__()
        for (instruction, handler) in INSTRUCTIONS.items():
            self.add_instruction(instruction, handler)
