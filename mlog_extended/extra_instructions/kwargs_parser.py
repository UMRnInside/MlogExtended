"""Python-style kwargs parser module. Used by ucontrol, uradar, ulocate, etc."""

def pad_args(src: list, total_verdicts: int) -> list:
    """Pad extra args with 0."""
    padding_count = max(total_verdicts - len(src), 0)
    result = []
    result.extend(src)
    result.extend(["0",]*padding_count)
    return result

def parse_kwargs(input_verdicts: list) -> dict:
    kwargs = {}
    for kv_string in input_verdicts:
        key, value = kv_string.split("=", 1)
        kwargs[key] = value
    return kwargs

def apply_aliases(kwdict: dict, aliases: dict) -> dict:
    for alias, real in aliases.items():
        if alias in kwdict.keys():
            kwdict[real] = kwdict[alias]
    return kwdict
