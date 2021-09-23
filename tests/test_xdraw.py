import unittest
from .context import mlog_extended

ExtendedCompiler = mlog_extended.ExtendedCompiler
CompilationError = mlog_extended.CompilationError

class XdrawTestSuite(unittest.TestCase):
    """Test xcontrol instructions."""

    def test_xdraw_actions(self):
        compiler = ExtendedCompiler()
        src_text = """
    # Clear display, using material gray color #373737
    xdraw clear r=55 g=55 b=55
    xdraw clear rgb=0x373737
    # Set stroke width
    xdraw stroke width=1
    # Set color to #FF9100
    xdraw color rgb=0xFF9100
    # Draw a line
    xdraw line x=3 y=1 x2=3 y2=80
    xdraw line x1=3 y1=1 x2=3 y2=80
    # Draw a rectangle
    xdraw rect x1=5 y1=5 height=5 width=10
    # Draw a line rectangle
    xdraw lineRect x1=15 y1=5 height=5 width=10
    # Draw a pentagon
    xdraw poly x=20 y=40 sides=5 radius=10 rotation=0
    # Draw a triangle
    xdraw triangle x1=30 y1=30 x2=20 y2=30 x3=20 y3=20
    # Draw a cyclone
    xdraw color rgb=FFFFFF
    xdraw image x=60 y=60 image=@cyclone size=40 rotation=0
    # Flush
    drawflush display1
"""
        ans = """draw clear 55 55 55 0 0 0
draw clear 55 55 55 0 0 0
draw stroke 1 0 0 0 0 0
draw color 255 145 0 0 0 0
draw line 3 1 3 80 0 0
draw line 3 1 3 80 0 0
draw rect 5 5 10 5 0 0
draw lineRect 15 5 10 5 0 0
draw poly 20 40 5 10 0 0
draw triangle 30 30 20 30 20 20
draw color 255 255 255 0 0 0
draw image 60 60 @cyclone 40 0 0
drawflush display1"""
        self.assertEqual(ans.splitlines(),
                compiler.compile(src_text).splitlines())

if __name__ == '__main__':
    unittest.main()
