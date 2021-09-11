from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, apply_aliases

ARGS = ("filter1", "filter2", "filter3", "order", "sort", "output")
FILTER_NAMES = ("filter1", "filter2", "filter3")
ARG_ALIASES = {
    "target": "filter1",
    "orderBy": "order",
    "asc": "sort",
}

def unit_radar(src_line: str) -> list:
    """Enhanced unit radar instruction, with Python-style kwargs.
    """
    verdicts = src_line.split()
    kwargs = parse_kwargs(verdicts[1:])
    kwargs = apply_aliases(kwargs, ARG_ALIASES)

    for filter_id in FILTER_NAMES:
        if filter_id not in kwargs.keys():
            kwargs[filter_id] = "any"

    output_verdicts = ["uradar", ]
    try:
        for arg in ARGS:
            output_verdicts.append(kwargs[arg])
    except KeyError as exception:
        name = exception.args[0]
        message = F"error: argument '{name}' is required, but not found"
        raise CompilationError(message) from exception
    return [" ".join(output_verdicts), ]
