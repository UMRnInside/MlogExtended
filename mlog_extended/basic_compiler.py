from .compilation_error import CompilationError

class BasicCompiler:
    """Basic compiler, supports xjump instruction."""
    def __init__(self):
        self.external_instructions = {}

    def add_instruction(self, instruction: str, handler):
        if instruction.startswith(":"):
            raise ValueError("Instructions that start with ':' is disallowed.")
        self.external_instructions[instruction] = handler

    def compile(self, src_text: str, sep='\n') -> str:
        code_lines = src_text.splitlines()
        code_lines = self.convert_externals(code_lines)

        code_lines, tags = parse_tags(code_lines)
        code_lines = convert_xjumps(code_lines, tags)
        code_lines = replace_tag_counter_macros(code_lines, tags)
        return sep.join(code_lines) + sep

    def convert_externals(self, src_lines: list) -> list:
        """Convert added instructions, remove empty lines, etc."""
        dst_lines = []
        for (src_cursor, src_line) in enumerate(src_lines):
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
            except CompilationError as exception:
                ext_info = ""
                if len(exception.args) > 0:
                    ext_info = " ".join(exception.args)

                message = F"line {src_cursor+1}: {ext_info}"
                raise CompilationError(message) from exception
        return dst_lines

def convert_xjumps(src_lines: list, dst_tagged: dict) -> list:
    dst_lines = []

    for (src_cursor, src_line) in enumerate(src_lines):
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
        except KeyError as exception:
            if len(exception.args) >= 1:
                message = F"line {src_cursor+1}: error: No such tag '{exception.args[0]}'"
                raise CompilationError(message) from exception
            raise exception

    return dst_lines

def parse_tags(src_lines: list) -> tuple:
    """Parse tags.
    If there are any tags at the end, an no-op instruction will be added.
    """
    dst_tagged = {}
    dst_lines = []

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

def replace_tag_counter_macros(src_lines: list, tags: dict) -> list:
    """Trivial __TAG_COUNTER macro processor.
Replace __TAG_COUNTER(tag_name) with corresponding destination code @counter.
"""
    result = []
    MACRO_HEADER = "__TAG_COUNTER("
    MACRO_HEADER_LEN = len(MACRO_HEADER)
    for (src_cursor, src_line) in enumerate(src_lines):
        verdicts = src_line.split()
        new_verdicts = []
        for arg in verdicts:
            if not arg.startswith(MACRO_HEADER) or not arg.endswith(")"):
                new_verdicts.append(arg)
                continue
            tag_name = arg[MACRO_HEADER_LEN:-1]
            try:
                tag_line = tags[tag_name]
                new_verdicts.append(str(tag_line))
            except KeyError as exception:
                if len(exception.args) >= 1:
                    message = F"line {src_cursor+1}: error: No such tag '{exception.args[0]}'"
                    raise CompilationError(message) from exception
                raise exception
        result.append(" ".join(new_verdicts))
    return result
