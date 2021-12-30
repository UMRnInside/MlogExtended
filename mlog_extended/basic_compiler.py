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
        code_mappings = list(enumerate(src_text.splitlines()))
        return self.compile_with_mappings(code_mappings, sep)

    def compile_with_mappings(self, src_mappings: list, sep='\n'):
        code_mappings = self.convert_externals(src_mappings)

        code_mappings, tags = parse_tags(code_mappings)
        code_mappings = convert_xjumps(code_mappings, tags)
        code_mappings = replace_tag_counter_macros(code_mappings, tags)
        code_lines = [ codemap[1] for codemap in code_mappings ]
        return sep.join(code_lines) + sep

    def convert_externals(self, src_mappings: list) -> list:
        """Convert added instructions, remove empty lines, etc."""
        dst_mappings = []
        for (src_cursor, src_line) in src_mappings:
            src_line = src_line.strip().rstrip()
            try:
                verdicts = src_line.split()
                if verdicts[0] in self.external_instructions.keys():
                    handler = self.external_instructions[verdicts[0]]
                    handler_result = handler(src_line)
                    dst_mappings.extend([(src_cursor, code) for code in handler_result])
                else:
                    # Pass them as-is
                    # They can be vanilla-mlog instructions ,xjump or tag
                    dst_mappings.append((src_cursor, src_line))
            except IndexError:
                # verdicts[0]
                pass
            except CompilationError as exception:
                ext_info = ""
                if len(exception.args) > 0:
                    ext_info = " ".join(exception.args)
                message = F"line {src_cursor+1}: {ext_info}"
                raise CompilationError(message) from exception
        return dst_mappings

def convert_xjumps(src_mappings: list, dst_tagged: dict) -> list:
    """Convert xjumps, xjumps are always inline, keep mappings."""
    dst_mappings = []

    for (src_cursor, src_line) in src_mappings:
        try:
            verdicts = src_line.split()
            if verdicts[0] == "xjump":
                tag_name = verdicts[1]
                real_destination = dst_tagged[tag_name]

                # Mindustry logic instruction
                verdicts[0] = "jump"
                verdicts[1] = str(real_destination)

                dst_mappings.append((src_cursor ," ".join(verdicts) ))
            else:
                dst_mappings.append((src_cursor, src_line))
        except KeyError as exception:
            if len(exception.args) >= 1:
                message = F"line {src_cursor+1}: error: No such mlogex tag '{exception.args[0]}'"
                raise CompilationError(message) from exception
            raise exception

    return dst_mappings

def parse_tags(src_mappings: list) -> tuple:
    """Parse tags.
    If there are any tags at the end, an no-op instruction will be added.
    """
    dst_tagged = {}
    dst_mappings = []

    dst_cursor = 0
    last_tagged_line = -1
    last_source_line = -1

    for (src_cursor, src_line) in src_mappings:
        try:
            # One line, one tag
            # But you can apply multiple tags on one destination line
            verdicts = src_line.split()
            last_source_line = src_cursor
            if verdicts[0].startswith(":"):
                tag_name = verdicts[0][1:]
                dst_tagged[tag_name] = dst_cursor
                last_tagged_line = dst_cursor
            else:
                dst_mappings.append((src_cursor, src_line.lstrip().rstrip()))
                dst_cursor += 1
        except IndexError:
            # Possibly empty lines
            pass

    if last_tagged_line == len(dst_mappings):
        dst_mappings.append((last_source_line+1, "end"))
    return (dst_mappings, dst_tagged)

def replace_tag_counter_macros(src_mappings: list, tags: dict) -> list:
    """Trivial __TAG_COUNTER macro processor.
Replace __TAG_COUNTER(tag_name) with corresponding destination code @counter.
"""
    result = []
    MACRO_HEADER = "__TAG_COUNTER("
    MACRO_HEADER_LEN = len(MACRO_HEADER)
    for (src_cursor, src_line) in src_mappings:
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
        result.append((src_cursor, " ".join(new_verdicts)))
    return result
