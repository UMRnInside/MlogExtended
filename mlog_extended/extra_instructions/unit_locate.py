from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, apply_aliases

ARGS = ("find", "group", "enemy", "ore", "outX", "outY", "found", "building")
ARG_ALIASES = {
    "type": "find",
    "isEnemy": "enemy",
    "oreType": "ore",
    "resultX": "outX",
    "resultY": "outY",
    "resultFound": "found",
    "resultIsFound": "found",
    "resultBuilding": "building",
}

def unit_locate(src_line: str) -> list:
    """Enhanced unit locate instruction, with Python-style kwargs.
    Example:
    unit-locate type=ore oreType=@coal resultX=x resultY=y resultIsFound=found
    unit-locate type=building group=core isEnemy=false outX=x outY=y found=found building=core
    # Aliases
    unit-locate find=building group=core enemy=false outX=x outY=y found=found building=core
    unit-locate type=spawn resultX=x resultY=y resultIsFound=found building=building
    unit-locate type=damaged outX=x outY=y resultIsFound=found resultBuilding=building
    """
    verdicts = src_line.split()
    kwargs = parse_kwargs(verdicts[1:])
    kwargs = apply_aliases(kwargs, ARG_ALIASES)

    if kwargs["find"] == "ore":
        kwargs["group"] = "core"
        kwargs["enemy"] = "false"
        kwargs["building"] = "0"
    elif kwargs["find"] == "building":
        kwargs["ore"] = "0"
    elif kwargs["find"] == "spawn" or kwargs["find"] == "damaged":
        kwargs["group"] = "core"
        kwargs["enemy"] = "false"
        kwargs["ore"] = "0"
    else:
        message = F"error: type '{kwargs['find']}' is not supported"
        raise CompilationError(message)

    output_verdicts = ["ulocate", ]
    try:
        for arg in ARGS:
            output_verdicts.append(kwargs[arg])
    except KeyError as exception:
        name = exception.args[0]
        message = F"error: argument '{name}' is required, but not found"
        raise CompilationError(message) from exception
    return [" ".join(output_verdicts), ]
