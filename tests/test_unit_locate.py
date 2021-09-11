import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler

class UnitLocateTestSuite(unittest.TestCase):
    """Test unit-radar instructions."""

    def test_unit_locate(self):
        compiler = ExtendedCompiler()
        src_text = """
unit-locate type=ore oreType=@coal resultX=x resultY=y resultIsFound=found
unit-locate type=building group=core isEnemy=false outX=x outY=y found=found building=core
unit-locate find=building group=core enemy=false outX=x outY=y found=found building=core
unit-locate type=spawn resultX=x resultY=y resultIsFound=found building=building
unit-locate type=damaged outX=x outY=y resultIsFound=found resultBuilding=building
"""
        ans = """ulocate ore core false @coal x y found 0
ulocate building core false 0 x y found core
ulocate building core false 0 x y found core
ulocate spawn core false 0 x y found building
ulocate damaged core false 0 x y found building
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
