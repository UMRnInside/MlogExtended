from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, apply_aliases

ARGS = ("filter1", "filter2", "filter3", "sort", "from", "order", "output")
FILTER_NAMES = ("filter1", "filter2", "filter3")
ARG_ALIASES = {
    "target": "filter1",
    "orderBy": "sort",
    "asc": "order",
    "result": "output",
}
SOURCE_IS_UNIT = "__SOURCE_IS_UNIT"

def general_radar(src_line: str) -> list:
    """Enhanced unit radar instruction, with Python-style kwargs.
    """
    verdicts = src_line.split()
    kwargs = parse_kwargs(verdicts[1:])
    kwargs = apply_aliases(kwargs, ARG_ALIASES)

    for filter_id in FILTER_NAMES:
        if filter_id not in kwargs.keys():
            kwargs[filter_id] = "any"

    output_verdicts = []
    if "unit" in src_line:
        output_verdicts.append("uradar")
        kwargs["from"] = "0"
    else:
        output_verdicts.append("radar")

    try:
        for arg in ARGS:
            output_verdicts.append(kwargs[arg])
    except KeyError as exception:
        name = exception.args[0]
        message = F"error: argument '{name}' is required, but not found"
        raise CompilationError(message) from exception
    return [" ".join(output_verdicts), ]
