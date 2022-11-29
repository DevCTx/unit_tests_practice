import time
import unittest
import webbrowser

import pytest
from pytest import fixture, mark

'''
This can be used when resources need to be set up before the test cases and clean once done, like 
- Connect to a DB before
- Launch a URL
- Open a file to read/write 
'''

# The function identified by fixture can be added in arg of specific methods/functions
# and will be called before and after these specific method/function
# yield means that the code following will be run on the second call
# the option -s must be used with pytest to have the details of strings
#
# @fixture()
# def I_handle_DB_URL_FILE():
#     print(" --> connect to DB/URL/FILE", end=' ')
#     yield
#     print(" --> disconnect from DB/URL/FILE", end=' ')
#
# def test_function_01(I_handle_DB_URL_FILE):
#     print(" --> test_function_01", end=' ')
#     assert True
#
# def test_function_02(I_handle_DB_URL_FILE):
#     print(" --> test_function_02", end=' ')
#     assert True
#
# def test_function_03():
#     print(" --> test_function_03", end=' ')
#     assert True
#
#
''' pytest -v -k test_fictures.py -s
test_fictures.py::test_function_01  --> connect to DB/URL/FILE  --> test_function_01 PASSED --> disconnect from DB/URL/FILE
test_fictures.py::test_function_02  --> connect to DB/URL/FILE  --> test_function_02 PASSED --> disconnect from DB/URL/FILE
test_fictures.py::test_function_03  --> test_function_03 PASSED
'''


# # But usually DB must be opened once, be used by different tests and be closed, and may need a scope to be defined
# # The fixtures are created when first requested by a test, and are destroyed based on their scope:
# #     function: the default scope, the fixture is destroyed at the end of the test.
# #     class: the fixture is destroyed during teardown of the last test in the class.
# #     module: the fixture is destroyed during teardown of the last test in the module.
# #     package: the fixture is destroyed during teardown of the last test in the package.
# #     session: the fixture is destroyed at the end of the test session.
# # Src : https://docs.pytest.org/en/6.2.x/fixture.html#fixture-scopes
#
# @fixture(scope="module")
# def I_handle_DB_URL_FILE_V2():
#     print(" --> connect to DB/URL/FILE V2", end=' ')
#     yield
#     print(" --> disconnect from DB/URL/FILE V2", end=' ')
#
# def test_function_04(I_handle_DB_URL_FILE_V2):
#     print(" --> test_function_04", end=' ')
#     assert True
#
# def test_function_05(I_handle_DB_URL_FILE_V2):
#     print(" --> test_function_05", end=' ')
#     assert True
#
# def test_function_06():
#     print(" --> test_function_06", end=' ')
#     assert True
#
'''
test_fictures.py::test_function_04  --> connect to DB/URL/FILE V2  --> test_function_04 PASSED
test_fictures.py::test_function_05  --> test_function_05 PASSED
test_fictures.py::test_function_06  --> test_function_06 PASSED --> disconnect from DB/URL/FILE V2
'''


# This can also be integrated into classes
# Note : fixture functions, and method using fixture functions do not need 'self' EXCEPT if pytest.ini is used
#
# Althought this format can be accepted in a class not inherited from unittest.TestCase if a pytest.ini file is defined
#     def test_method_01(self,I_handle_DB_URL_FILE_in_class):
#
# It will be better to use this format for being accepted by all cases (with or without pytest.ini)
#     #@mark.usefixtures('I_handle_DB_URL_FILE_in_class')
#     def test_method_01(self):
#
# class repeating_calls():
#
#     @fixture(scope='class')
#     def I_handle_DB_URL_FILE_in_class(self):
#         print(" --> connect to DB/URL/FILE in class", end=' ')
#         yield
#         print(" --> disconnect from DB/URL/FILE in class", end=' ')
#
#     @mark.marker_name1
#     @mark.usefixtures('I_handle_DB_URL_FILE_in_class')
#     def test_method_01(self):
#         print(" --> test_method_01", end=' ')
#         assert True
#
#     @mark.usefixtures('I_handle_DB_URL_FILE_in_class')
#     def test_method_02(self):
#         print(" --> test_method_02", end=' ')
#         assert True
#
#     @mark.marker_name1
#     def test_method_03(self):
#         print(" --> test_method_03", end=' ')
#         assert True
#
#
# # Without unittest.TestCase heritage
# class check_01_Tests(repeating_calls): pass
#
#
# # With unittest.TestCase heritage
# class check_02_TestCase_Tests(unittest.TestCase, repeating_calls): pass

