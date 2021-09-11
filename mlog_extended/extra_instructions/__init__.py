from .jump_if import jump_if
from .extended_let import extended_let
from .unit_control import unit_control
from .unit_radar import unit_radar
from .unit_locate import unit_locate

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
    "unit-locate": unit_locate,
}
