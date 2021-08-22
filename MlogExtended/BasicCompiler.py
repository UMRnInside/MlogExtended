import sys
from collections.abc import Callable

TaggedLines = dict[str, int]
ParserOutput = tuple[list, TaggedLines]
InstructionHandler = Callable[[str], list[str]]

class CompilationError(BaseException):
    pass


class BasicCompiler:
    """Basic compiler, supports xjump instruction."""
    def __init__(self):
        self.external_instructions = {}
        pass

    def add_instruction(self, instruction: str, handler: InstructionHandler):
        if instruction.startswith(":"):
            raise ValueError("Instructions that start with ':' is disallowed.")
        self.external_instructions[instruction] = handler

    def compile(self, src_text: str, sep='\n') -> str:
        code_lines = src_text.splitlines()
        code_lines = self.convert_externals(code_lines)
        code_lines = self.convert_xjump_and_tags(code_lines)
        return sep.join(code_lines) + sep

    def convert_externals(self, src_lines: list[str]) -> list[str]:
        """Convert added instructions, remove empty lines, etc."""
        dst_lines = []
        for src_line in src_lines:
            src_line = src_line.strip().rstrip()
            try:
                verdicts = src_line.split()
                if verdicts[0] in self.external_instructions.keys():
                    handler = self.external_instructions[verdicts[0]]
                    dst_lines.extend(handler(src_line))
                else:
                    # Pass them as-is
                    # They can be vanilla-mlog instructions ,xjump or tag
                    dst_lines.append(src_line)
            except IndexError:
                # verdicts[0]
                pass
        return dst_lines


    def convert_xjump_and_tags(self, src_lines: list[str]) -> list[str]:
        (phase1_lines, dst_tagged) = ParseTags(src_lines)
        dst_lines = []

        for (src_cursor, src_line) in enumerate(phase1_lines):
            try:
                verdicts = src_line.split()
                if verdicts[0] == "xjump":
                    tag_name = verdicts[1]
                    real_destination = dst_tagged[tag_name]

                    # Mindustry logic instruction
                    verdicts[0] = "jump"
                    verdicts[1] = str(real_destination)

                    dst_lines.append(" ".join(verdicts))
                else:
                    dst_lines.append(src_line)
            except IndexError:
                raise
            except KeyError as e:
                if len(e.args) >= 1:
                    message = F"line {src_cursor}: error: No such tag '{e.args[0]}'"
                    raise CompilationError(message)
                raise e

        return dst_lines


def ParseTags(src_lines: list) -> ParserOutput:
    """Parse tags.
    If there are any tags at the end, an no-op instruction will be added.
    """
    dst_tagged = {}
    dst_lines = []

    src_tail = len(src_lines)
    dst_cursor = 0
    last_tagged_line = 0

    for src_line in src_lines:
        try:
            # One line, one tag
            # But you can apply multiple tags on one destination line
            verdicts = src_line.split()
            if verdicts[0].startswith(":"):
                tag_name = verdicts[0][1:]
                dst_tagged[tag_name] = dst_cursor
                last_tagged_line = dst_cursor
            else:
                dst_lines.append(src_line.lstrip().rstrip())
                dst_cursor += 1
        except IndexError:
            # Possibly empty lines
            pass

    if last_tagged_line == len(dst_lines):
        dst_lines.append("end")
    return (dst_lines, dst_tagged)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(F"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    compiler = BasicCompiler()

    input_file = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1], 'r')
    output_file = sys.stdout if sys.argv[2] == "-" else open(sys.argv[2], 'w')
    try:
        result = compiler.compile(input_file.read())
        output_file.write(result)
    finally:
        output_file.close()
        input_file.close()


