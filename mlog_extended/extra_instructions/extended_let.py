"""Provide xlet instruction, a replacement of `op`, `set`, `sensor` and `getlink`."""
from .. import CompilationError

# From Mindustry 126.2
BINARY_OPERATORS = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "/": "div",
    "//": "idiv",
    "%": "mod",
    "**": "pow",
    "==": "equal",
    "!=": "notEqual",
    "&&": "land",
    "<": "lessThan",
    "<=": "lessThanEq",
    ">": "greaterThan",
    ">=": "greaterThanEq",
    "===": "strictEqual",
    "<<": "shl",
    ">>": "shr",
    "|": "or",
    "&": "and",
    "^": "xor"
}

BINARY_ASSIGNERS = {
    "max": "max",
    "min": "min",
    "angle": "angle",
    "len": "len",
    "noise": "noise",
}

UNARY_ASSIGNERS = {
    "not": "not",
    "abs": "abs",
    "log": "log",
    "log10": "log10",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "floor": "floor",
    "ceil": "ceil",
    "sqrt": "sqrt",
    "rand": "rand",
    # Custom assigners
    "~": "not",
    "ln": "log",
    "lg": "log10"
}

def unary_xlet(verdicts: list) -> list:
    """xlet for unary operators and assignments."""
    line = ""
    if verdicts[2] == "=":
        # variable assignment, 'set' in Mindustry logic
        lvalue, rvalue = verdicts[1], verdicts[3]
        line = F"set {lvalue} {rvalue}"

    verdicts[2] = verdicts[2].strip("=")
    if verdicts[2] in UNARY_ASSIGNERS.keys():
        vanilla_assigner = UNARY_ASSIGNERS[verdicts[2]]
        lvalue, rvalue = verdicts[1], verdicts[3]
        line = F"op {vanilla_assigner} {lvalue} {rvalue} 0"
    elif verdicts[2] in BINARY_OPERATORS.keys():
        vanilla_operator = BINARY_OPERATORS[verdicts[2]]
        lvalue, rvalue = verdicts[1], verdicts[3]
        line = F"op {vanilla_operator} {lvalue} {lvalue} {rvalue}"
    elif verdicts[2] == "getlink":
        lvalue, link_id = verdicts[1], verdicts[3]
        line = F"getlink {lvalue} {link_id}"
    if len(line) > 0:
        return [line, ]
    message = F"error: unsupported operator '{verdicts[2]}'"
    if verdicts[2] in BINARY_ASSIGNERS.keys():
        message = F"error: too few argument for '{verdicts[2]}'"
    raise CompilationError(message)

def extended_let(src_line: str) -> list:
    """
    C-sytle operators for Mindustry logic. Use '**' for pow/exponetia.
    Usage:
    xlet a = b
    xlet a1 = b + c
    xlet a1 += 3
    xlet a1 = 2 ** 8
    xlet a2 min c d
    xlet a2 =min c d
    xlet a2 =~ x
    xlet a2 floor x
    xlet a3 = b / c
    xlet a4 = b // c
    xlet x =sensor @unit @x
    xlet building =getlink 1
    """
    verdicts = src_line.split()
    if len(verdicts) == 2:
        return []
    if len(verdicts) == 4:
        result = unary_xlet(verdicts)
        return result
    if len(verdicts) == 5:
        verdicts[2] = verdicts[2].lstrip("=")
        line = ""
        if verdicts[2] in BINARY_ASSIGNERS.keys():
            vanilla_assigner = BINARY_ASSIGNERS[verdicts[2]]
            lvalue, arg1, arg2 = verdicts[1], verdicts[3], verdicts[4]
            line = F"op {vanilla_assigner} {lvalue} {arg1} {arg2}"
        elif verdicts[2] == "sensor":
            lvalue, target, attribute = verdicts[1], verdicts[3], verdicts[4]
            line = F"sensor {lvalue} {target} {attribute}"
        if len(line) > 0:
            return [line, ]
        message = F"error: unsupported operator '{verdicts[2]}'"
        raise CompilationError(message)

    if len(verdicts) == 6:
        if verdicts[4] in BINARY_OPERATORS.keys():
            vanilla_operator = BINARY_OPERATORS[verdicts[4]]
            lvalue, arg1, arg2 = verdicts[1], verdicts[3], verdicts[5]
            line = F"op {vanilla_operator} {lvalue} {arg1} {arg2}"
            return [line, ]

        message = F"error: unsupported binary operator '{verdicts[4]}'"
        raise CompilationError(message)

    message = F"error: too {'few' if len(verdicts)<6 else 'many'}"
    message += F"arguments ({len(verdicts)}) for xlet"
    raise CompilationError(message)
