import unittest

from pytest import mark
from parameterized import parameterized

# For detailed displays : pytest -v
# To test only this file :  pytest -v -k test_marks.py

# To test only some markers :  pytest -v -k test_marks.py -m 'marker_name'
# Or the inverse test all except the markers :   pytest -v -k test_marks.py -m 'not marker_name'

# To avoid warnings on custom marks 'marker_name', list of markers can be added into pytest.ini
# [pytest]
# markers=
#         marker_name :  marker test written into pytest.ini for a better understanding
#         marker_name1 : marker test written into pytest.ini for a better understanding

# or defined into the conftest.py file      # both are compatible
# import pytest
# def pytest_configure(config):
#     config.addinivalue_line(
#         "markers", "marker_name : marker tests written for a better understanding"
#     )
#     config.addinivalue_line(
#         "markers", "marker_name1 : marker tests written for a better understanding"
#     )

# To see the registered common and custom markers : pytest --markers

# Possibility to add a 'skip' marker (no need to declare it into pytest.ini ou conftest.py)
# 'skip' allows to add a reason which will be printed on test results
# 'skipif(True)' adds conditions like running on a specific system or version or depending on a previous test result

# markers accept NOT or OR or AND operator and can be mixed during the calls
# pytest -v -k test_marks.py -m 'marker_name1 or marker_name2'
# pytest -v -k test_marks.py -m 'marker_name1 and marker_name2'


class repeating_checks():
    @mark.marker_name1
    def test_method_01(self): assert (1 + 1 == 2)
    @mark.marker_name
    def test_method_02(self): assert (1 + 1 == 2)      # 'mark_test' marked function
    @mark.skip('This is a skip reason : no need to test this method')
    def test_method_03(self): assert (1 + 1 == 2)      # 'skip' marked function

    # parametrize is not supported by unittest.TestCase
    @mark.marker_name3
    @mark.parametrize("val",[1,2])                    # 'parametrize' may test different values
    def test_method_04(self, val):
        assert val > 0

    # and should be modified by using parameterized (following this structure)
    @parameterized.expand([
        (1, 1),
        (2, 2),
    ])
    @mark.marker_name3                                    # Careful, the parameterized must not be under marker
    def test_method_05(self,val1, val2):
        print(f"Test {val1} > 0 (no use of {val2})", end=' ')
        assert val1 > 0  # 'parametrize' to test different values


# Without unittest.TestCase heritage
@mark.marker_name1
class check_01_Tests(repeating_checks): pass
@mark.marker_name
class check_02_Tests(repeating_checks): pass    # 'mark_test' marked class
@mark.skip('This is a skip reason : no need to test this class')
class check_03_Tests(repeating_checks): pass    # 'skip' marked class

# With unittest.TestCase heritage
@mark.marker_name2
class check_04_TestCase_Tests(unittest.TestCase,repeating_checks): pass
@mark.marker_name
class check_05_TestCase_Tests(unittest.TestCase,repeating_checks): pass    # 'mark_test' marked class
@mark.skip('This is a skip reason : no need to test this class')
class check_06_TestCase_Tests(unittest.TestCase,repeating_checks): pass    # 'skip' marked class

# # # With unittest.TestCase heritage
# @mark.marker_name2
# class check_04_TestCase_Tests(repeating_checks): pass
# @mark.marker_name
# class check_05_TestCase_Tests(repeating_checks): pass    # 'mark_test' marked class
# @mark.skip('This is a skip reason : no need to test this class')
# class check_06_TestCase_Tests(repeating_checks): pass    # 'skip' marked class

''' pytest considers all tests if pytest.ini file is defined 
>>> pytest -v -k test_marks.py
test_marks.py::check_01_Tests::test_method_01 PASSED         
test_marks.py::check_01_Tests::test_method_02 PASSED         
test_marks.py::check_02_Tests::test_method_01 PASSED         
test_marks.py::check_02_Tests::test_method_02 PASSED         
test_marks.py::check_03_Tests::test_method_01 PASSED         
test_marks.py::check_03_Tests::test_method_02 PASSED         
test_marks.py::check_04_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_02 PASSED
'''
''' but only considers unittest.TestCase classes if no pytest.ini file
>>> pytest -v -k test_marks.py
test_marks.py::check_04_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_02 PASSED
'''

''' To test specific 'marker_name' tests WITH pytest.ini file
>>> pytest -v -k test_marks.py -m 'marker_name'
test_marks.py::check_01_Tests::test_method_02 PASSED         
test_marks.py::check_02_Tests::test_method_01 PASSED         
test_marks.py::check_02_Tests::test_method_02 PASSED         
test_marks.py::check_03_Tests::test_method_02 PASSED         
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_02 PASSED
'''
''' WITHOUT pytest.ini file
>>> pytest -v -k test_marks.py -m 'marker_name'
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_02 PASSED
'''

