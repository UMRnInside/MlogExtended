from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, apply_aliases, pad_args

TOTAL_VERDICTS = 7

ACTION_ALIASES = {
    "toggle": "enabled",
    "config": "configure",
}

ACTION_ARGS = {
    "enabled": ("status", ),
    "shoot": ("x", "y", "shoot"),
    "shootp": ("unit", "shoot"),
    "configure": ("config", ),
    "color": ("r", "g", "b"),
}

ACTION_ARG_ALIASES = {
    "shootp": {
        "target": "unit",
    },
}

def control(src_line: str) -> list:
    """Enhanced control instruction, with Python-style kwargs.
    Examples:
    # Disable a generator
    xcontrol generator1 action=toggle status=0
    xcontrol generator1 action=enabled status=0
    # Control a cyclone (turret), using argument aliases(unit vs target)
    xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=1
    xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=0
    xcontrol cyclone1 action=shootp unit=enemy shoot=1
    xcontrol cyclone1 action=shootp target=enemy shoot=1
    # Config a sorter to sort different items
    xcontrol sorter1 action=configure config=@copper
    xcontrol sorter1 action=config config=@lead
    # Set illuminator's color
    xcontrol illuminator1 action=color r=255 g=153 b=0
    """
    verdicts = src_line.split()
    target_building = verdicts[1]
    kwargs = parse_kwargs(verdicts[2:])

    result = []

    try:
        action = kwargs["action"]
        if action in ACTION_ALIASES.keys():
            action = ACTION_ALIASES[action]
        if action not in ACTION_ARGS.keys():
            message = F"error: unsupported control action '{action}'"
            raise CompilationError(message)
        if action in ACTION_ARG_ALIASES.keys():
            kwargs = apply_aliases(kwargs, ACTION_ARG_ALIASES[action])

        output_verdicts = []
        output_verdicts.append("control")
        output_verdicts.append(action)
        output_verdicts.append(target_building)
        for key in ACTION_ARGS[action]:
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
