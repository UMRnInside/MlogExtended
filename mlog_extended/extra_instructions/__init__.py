from .jump_if import jump_if
from .extended_let import extended_let
from .unit_control import unit_control
from .unit_radar import unit_radar

def comment(src_line: str) -> list:
    """Returns an empty list."""
    return []


INSTRUCTIONS = {
    # Yes, comments are instructions
    "#": comment,
    "jump-if": jump_if,
    "xlet": extended_let,
    "unit-control": unit_control,
    "unit-radar": unit_radar,
}
