import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class UnsafeCallReturnTestSuite(unittest.TestCase):
    """Test __unsafe_call and __unsafe_return instructions."""

    def test_unsafe_call_return(self):
        compiler = ExtendedCompiler()
        src_text = """
xlet i = 10
:loop
xlet delays = 60 - 5
:delay1s
xlet delays = delays - 1
jump-if delay1s delays > 0

xlet print_content = i
xlet message_board = message1
xlet i = i - 1
__unsafe_call AutoPrint
jump-if loop i >= 0
end

:AutoPrint
print print_content
printflush message_board
__unsafe_return AutoPrint
        """
        ans = """set i 10
op sub delays 60 5
op sub delays delays 1
jump 2 greaterThan delays 0
set print_content i
set message_board message1
op sub i i 1
op add AutoPrint_return_address @counter 1
jump 11 always 0 0
jump 1 greaterThanEq i 0
end
print print_content
printflush message_board
set @counter AutoPrint_return_address"""

        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())


if __name__ == '__main__':
    unittest.main()
