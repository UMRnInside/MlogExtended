import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class UnitControlTestSuite(unittest.TestCase):
    """Test xlet instructions."""

    def test_unit_control_commands(self):
        compiler = ExtendedCompiler()
        src_test = """
unit-control idle
unit-control stop
unit-control move x=128 y=192
unit-control approach x=128 y=192 radius=9
unit-control boost enable=1
unit-control pathfind
unit-control target x=targetX y=targetY shoot=shooting
unit-control targetp unit=enemy shoot=shooting
unit-control itemDrop to=core amount=1
unit-control itemTake from=core amount=1 item=@copper
unit-control payDrop
unit-control payTake takeUnits=myUnit
unit-control mine x=128 y=192
unit-control flag value=10000
unit-control getBlock x=1 y=2 type=0 building=resultBuilding
unit-control within x=1 y=2 radius=3 result=isWithinRadius
"""
        ans = [
            "set a 42",
            "op not a 42 0",
            "op log a 42 0",
            "op log a 42 0",
            "op log10 a 42 0",
            "op log10 a 42 0",
            "op min a 42 1000",
            "op max a 42 1000",
        ]
        self.assertEqual(ans,
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