''' To AVOID specific 'marker_name' tests WITH pytest.ini file
>>> pytest -v -k test_marks.py -m 'not marker_name'
test_marks.py::check_01_Tests::test_method_01 PASSED         
test_marks.py::check_03_Tests::test_method_01 PASSED         
test_marks.py::check_04_TestCase_Tesgits::test_method_01 PASSED
test_marks.py::check_06_TestCase_Tests::test_method_01 PASSED
'''
''' WITHOUT pytest.ini file
>>> pytest -v -k test_marks.py -m 'not marker_name'
test_marks.py::check_04_TestCase_Tests::test_method_01 PASSED 
test_marks.py::check_06_TestCase_Tests::test_method_01 PASSED
'''

''' ADDING 'skip' marks on functions and classes, WITH pytest.ini
>>> pytest -v -k test_marks.py -m 'marker_name'
test_marks.py::check_01_Tests::test_method_02 PASSED                                                                
test_marks.py::check_02_Tests::test_method_01 PASSED                                                                
test_marks.py::check_02_Tests::test_method_02 PASSED                                                                
test_marks.py::check_02_Tests::test_method_03 SKIPPED (This is a skip reason : no need to test this method)         
test_marks.py::check_03_Tests::test_method_02 SKIPPED (This is a skip reason : no need to test this class)          
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_03 SKIPPED (This is a skip reason : no need to test this method)
test_marks.py::check_06_TestCase_Tests::test_method_02 SKIPPED (This is a skip reason : no need to test this class)   
'''
''' WITHOUT pytest.ini
>>> pytest -v -k test_marks.py -m 'marker_name'
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_02 PASSED                                                       
test_marks.py::check_05_TestCase_Tests::test_method_03 SKIPPED (This is a skip reason : no need to test this method)
test_marks.py::check_06_TestCase_Tests::test_method_02 SKIPPED (This is a skip reason : no need to test this class)
'''

''' Operator can be mixed into the marker option, WITH pytest.ini
This considers and details all the functions of the classes marked by 'marker_name1' [check_01_Tests]
AVOIDING all the functions of the classes marked by 'marker_name2' [check_04_TestCase_Tests] 
IDENTIFY all the functions of other classes with 'marker_name1' and not 'marker_name2'  (All test_method_01)
AND considers or skip them depending of the 'skip' marker over the class
>>> pytest -v -k test_marks.py -m 'marker_name1 and not marker_name2'
test_marks.py::check_01_Tests::test_method_01 PASSED                                                               
test_marks.py::check_01_Tests::test_method_02 PASSED                                                               
test_marks.py::check_01_Tests::test_method_03 SKIPPED (This is a skip reason : no need to test this method)        
test_marks.py::check_02_Tests::test_method_01 PASSED                                                               
test_marks.py::check_03_Tests::test_method_01 SKIPPED (This is a skip reason : no need to test this class)         
test_marks.py::check_05_TestCase_Tests::test_method_01 PASSED                                                      
test_marks.py::check_06_TestCase_Tests::test_method_01 SKIPPED (This is a skip reason : no need to test this class)  
'''

# marks can also be parametrized to test different values but
#
#     # parametrize is not supported by unittest.TestCase
#     @mark.marker_name3
#     @mark.parametrize("val", [1, 2])                      # 'parametrize' may test different values
#     def test_method_04(self, val):
#     assert val > 0
#
#     # and should be modified by using parameterized (following this structure)
#     @parameterized.expand([
#         (1, 1),
#         (2, 2),
#     ])
#     @mark.marker_name3                                    # Careful, the parameterized must not be under marker
#     def test_method_05(self,val1, val2):
#         print(f"Test {val1} > 0 (no use of {val2})", end=' ')
#         assert val1 > 0  # 'parametrize' to test different values
#
# This required to import and install 'parameterized'
#
'''
>>> pytest -v -k test_marks.py -m 'marker_name and marker_name3' -s
test_marks.py::check_02_Tests::test_method_04[1] PASSED
test_marks.py::check_02_Tests::test_method_04[2] PASSED
test_marks.py::check_02_Tests::test_method_05_0 Test 1 > 0 (no use of 1) PASSED
test_marks.py::check_02_Tests::test_method_05_1 Test 2 > 0 (no use of 2) PASSED
test_marks.py::check_05_TestCase_Tests::test_method_04 FAILED                      # Not support by unittest.TestCase
test_marks.py::check_05_TestCase_Tests::test_method_05_0 Test 1 > 0 (no use of 1) PASSED
test_marks.py::check_05_TestCase_Tests::test_method_05_1 Test 2 > 0 (no use of 2) PASSED
'''
