from .extra_instructions.jump_if import COMPARATORS
from .extra_instructions.extended_let import BINARY_OPERATORS
from .extra_instructions.extended_let import BINARY_ASSIGNERS
from .extra_instructions.extended_let import UNARY_ASSIGNERS

DECOMPILER_TAG_PREFIX = "L"

class BasicDecompiler:
    def __init__(self):
        self.line_tags = {}
        self.jump_if_mapping = get_reversed_mapping(COMPARATORS)
        self.xlet_convertor = XletConvertor()

    def decompile(self, src_text:str, sep='\n') -> str:
        src_lines = src_text.splitlines()
        dst_lines = []
        self._parse_jumps(src_lines)
        for line_number, src_line in enumerate(src_lines):
            if line_number in self.line_tags.keys():
                tag_name = ":" + self.line_tags[line_number]
                dst_lines.append(tag_name)
            instruction = src_line.split(None, 1)[0]
            if instruction == "jump":
                dst_lines.append(self._convert_jump(src_line))
            elif instruction in self.xlet_convertor.handlers.keys():
                dst_lines.append(self.xlet_convertor.convert(src_line))
            else:
                dst_lines.append(src_line)
        return sep.join(dst_lines)

    def compile(self, src_text:str, sep='\n') -> str:
        return self.decompile(src_text, sep)

    def _parse_jumps(self, src_lines:list) -> None:
        for src_line in src_lines:
            verdicts = src_line.split()
            if len(verdicts) == 0:
                continue
            if verdicts[0] == "jump":
                tag_name = DECOMPILER_TAG_PREFIX + verdicts[1]
                line_number = int(verdicts[1])
                self.line_tags[line_number] = tag_name

    def _convert_jump(self, src_line:str) -> str:
        verdicts = src_line.split()
        dst_line_number = int(verdicts[1])
        dst_tag = self.line_tags[dst_line_number]
        comparator = self.jump_if_mapping[verdicts[2]]
        if comparator == "always":
            return F"jump-if {dst_tag} always"
        return F"jump-if {dst_tag} {verdicts[3]} {comparator} {verdicts[4]}"

class XletConvertor:
    """Convert op, set, sensor and getlink to xlet."""
    xlet = "xlet"
    def __init__(self):
        self.binary_assigners = get_reversed_mapping(BINARY_ASSIGNERS)
        self.unary_assigners = get_reversed_mapping(UNARY_ASSIGNERS)
        self.binary_operators = get_reversed_mapping(BINARY_OPERATORS)
        self.handlers = {
            "op": self.convert_op,
            "set": self.convert_set,
            "getlink": self.convert_getlink,
            "sensor": self.convert_sensor,
        }

    def convert(self, src_line: str) -> str:
        verdicts = src_line.split()
        result = ""
        try:
            handle = self.handlers[verdicts[0]]
            result = handle(verdicts)
        except IndexError:
            pass
        return result

    def convert_op(self, verdicts: list) -> str:
        action, destination = verdicts[1:3]
        value_a, value_b = verdicts[3:5]
        if action in self.binary_assigners.keys():
            xlet_action = self.binary_assigners[action]
            return F"xlet {destination} ={xlet_action} {value_a} {value_b}"
        if action in self.binary_operators.keys():
            xlet_action = self.binary_operators[action]
            return F"xlet {destination} = {value_a} {xlet_action} {value_b}"
        if action in self.unary_assigners.keys():
            xlet_action = self.unary_assigners[action]
            return F"xlet {destination} ={xlet_action} {value_a}"
        return " ".join(verdicts)

    def convert_set(self, verdicts: list) -> str:
        lvalue, rvalue = verdicts[1:3]
        return F"xlet {lvalue} = {rvalue}"

    def convert_getlink(self, verdicts: list) -> str:
        lvalue, link_number = verdicts[1:3]
        return F"xlet {lvalue} =getlink {link_number}"

    def convert_sensor(self, verdicts: list) -> str:
        lvalue, being_sensed, attribute = verdicts[1:4]
        return F"xlet {lvalue} =sensor {being_sensed} {attribute}"

def get_reversed_mapping(raw_mapping: dict) -> dict:
    """Get "reversed" mapping, work on dictionaries."""
    reversed_mapping = {}
    for key, value in raw_mapping.items():
        reversed_mapping[value] = key
    return reversed_mapping
