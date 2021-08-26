from .jump_if import jump_if
from .extended_let import extended_let

INSTRUCTIONS = {
    "jump-if": jump_if,
    "xlet": extended_let
}
