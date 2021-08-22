import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
mlog_extended = __import__("mlog_extended")

compiler = mlog_extended.BasicCompiler()
