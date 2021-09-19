"""Vanilla Mindustry logic support "function calling" by setting @counter.
However, vanilla Mindustry logic has neither stack nor namespace.
"Functions" may accidentally overwrite variables outside of them.
This module provides a thin wrapper for function calls ans returns.
"""
from ..compilation_error import CompilationError

def unsafe_call(src_line: str) -> list:
    """Provide __unsafe_call instruction. Will assign a variable to store return address.
    DOES NOT SUPPORT RECURSION!
    Usage:
    __unsafe_call SomeTag
    Note:
    The instruction above assigns an variable "SomeTag_return_address"
    """
    result = []
    verdicts = src_line.split()

    if len(verdicts) < 2:
        raise CompilationError("error: too few arguments for __unsafe_call")
    if len(verdicts) > 2:
        raise CompilationError("error: too many arguments for __unsafe_call")

    target_tag = verdicts[1]
    return_address_variable = target_tag + "_return_address"
    result.append(F"op add {return_address_variable} @counter 1")
    result.append(F"xjump {target_tag} always 0 0")
    return result

def unsafe_return(src_line: str) -> list:
    """Provide __unsafe_return instruction. Return to previously assigned return address.
    Usage:
    __unsafe_return SomeTag
    Note:
    The instruction above overwrites @counter with the value of SomeTag_return_address.
    That is, probably return to the callee.
    """
    result = []
    verdicts = src_line.split()

    if len(verdicts) < 2:
        raise CompilationError("error: too few arguments for __unsafe_return")
    if len(verdicts) > 2:
        raise CompilationError("error: too many arguments for __unsafe_return")

    target_tag = verdicts[1]
    return_address_variable = target_tag + "_return_address"
    result.append(F"set @counter {return_address_variable}")
    return result
