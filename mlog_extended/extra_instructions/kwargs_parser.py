"""Python-style kwargs parser module. Used by ucontrol, uradar, ulocate, etc."""

def parse_kwargs(input_verdicts: list) -> dict:
    kwargs = {}
    for kv_string in input_verdicts:
        key, value = kv_string.split("=", 1)
        kwargs[key] = value
    return kwargs
