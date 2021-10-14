"""Maintain jump tags for if-elif-else branches and while loops."""

class WhileLoopFlags:
    """Maintain while loop flags."""
    def __init__(self, identifier: str):
        self.tag_prefix = F"__mlogex_while_loop_{identifier}"
        self.while_looper = []

    def get_condition_tag(self):
        return F"{self.tag_prefix}_loop_cond"

    def get_loopbody_start_tag(self):
        return F"{self.tag_prefix}_loop_start"

    def get_loopbody_end_tag(self):
        return F"{self.tag_prefix}_loop_end"


class IfElseFlags:
    """Main if-elif-else branches and flags."""
    def __init__(self, identifier: str):
        self.tag_prefix = F"__mlogex_branches_{identifier}"
        self.branch_id = 0

    def get_current_branch_tag(self):
        return F"{self.tag_prefix}_{self.branch_id}"

    def get_next_branch_tag(self):
        return F"{self.tag_prefix}_{self.branch_id+1}"

    def get_endif_tag(self):
        return F"{self.tag_prefix}_endif"

    def increase_branch_id(self):
        self.branch_id += 1
