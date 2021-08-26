from ..compilation_error import CompilationError

# From Mindustry 126.2
COMPARATORS = {
    "===": "strictEqual",
    "==": "equal",
    "!=": "notEqual",
    "<": "lessThan",
    "<=": "lessThanEq",
    ">": "greaterThan",
    ">=": "greaterThanEq",
    "always": "always"
}

def jump_if(src_line: str) -> list:
    """Usage:
    jump-if <Tag> always
    jump-if <Tag> x <= 42
    """
    result = []
    verdicts = src_line.split()
    # Supported by BasicCompiler
    verdicts[0] = "xjump"

    if len(verdicts) == 3:
        if verdicts[2] == "always":
            verdicts.extend(("0", "0"))
            line = " ".join(verdicts)
            result.append(line)
            return result
        raise CompilationError("error: too few arguments for jump-if")
    if len(verdicts) < 3:
        raise CompilationError("error: too few arguments for jump-if")
    if len(verdicts) == 4:
        raise CompilationError("error: invalid or incomplete arguments for jump-if")
    if len(verdicts) > 5:
        raise CompilationError("error: too many arguments for jump-if")

    (verdicts[2], verdicts[3]) = (verdicts[3], verdicts[2])
    try:
        verdicts[2] = COMPARATORS[verdicts[2]]
    except KeyError as exception:
        raise CompilationError(F"error: '{verdicts[2]}' is not supported") from  exception
    line = " ".join(verdicts)
    result.append(line)
    return result
