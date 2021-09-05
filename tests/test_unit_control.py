import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class UnitControlTestSuite(unittest.TestCase):
    """Test unit-control instructions."""

    def test_unit_control_commands(self):
        compiler = ExtendedCompiler()
        src_text = """
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
unit-control getBlock x=1 y=2 type=type building=resultBuilding
unit-control within x=1 y=2 radius=3 result=isWithinRadius
"""
        ans = """ucontrol idle 0 0 0 0 0
ucontrol stop 0 0 0 0 0
ucontrol move 128 192 0 0 0
ucontrol approach 128 192 9 0 0
ucontrol boost 1 0 0 0 0
ucontrol pathfind 0 0 0 0 0
ucontrol target targetX targetY shooting 0 0
ucontrol targetp enemy shooting 0 0 0
ucontrol itemDrop core 1 0 0 0
ucontrol itemTake core @copper 1 0 0
ucontrol payDrop 0 0 0 0 0
ucontrol payTake myUnit 0 0 0 0
ucontrol mine 128 192 0 0 0
ucontrol flag 10000 0 0 0 0
ucontrol getBlock 1 2 type resultBuilding 0
ucontrol within 1 2 3 isWithinRadius 0
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

    def test_unit_control_aliases(self):
        compiler = ExtendedCompiler()
        src_text = """
unit-control boost boost=1
unit-control targetp target=enemy shoot=shooting
unit-control flag flag=10000
unit-control getBlock x=1 y=2 resultType=type resultBuilding=building
"""
        ans = """ucontrol boost 1 0 0 0 0
ucontrol targetp enemy shooting 0 0 0
ucontrol flag 10000 0 0 0 0
ucontrol getBlock 1 2 type building 0
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
