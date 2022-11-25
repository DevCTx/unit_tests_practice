import unittest

# By default, pytest read recursively all :
# python_files     = *_test.py
# python_classes   = *_Tests
# python_functions = test test_*

# But if a pytest.ini is overwritten, it is possible to change some parameters :
# [pytest]
# python_files=tst_*.py             # Change the file names to read tst_*
# python_classes=*_tests            # *_tests or *_Tests are read
# python_functions=test test_*
class repeating_checks():
    def test_01(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def Test_02(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def tests_03(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def Tests_04(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def check_05(self): assert [1, 2] == [1, 2]     # tst_* file / *_Tests class / check_* method : not read
    def check_06_test(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def check_07_Test(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def check_08_tests(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read
    def check_09_Tests(self): assert (1 + 1 == 2)          # tst_* file / *_Tests class / test_* method : read

class check_01_Tests(repeating_checks): pass
# 01 : tst_* file / *_Tests class / test_* method : read
# 02 : tst_* file / *_Tests class / Test_* method : read
# 03 : tst_* file / *_Tests class / tests_* method : read
class check_02_tests(repeating_checks): pass
# 01 : tst_* file / *_tests class / test_* method : read
# 02 : tst_* file / *_tests class / Test_* method : read
# 03 : tst_* file / *_tests class / tests_* method : read
class check_03_Test(repeating_checks): pass     # not read
class check_04_test(repeating_checks): pass     # not read
class check_05_TST(repeating_checks): pass      # not read
class Tests_check_06(repeating_checks): pass    # not read
class tests_check_07(repeating_checks): pass    # not read
class Test_check_08(repeating_checks): pass     # not read
class test_check_09(repeating_checks): pass     # not read
# Conclusion : the method must starts with the prefix 'test_*' 'Test_*' or 'tests_*'
# and the class name must have the suffix '_Tests' or '_tests' to be read

# except if the class inherits of unittest.TestCase, where the class name is not relevant
class check_10_Tests(unittest.TestCase,repeating_checks): pass
class check_11_tests(unittest.TestCase,repeating_checks): pass
class check_12_Test(unittest.TestCase,repeating_checks): pass
class check_13_test(unittest.TestCase,repeating_checks): pass
class check_14_TST(unittest.TestCase,repeating_checks): pass
class Tests_check_15(unittest.TestCase,repeating_checks): pass
class tests_check_16(unittest.TestCase,repeating_checks): pass
class Test_check_17(unittest.TestCase,repeating_checks): pass
class test_check_18(unittest.TestCase,repeating_checks): pass
# Conclusion : All methods starting with the prefix 'test_*' or 'tests_*' can be read

# By default, FILES matching 'test_*.py' and '*_test.py' will be considered test modules
# By default, pytest will consider any FUNCTION prefixed with 'test' (lowercase) as a test

# A directory can be set by pythonpath = src1 src2  or by using the -k <dir> option with pytest
# There is no recurse in folder '*.egg', '.*', '_darcs', 'build', 'CVS', 'dist', 'node_modules', 'venv', '{arch}'
# and more can be added by norecursedirs = .svn _build tmp*

# PRO : The recommendation is to only use these configuration options for legacy projects that follow a different
# convention, and stick with the defaults for new projects. Using the defaults is less work and avoids confusing
# for other collaborators.

# Src : https://buildmedia.readthedocs.org/media/pdf/pytest/latest/pytest.pdf
