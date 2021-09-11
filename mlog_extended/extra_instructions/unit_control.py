from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, pad_args

TOTAL_VERDICTS = 7

COMMAND_ARGS = {
    "idle": (),
    "stop": (),
    "move": ("x", "y"),
    "approach": ("x", "y", "radius"),
    "boost": ("enable", ),
    "pathfind": (),
    "target": ("x", "y", "shoot"),
    "targetp": ("unit", "shoot"),
    "itemDrop": ("to", "amount"),
    "itemTake": ("from", "item", "amount"),
    "payDrop": (),
    "payTake": ("takeUnits", ),
    "mine": ("x", "y"),
    "flag": ("value", ),
    "build": ("x", "y", "block", "rotation", "config"),
    "getBlock": ("x", "y", "type", "building"),
    "within": ("x", "y", "radius", "result"),
}

COMMAND_ARG_ALIASES = {
    "boost": {
        "boost": "enable",
    },
    "targetp": {
        "target": "unit",
    },
    "flag": {
        "flag": "value",
    },
    "getBlock": {
        "resultType": "type",
        "resultBuilding": "building",
    },
}

def unit_control(src_line: str) -> list:
    """Enhanced unit control instruction, with Python-style kwargs.
    """
    verdicts = src_line.split()
    command = verdicts[1]
    kwargs = parse_kwargs(verdicts[2:])
    result = []

    try:
        if command not in COMMAND_ARGS.keys():
            message = F"error: unsupported unit command '{command}'"
            raise CompilationError(message)

        vanilla_kwargs = []
        if command in COMMAND_ARG_ALIASES.keys():
            aliases = COMMAND_ARG_ALIASES[command]
            for alias in aliases.keys():
                if alias in kwargs.keys():
                    vanilla_kwargs.append((aliases[alias], kwargs[alias]))
        for (k, v) in vanilla_kwargs:
            kwargs[k] = v

        output_verdicts = []
        output_verdicts.append("ucontrol")
        output_verdicts.append(command)
        for key in COMMAND_ARGS[command]:
            output_verdicts.append(kwargs[key])
        output_verdicts = pad_args(output_verdicts, TOTAL_VERDICTS)
        result.append(" ".join(output_verdicts))
    except KeyError as exception:
        name = ""
        if len(exception.args) >= 1:
            name = exception.args[0]
        message = F"error: argument '{name}' is required, but not found"
        raise CompilationError(message) from exception

    return result
