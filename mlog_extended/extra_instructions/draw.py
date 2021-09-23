from ..compilation_error import CompilationError
from .kwargs_parser import parse_kwargs, apply_aliases, pad_args

TOTAL_VERDICTS = 8

ACTION_ALIASES = {
    "rectangle": "rect",
    "lineRectangle": "lineRect",
    "polygon": "poly",
    "linePolygon": "linePoly",
}

ACTION_ARGS = {
    "clear": ("r", "g", "b"),
    "stroke": ("width", ),
    "color": ("r", "g", "b"),
    "line": ("x", "y", "x2", "y2"),
    "rect": ("x", "y", "width", "height"),
    "lineRect": ("x", "y", "width", "height"),
    "poly": ("x", "y", "sides", "radius", "rotation"),
    "linePoly": ("x", "y", "sides", "radius", "rotation"),
    "image": ("x", "y", "image", "size", "rotation"),
    "triangle": ("x", "y", "x2", "y2", "x3", "y3"),
}

ARG_ALIASES = {
    "x1": "x",
    "y1": "y",
}

def convert_rgb(kwargs: dict) -> dict:
    if "rgb" not in kwargs.keys():
        return kwargs
    color_rgb = int(kwargs["rgb"], 16)
    kwargs["r"] = str((color_rgb >> 16) & 0xFF)
    kwargs["g"] = str((color_rgb >> 8) & 0xFF)
    kwargs["b"] = str((color_rgb >> 0) & 0xFF)
    return kwargs

def draw(src_line: str) -> list:
    """Enhanced draw instruction, with Python-style kwargs.
    Examples:
    # Clear display, using material gray color #373737
    xdraw clear r=55 g=55 b=55
    xdraw clear rgb=0x373737
    # Set stroke width
    xdraw stroke width=1
    # Set color to #FF9100
    xdraw color rgb=0xFF9100
    # Draw a line
    xdraw line x=3 y=1 x2=3 y2=80
    xdraw line x1=3 y1=1 x2=3 y2=80
    # Draw a rectangle
    xdraw rect x1=5 y1=5 height=5 width=10
    # Draw a line rectangle
    xdraw lineRect x1=15 y1=5 height=5 width=10
    # Draw a pentagon
    xdraw poly x=20 y=40 sides=5 radius=10 rotation=0
    # Draw a triangle
    xdraw triangle x1=30 y1=30 x2=20 y2=30 x3=20 y3=20
    # Draw a cyclone
    xdraw color rgb=FFFFFF
    xdraw image x=60 y=60 image=@cyclone size=40 rotation=0
    # Flush
    drawflush display1
    """
    verdicts = src_line.split()
    action = verdicts[1]
    kwargs = parse_kwargs(verdicts[2:])
    kwargs = convert_rgb(kwargs)
    result = []

    try:
        if action in ACTION_ALIASES.keys():
            action = ACTION_ALIASES[action]
        if action not in ACTION_ARGS.keys():
            message = F"error: unsupported xdraw action '{action}'"
            raise CompilationError(message)
        kwargs = apply_aliases(kwargs, ARG_ALIASES)

        output_verdicts = []
        output_verdicts.append("draw")
        output_verdicts.append(action)
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
