from .extra_instructions.jump_if import COMPARATORS

DECOMPILER_TAG_PREFIX = "L"

class BasicDecompiler:
    def __init__(self):
        self.line_tags = {}
        self.jump_if_mapping = {}
        for (k, v) in COMPARATORS.items():
            self.jump_if_mapping[v] = k

    def decompile(self, src_text:str, sep='\n') -> str:
        src_lines = src_text.splitlines()
        dst_lines = []
        self._parse_jumps(src_lines)
        for line_number, src_line in enumerate(src_lines):
            if line_number in self.line_tags.keys():
                tag_name = ":" + self.line_tags[line_number]
                dst_lines.append(tag_name)
            if src_line.startswith("jump"):
                dst_lines.append(self._convert_jump(src_line))
            else:
                dst_lines.append(src_line)
        return sep.join(dst_lines)

    def compile(self, src_text:str, sep='\n') -> str:
        return self.decompile(src_text, sep)

    def _parse_jumps(self, src_lines:list) -> None:
        for line_number, src_line in enumerate(src_lines):
            verdicts = src_line.split()
            if len(verdicts) == 0:
                continue
            if verdicts[0] == "jump":
                tag_name = DECOMPILER_TAG_PREFIX + verdicts[1]
                self.line_tags[line_number] = tag_name

    def _convert_jump(self, src_line:str) -> str:
        verdicts = src_line.split()
        dst_line_number = int(verdicts[1])
        dst_tag = self.line_tags[dst_line_number]
        comparator = self.jump_if_mapping[verdicts[2]]
        if comparator == "always":
            return F"jump-if {dst_tag} always"
        return F"jump-if {dst_tag} {verdicts[3]} {comparator} {verdicts[4]}"
