import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class UnitRadarTestSuite(unittest.TestCase):
    """Test unit-radar instructions."""

    def test_unit_radar_commands(self):
        compiler = ExtendedCompiler()
        src_text = """
unit-radar filter1=enemy filter2=attacker filter3=flying order=distance sort=1 output=attacker
"""
        ans = """uradar enemy attacker flying distance 1 attacker
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

    def test_unit_radar_aliases(self):
        compiler = ExtendedCompiler()
        src_text = """
unit-radar target=enemy orderBy=distance asc=1 output=enemy
"""
        ans = """uradar enemy any any distance 1 enemy
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
