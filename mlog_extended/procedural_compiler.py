"""Procedural compiler module.
Provide ProceduralCompiler."""
from .compilation_error import CompilationError
from .extended_compiler import ExtendedCompiler
from .procedural_structures import WhileLoopFlags, IfElseFlags

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
    """

    if_keywords = ("if", "elif", "else", "endif")
    while_keywords = ("while", "wend", "endwhile", "break", "continue")

    def __init__(self):
        self.backend = ExtendedCompiler()
        self.loop_stack = []
        self.if_stack = []

    def compile_to_backend(self, src_text:str, sep='\n') -> str:
        dst_lines = []
        for (line_number, src_line) in enumerate(src_text.splitlines()):
            verdicts = src_line.split()
            if len(verdicts) == 0:
                continue
            if verdicts[0] in self.if_keywords:
                try:
                    dst_lines.extend(self.handle_if(verdicts, str(line_number)))
                except IndexError as exception:
                    message = F"line {line_number+1}: error: "
                    message += F"{verdicts[0]} without if."
                    raise CompilationError(message) from exception
            elif verdicts[0] in self.while_keywords:
                try:
                    dst_lines.extend(self.handle_while(verdicts, str(line_number)))
                except IndexError as exception:
                    message = F"line {line_number+1}: error: "
                    message += F"{verdicts[0]} outside of loop."
                    raise CompilationError(message) from exception
            else:
                dst_lines.append(" ".join(verdicts))
        return sep.join(dst_lines)

    def handle_if(self, verdicts:list, identifier: str) -> list:
        result = []
        condition = "__mlogex_ifelse_condition"
        if verdicts[0] == "if":
            self.if_stack.append(IfElseFlags(identifier))
            top_tagger = self.if_stack[-1]
            next_tag = top_tagger.get_next_branch_tag()
            top_tagger.increase_branch_id()
            result.append(create_temporary_xlet(condition, verdicts[1:]))
            result.append(F"jump-if {next_tag} {condition} == false")
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
                result.append(create_temporary_xlet(condition, verdicts[1:]))
                result.append(F"jump-if {next_tag} {condition} == false")
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
        if verdicts[0] == "while":
            self.loop_stack.append(WhileLoopFlags(identifier))
            top_tagger = self.loop_stack[-1]
            start_tag = top_tagger.get_loopbody_start_tag()
            cond_tag = top_tagger.get_condition_tag()

            top_tagger.while_looper.append(F":{cond_tag}")
            top_tagger.while_looper.append(create_temporary_xlet(condition, verdicts[1:]))
            top_tagger.while_looper.append(F"jump-if {start_tag} {condition} != false")
            result.append(F"jump-if {cond_tag} always")
            result.append(F":{start_tag}")
            return result
        top_tagger = self.loop_stack[-1]
        cond_tag = top_tagger.get_condition_tag()
        end_tag = top_tagger.get_loopbody_end_tag()
        if verdicts[0] in ("wend", "endwhile"):
            result.extend(top_tagger.while_looper)
            # result.append(F"# {repr(top_tagger.while_looper)}")
            # result.append(F"# {repr(verdicts)}")
            result.append(F":{end_tag}")
            self.loop_stack.pop()
        elif verdicts[0] == "break":
            result.append(F"jump-if {end_tag} always")
        elif verdicts[0] == "continue":
            result.append(F"jump-if {cond_tag} always")
        return result

    def compile(self, src_text:str, sep='\n') -> str:
        extended_source_code = self.compile_to_backend(src_text, sep)
        return self.backend.compile(extended_source_code, sep)

def create_temporary_xlet(variable: str, arguments: list) -> str:
    return F"xlet {variable} = " + (" ".join(arguments))
