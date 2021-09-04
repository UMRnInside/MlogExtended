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
    "<=": "lessTnanEq",
    ">": "greaterThan",
    ">=": "greaterTnanEq",
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

def extended_let(src_line: str) -> list:
    """
    C-sytle operators for Mindustry logic. Use '**' for pow/exponetia.
    Usage:
    xlet a = b
    xlet a1 = b + c
    xlet a1 = 2 ** 8
    xlet a2 min c d
    xlet a2 =min c d
    xlet a2 =~ x
    xlet a2 floor x
    xlet x =sensor @unit @x
    """
    verdicts = src_line.split()
    if len(verdicts) == 2:
        return []
    if len(verdicts) == 4:
        output_verdicts = []
        if verdicts[2] == "=":
            # variable assignment, 'set' in Mindustry logic
            output_verdicts.append("set")
            output_verdicts.append(verdicts[1])
            output_verdicts.append(verdicts[3])
            line = " ".join(output_verdicts)
            return [line, ]

        verdicts[2] = verdicts[2].lstrip("=")
        if verdicts[2] in UNARY_ASSIGNERS.keys():
            vanilla_assigner = UNARY_ASSIGNERS[verdicts[2]]
            output_verdicts.append("op")
            output_verdicts.append(vanilla_assigner)
            output_verdicts.append(verdicts[1])
            output_verdicts.append(verdicts[3])
            output_verdicts.append("0")
            line = " ".join(output_verdicts)
            return [line, ]

        message = F"error: unsupported operator '{verdicts[2]}'"
        if verdicts[2] in BINARY_ASSIGNERS.keys():
            message = F"error: too few argument for '{verdicts[2]}'"
        raise CompilationError(message)

    if len(verdicts) == 5:
        output_verdicts = []
        if verdicts[2] in BINARY_ASSIGNERS.keys():
            vanilla_assigner = BINARY_ASSIGNERS[verdicts[2]]
            output_verdicts.append("op")
            output_verdicts.append(vanilla_assigner)
            output_verdicts.append(verdicts[1])
            output_verdicts.append(verdicts[3])
            output_verdicts.append(verdicts[4])
            line = " ".join(output_verdicts)
            return [line, ]
        # Use sensor command
        verdicts[2] = verdicts[2].lstrip("=")
        if verdicts[2] == "sensor":
            output_verdicts.append("sensor")
            output_verdicts.append(verdicts[1])
            output_verdicts.extend(verdicts[3:5])
            line = " ".join(output_verdicts)
            return [line, ]
        message = F"error: unsupported operator '{verdicts[2]}'"
        raise CompilationError(message)

    if len(verdicts) == 6:
        output_verdicts = []
        if verdicts[4] in BINARY_OPERATORS.keys():
            vanilla_operator = BINARY_OPERATORS[verdicts[4]]
            output_verdicts.append("op")
            output_verdicts.append(vanilla_operator)
            output_verdicts.append(verdicts[1])
            output_verdicts.append(verdicts[3])
            output_verdicts.append(verdicts[5])
            line = " ".join(output_verdicts)
            return [line, ]

        message = F"error: unsupported binary operator '{verdicts[4]}'"
        raise CompilationError(message)

    message = F"error: too {'few' if len(verdicts)<6 else 'many'}"
    message += "arguments ({len(verdicts)}) for xlet"
    raise CompilationError(message)
