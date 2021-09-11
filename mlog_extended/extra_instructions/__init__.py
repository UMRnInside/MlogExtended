from .jump_if import jump_if
from .extended_let import extended_let
from .unit_control import unit_control
from .radars import general_radar
from .unit_locate import unit_locate
from .control import control

def comment(src_line: str) -> list:
    """Returns an empty list."""
    return []


INSTRUCTIONS = {
    # Yes, comments are instructions
    "#": comment,
    "jump-if": jump_if,
    "xlet": extended_let,
    "unit-control": unit_control,
    "unit-radar": general_radar,
    "unit-locate": unit_locate,
    "xradar": general_radar,
    "xcontrol": control,
}