'''
test_fictures.py::check_01_Tests::test_method_01  --> connect to DB/URL/FILE in class  --> test_method_01 PASSED
test_fictures.py::check_01_Tests::test_method_02  --> test_method_02 PASSED
test_fictures.py::check_01_Tests::test_method_03  --> test_method_03 PASSED --> disconnect from DB/URL/FILE in class
test_fictures.py::check_02_TestCase_Tests::test_method_01  --> connect to DB/URL/FILE in class  --> test_method_01 PASSED
test_fictures.py::check_02_TestCase_Tests::test_method_02  --> test_method_02 PASSED
test_fictures.py::check_02_TestCase_Tests::test_method_03  --> test_method_03 PASSED --> disconnect from DB/URL/FILE in class 
'''


# Fixtures can be out or included into a class or upgrade to the conftest.py file if needed in different files
# with the 'package' or 'session' scope
#
# in conftest.py :
# @fixture(scope='session')
# def I_handle_DB_URL_FILE_in_class():
#     print(" --> connect to DB/URL/FILE in class", end=' ')
#     yield
#     print(" --> disconnect from DB/URL/FILE in class", end=' ')
#
# in test file
class repeating_calls():

    @mark.marker_name2
    @mark.usefixtures('I_handle_DB_URL_FILE_in_class')
    def test_method_01(self):
        print(" --> test_method_01", end=' ')
        assert True

    @mark.usefixtures('I_handle_DB_URL_FILE_in_class')
    def test_method_02(self):
        print(" --> test_method_02", end=' ')
        assert True

    @mark.marker_name2
    def test_method_03(self):
        print(" --> test_method_03", end=' ')
        assert True

    @mark.marker_name4
    @mark.usefixtures('different_values_tested_in_param')
    def test_method_04(self, different_values_tested_in_param):
        print(f" --> test_method_04 says {different_values_tested_in_param} > 0", end=' ')
        assert different_values_tested_in_param > 0

    @mark.marker_name4
    @pytest.mark.usefixtures("value_given_by_fixture")
    def test_method_05(self):
        print(f" --> test_method_05 says {self.input[1]} > 0", end=' ')
        assert self.input[1] > 0




# Without unittest.TestCase heritage
class check_01_Tests(repeating_calls): pass

# With unittest.TestCase heritage
class check_02_TestCase_Tests(unittest.TestCase, repeating_calls):pass



''' With the 'session' scope, the DB is opened only once at the beginning of all tests,
    even if they are in differents test files, and closed at the end
>>> pytest -v -s -m marker_name2
test_fictures.py::check_01_Tests::test_method_01  --> connect to DB/URL/FILE in class  --> test_method_01 PASSED
test_fictures.py::check_01_Tests::test_method_03  --> test_method_03 PASSED
test_fictures.py::check_02_TestCase_Tests::test_method_01  --> test_method_01 PASSED
test_fictures.py::check_02_TestCase_Tests::test_method_03  --> test_method_03 PASSED
test_marks.py::check_04_TestCase_Tests::test_method_01 PASSED
test_marks.py::check_04_TestCase_Tests::test_method_02 PASSED
test_marks.py::check_04_TestCase_Tests::test_method_03 SKIPPED --> disconnect from DB/URL/FILE in class
'''

# At least, fixtures can return values to test and be parametrized to test different values (not on TestCase)
#
# Use the request.cls.input to set a value or a dictionary like {'key':'value'}
#     @fixture(scope="class")
#     def value_given_by_fixture(request):
#         request.cls.input = [10,20]
#
# And the self.input option to get it into the test_method
#     @pytest.mark.usefixtures("value_given_by_fixture")
#     def test_method_05(self):
#         print(f" --> test_method_05 says {self.input[1]} > 0", end=' ')
#         assert self.input[1] > 0
#
# Or use the params option into the fixture and the request.param to return them one by one to the test_method
#     @fixture(scope='function', params=[10,20])
#     def value_in_parameter(request):                                # param and request are keywords
#         print(f" --> fixture opened with {request.param}", end=' ')
#         return request.param
#
#     @mark.usefixtures('different_values_tested_in_param')
#     def test_method_04(self, different_values_tested_in_param):
#         print(f" --> test_method_04 says {different_values_tested_in_param} > 0", end=' ')
#         assert different_values_tested_in_param > 0
#
# But params is not supported by unittest.TestCase
'''  
>>> pytest -v -k test_fictures.py -m 'marker_name4' -s
test_fictures.py::check_01_Tests::test_method_04[10]  --> fixture opened with 10  --> test_method_04 says 10 > 0 PASSED
test_fictures.py::check_01_Tests::test_method_04[20]  --> fixture opened with 20  --> test_method_04 says 20 > 0 PASSED
test_fictures.py::check_01_Tests::test_method_05  --> test_method_05 says 20 > 0 PASSED
test_fictures.py::check_02_TestCase_Tests::test_method_04 ERROR
test_fictures.py::check_02_TestCase_Tests::test_method_05  --> test_method_05 says 20 > 0 PASSED
'''