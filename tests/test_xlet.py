import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class XletTestSuite(unittest.TestCase):
    """Test xlet instructions."""

    def test_xlet_assignment(self):
        compiler = ExtendedCompiler()
        src = [
            "xlet a = 42",
            "xlet a =~ 42",
            "xlet a log 42",
            "xlet a ln 42",
            "xlet a log10 42",
            "xlet a lg 42",
            "xlet a =min 42 1000",
            "xlet a =max 42 1000",
            "xlet health =sensor @unit @health",
            "xlet building =getlink 1"
        ]
        ans = [
            "set a 42",
            "op not a 42 0",
            "op log a 42 0",
            "op log a 42 0",
            "op log10 a 42 0",
            "op log10 a 42 0",
            "op min a 42 1000",
            "op max a 42 1000",
            "sensor health @unit @health",
            "getlink building 1"
        ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_xlet_binary_operators(self):
        compiler = ExtendedCompiler()
        src = [
            "xlet a = 42",
            "xlet a = a + 42",
            "xlet a = a - 42",
            "xlet a = a * 42",
            "xlet a = a / 42",
            "xlet a = a // 42"
        ]
        ans = [
            "set a 42",
            "op add a a 42",
            "op sub a a 42",
            "op mul a a 42",
            "op div a a 42",
            "op idiv a a 42"
        ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_xlet_sensor(self):
        compiler = ExtendedCompiler()
        src = [
            "xlet a sensor block1 @copper",
            "xlet b =sensor block1 @lead"
        ]
        ans = [
            "sensor a block1 @copper",
            "sensor b block1 @lead"
        ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_fail_xlet_unsupported_operator(self):
        compiler = ExtendedCompiler()
        src = [
            "xlet a = b @@@ c",
        ]
        src_text = "\n".join(src)
        with self.assertRaises(CompilationError):
            compiler.compile(src_text)


if __name__ == '__main__':
    unittest.main()
