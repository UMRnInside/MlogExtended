from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs

TOTAL_VERDICTS = 7

def pad_args(src: list) -> list:
    """Pad extra args with 0."""
    padding_count = TOTAL_VERDICTS - len(src)
    result = []
    result.extend(src)
    result.extend(["0",]*padding_count)
    return result

def command_idle(kwargs: dict) -> list:
    idle_commands = ["ucontrol", "idle"]
    return pad_args(idle_commands)

def command_stop(kwargs: dict) -> list:
    commands = ["ucontrol", "stop"]
    return pad_args(commands)

def command_move(kwargs: dict) -> list:
    commands = ["ucontrol", "move"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    return pad_args(commands)

def command_approach(kwargs: dict) -> list:
    commands = ["ucontrol", "approach"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    commands.append(kwargs["radius"])
    return pad_args(commands)

def command_boost(kwargs: dict) -> list:
    commands = ["ucontrol", "boost"]
    commands.append(kwargs["enable"])
    return pad_args(commands)

def command_pathfind(kwargs: dict) -> list:
    commands = ["ucontrol", "pathfind"]
    return pad_args(commands)

def command_target(kwargs: dict) -> list:
    commands = ["ucontrol", "target"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    commands.append(kwargs["shoot"])
    return pad_args(commands)

def command_targetp(kwargs: dict) -> list:
    commands = ["ucontrol", "targetp"]
    commands.append(kwargs["unit"])
    commands.append(kwargs["shoot"])
    return pad_args(commands)

def command_itemdrop(kwargs: dict) -> list:
    commands = ["ucontrol", "itemDrop"]
    commands.append(kwargs["to"])
    commands.append(kwargs["amount"])
    return pad_args(commands)

def command_itemtake(kwargs: dict) -> list:
    commands = ["ucontrol", "itemTake"]
    commands.append(kwargs["from"])
    commands.append(kwargs["item"])
    commands.append(kwargs["amount"])
    return pad_args(commands)

def command_paydrop(kwargs: dict) -> list:
    commands = ["ucontrol", "payDrop"]
    return pad_args(commands)

def command_paytake(kwargs: dict) -> list:
    commands = ["ucontrol", "payTake"]
    commands.append(kwargs["takeUnits"])
    return pad_args(commands)

def command_mine(kwargs: dict) -> list:
    commands = ["ucontrol", "mine"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    return pad_args(commands)

def command_flag(kwargs: dict) -> list:
    commands = ["ucontrol", "flag"]
    commands.append(kwargs["value"])
    return pad_args(commands)

def command_build(kwargs: dict) -> list:
    commands = ["ucontrol", "build"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    commands.append(kwargs["block"])
    commands.append(kwargs["rotation"])
    commands.append(kwargs["config"])
    return pad_args(commands)

def command_getblock(kwargs: dict) -> list:
    commands = ["ucontrol", "getBlock"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    commands.append(kwargs["type"])
    commands.append(kwargs["building"])
    return pad_args(commands)

def command_within(kwargs: dict) -> list:
    commands = ["ucontrol", "within"]
    commands.append(kwargs["x"])
    commands.append(kwargs["y"])
    commands.append(kwargs["radius"])
    commands.append(kwargs["result"])
    return pad_args(commands)

COMMANDS = {
    "idle": command_idle,
    "stop": command_stop,
    "move": command_move,
    "approach": command_approach,
    "boost": command_boost,
    "pathfind": command_pathfind,
    "target": command_target,
    "targetp": command_targetp,
    "itemDrop": command_itemdrop,
    "itemTake": command_itemtake,
    "payDrop": command_paydrop,
    "payTake": command_paytake,
    "mine": command_mine,
    "flag": command_flag,
    "build": command_build,
    "getBlock": command_getblock,
    "within": command_within
}

def unit_control(src_line: str) -> list:
    """Enhanced unit control instruction, with Python-style kwargs.
    """
    verdicts = src_line.split()
    command = verdicts[1]
    kwargs = parse_kwargs(verdicts[2:])
    result = []

    try:
        if command not in COMMANDS.keys():
            message = F"error: unsupported unit command '{command}'"
            raise CompilationError(message)
        parser_function = COMMANDS[command]
        result.append(" ".join(parser_function(kwargs)))
    except KeyError as exception:
        name = ""
        if len(exception.args) >= 1:
            name = exception.args[0]
        message = F"error: argument '{name}' is required, but not found"
        raise CompilationError(message) from exception

    return result
