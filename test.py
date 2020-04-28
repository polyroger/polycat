import os
from pipeline_utilities import file_manipulation

version = file_manipulation.getLatestVersion("F:/projects/aaa/tst/tst0010","boxes")
print version
print type(version)


