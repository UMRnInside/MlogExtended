"""Procedural compiler module.
Provide ProceduralCompiler."""
from .compilation_error import CompilationError
from .extended_compiler import ExtendedCompiler
from .procedural_structures import WhileLoopFlags, IfElseFlags

INVERT_TABLE = {
    "!=": "==",
    "==": "!=",
    "<": ">=",
    "<=": ">",
    ">": "<=",
    ">=": "<",
}

class ProceduralCompiler:
    """Procedural compiler, provides procedural-programming-like experience.
if, elif and while can receive 2 arguments at most.
e.g.:
    if a && b
    elif b < 0
    elif a
    else
    while i > 0
Keywords:
    if: starts the first branch
    elif: involved if there is more than 1 branch.
    else: indicates the last branch
    endif: terminates an if-else branch, necessary.

    while: starts a while loop.
    endwhile: ends a while loop.
    wend: same as "endwhile"

    do: starts a do-while loop.
    dowhile: ends a do-while loop.

    break: break while or do-while loop.
    continue: skip to next loop.
    """

    if_keywords = ("if", "elif", "else", "endif")
    while_keywords = ("while", "wend", "endwhile", "do", "dowhile", "break", "continue")

    def __init__(self):
        self.backend = ExtendedCompiler()
        self.loop_stack = []
        self.if_stack = []

    def compile_to_backend(self, src_mappings:list, sep='\n') -> str:
        dst_mappings = []
        for (line_number, src_line) in src_mappings:
            verdicts = src_line.split()
            if len(verdicts) == 0:
                continue
            if verdicts[0] in self.if_keywords:
                try:
                    result = self.handle_if(verdicts, str(line_number))
                    dst_mappings.extend([(line_number, code) for code in result])
                except IndexError as exception:
                    message = F"line {line_number+1}: error: "
                    message += F"{verdicts[0]} without if."
                    raise CompilationError(message) from exception
            elif verdicts[0] in self.while_keywords:
                try:
                    result = self.handle_while(verdicts, str(line_number))
                    dst_mappings.extend([(line_number, code) for code in result])
                except IndexError as exception:
                    message = F"line {line_number+1}: error: "
                    message += F"{verdicts[0]} outside of loop."
                    raise CompilationError(message) from exception
            else:
                dst_mappings.append((line_number, " ".join(verdicts)))
        return dst_mappings

    def handle_if(self, verdicts:list, identifier: str) -> list:
        result = []
        condition = "__mlogex_ifelse_condition"
        if verdicts[0] == "if":
            self.if_stack.append(IfElseFlags(identifier))
            top_tagger = self.if_stack[-1]
            next_tag = top_tagger.get_next_branch_tag()
            top_tagger.increase_branch_id()
            jump_instructions = get_inverted_jump(condition, next_tag, verdicts)
            result.extend(jump_instructions)
            return result
        top_tagger = self.if_stack[-1]
        if verdicts[0] in ("elif", "else"):
            current_tag = top_tagger.get_current_branch_tag()
            next_tag = top_tagger.get_next_branch_tag()
            final_tag = top_tagger.get_endif_tag()
            top_tagger.increase_branch_id()
            result.append(F"jump-if {final_tag} always")
            result.append(F":{current_tag}")
            if verdicts[0] == "elif":
                jump_instructions = get_inverted_jump(condition, next_tag, verdicts)
                result.extend(jump_instructions)
            return result
        if verdicts[0] == "endif":
            current_tag = top_tagger.get_current_branch_tag()
            final_tag = top_tagger.get_endif_tag()
            result.append(F":{current_tag}")
            result.append(F":{final_tag}")
            self.if_stack.pop()
            return result
        return []

    def handle_while(self, verdicts:list, identifier: str) -> list:
        result = []
        condition = "__mlogex_while_condition"
        if verdicts[0] in ("while", "do"):
            self.loop_stack.append(WhileLoopFlags(identifier))
            top_tagger = self.loop_stack[-1]
            start_tag = top_tagger.get_loopbody_start_tag()
            cond_tag = top_tagger.get_condition_tag()
            if verdicts[0] == "while":
                top_tagger.while_looper.append(F":{cond_tag}")
                jumps = get_fastest_while_jump(condition, start_tag, verdicts)
                top_tagger.while_looper.extend(jumps)
                result.append(F"jump-if {cond_tag} always")
            result.append(F":{start_tag}")
            return result
        top_tagger = self.loop_stack[-1]
        start_tag = top_tagger.get_loopbody_start_tag()
        cond_tag = top_tagger.get_condition_tag()
        end_tag = top_tagger.get_loopbody_end_tag()
        if verdicts[0] in ("wend", "endwhile"):
            result.extend(top_tagger.while_looper)
            # result.append(F"# {repr(top_tagger.while_looper)}")
            # result.append(F"# {repr(verdicts)}")
            result.append(F":{end_tag}")
            self.loop_stack.pop()
        elif verdicts[0] == "dowhile":
            jumps = get_fastest_while_jump(condition, start_tag, verdicts)
            result.append(F":{cond_tag}")
            result.extend(jumps)
            result.append(F":{end_tag}")
            self.loop_stack.pop()
        elif verdicts[0] == "break":
            result.append(F"jump-if {end_tag} always")
        elif verdicts[0] == "continue":
            result.append(F"jump-if {cond_tag} always")
        return result

    def compile(self, src_text:str, sep='\n') -> str:
        src_mappings = list(enumerate(src_text.splitlines()))
        extended_mappings = self.compile_to_backend(src_mappings, sep)
        return self.backend.compile_with_mappings(extended_mappings, sep)

def create_temporary_xlet(variable: str, arguments: list) -> str:
    return F"xlet {variable} = " + (" ".join(arguments))

def try_invert_xlet(xlet_instruction: str, target_tag: str) -> str:
    """Optimize performance for if-elif and while-wend control flows.
    If operator is invertable (e.g.: <, >, <=, >=, ==, !=), return inverted expression.
    If it is not invertable, return empty string.
    Example:
    "xlet condition = a < b", "tag" -> "jump-if tag a >= b"
    "xlet condition = a && b", "tag" -> ""
    """
    verdicts = xlet_instruction.split()
    if len(verdicts) == 4:
        real_condition = verdicts[3]
        return F"jump-if {target_tag} {real_condition} == false"
    operator = verdicts[4]
    if operator in INVERT_TABLE.keys():
        inverted = INVERT_TABLE[operator]
        return F"jump-if {target_tag} {verdicts[3]} {inverted} {verdicts[5]}"
    return ""

def get_inverted_jump(condition:str, jump_tag:str, verdicts: list) -> list:
    result = []
    temp_xlet = create_temporary_xlet(condition, verdicts[1:])
    inverted = try_invert_xlet(temp_xlet, jump_tag)
    if inverted:
        result.append(inverted)
    else:
        result.append(temp_xlet)
        result.append(F"jump-if {jump_tag} {condition} == false")
    return result

def get_fastest_while_jump(condition:str, jump_tag:str, verdicts: list) -> list:
    """Verdicts like ["while", "a", "<", "10"] """
    result = []
    jumpables = ("===", ) + tuple(INVERT_TABLE.keys())
    if len(verdicts) == 2:
        result.append(F"jump-if {jump_tag} {verdicts[1]} != false")
    elif verdicts[2] in jumpables:
        result.append(F"jump-if {jump_tag} " + (" ".join(verdicts[1:]) ) )
    else:
        result.append(create_temporary_xlet(condition, verdicts[1:]))
        result.append(F"jump-if {jump_tag} {condition} != false")
    return result
