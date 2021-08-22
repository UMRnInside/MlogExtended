from .context import MlogExtended
import unittest

BasicCompiler = MlogExtended.BasicCompiler
CompilationError = MlogExtended.CompilationError

class XjumpTagTestSuite(unittest.TestCase):
    """Test xjump instructions."""

    def test_single_tag(self):
        compiler = BasicCompiler()
        src = [
            ":tag1",
            "xjump tag1 always 0 0"
        ]
        ans = ["jump 0 always 0 0", ]
        src_text = "\n".join(src)
        self.assertEqual(ans, 
                compiler.compile(src_text).splitlines())

    def test_multiple_tags(self):
        compiler = BasicCompiler()
        src = [
            ":tag1",
            ":tag2",
            "xjump tag1 always 0 0",
            ":tag3",
            "xjump tag2 strictEqual @unit null",
            "xjump tag3 notEqual 1 2"
        ]
        ans = ["jump 0 always 0 0",
            "jump 0 strictEqual @unit null",
            "jump 1 notEqual 1 2"
        ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_jumping_to_end(self):
        compiler = BasicCompiler()
        src = [
            ":tag1",
            "xjump tag2 always 0 0",
            ":tag2",
        ]
        ans = [
            "jump 1 always 0 0",
            "end"
        ]
        src_text = "\n".join(src)
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

    def test_nonexist_tag(self):
        compiler = BasicCompiler()
        src = [
            ":tag1",
            "xjump tag_that_does_not_exist always 0 0",
        ]
        src_text = "\n".join(src)
        with self.assertRaises(CompilationError):
            compiler.compile(src_text)


if __name__ == '__main__':
    unittest.main()
