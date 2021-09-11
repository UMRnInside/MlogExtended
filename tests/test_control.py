import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class ControlTestSuite(unittest.TestCase):
    """Test xcontrol instructions."""

    def test_control_actions(self):
        compiler = ExtendedCompiler()
        src_text = """
xcontrol generator1 action=toggle status=0
xcontrol generator1 action=enabled status=0
xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=1
xcontrol cyclone1 action=shoot x=enemyX y=enemyY shoot=0
xcontrol cyclone1 action=shootp unit=enemy shoot=1
xcontrol cyclone1 action=shootp target=enemy shoot=1
xcontrol sorter1 action=configure config=@copper
xcontrol sorter1 action=config config=@lead
xcontrol illuminator1 action=color r=255 g=153 b=0
"""
        ans = """control enabled generator1 0 0 0 0
control enabled generator1 0 0 0 0
control shoot cyclone1 enemyX enemyY 1 0
control shoot cyclone1 enemyX enemyY 0 0
control shootp cyclone1 enemy 1 0 0
control shootp cyclone1 enemy 1 0 0
control configure sorter1 @copper 0 0 0
control configure sorter1 @lead 0 0 0
control color illuminator1 255 153 0 0
"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
