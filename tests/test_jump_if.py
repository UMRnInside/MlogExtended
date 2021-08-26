import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class JumpIfTestSuite(unittest.TestCase):
    """Test jump-if instructions."""

    def test_jump_if_always(self):
        compiler = ExtendedCompiler()
        src = [
            ":tag1",
            "jump-if tag1 always"
        ]
        ans = ["jump 0 always 0 0", ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_jump_if_strict_equal(self):
        compiler = ExtendedCompiler()
        src = [
            ":tag1",
            "jump-if tag1 x === null"
        ]
        ans = ["jump 0 strictEqual x null", ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_fail_unsupported_condition(self):
        compiler = ExtendedCompiler()
        src = [
            ":tag1",
            "jump-if tag1 x ??? y",
        ]
        src_text = "\n".join(src)
        with self.assertRaises(CompilationError):
            compiler.compile(src_text)


if __name__ == '__main__':
    unittest.main()
