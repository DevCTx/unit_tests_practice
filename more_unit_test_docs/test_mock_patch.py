import unittest
from unittest import mock

from simple_prog import second_API, third_API

class Test_API(unittest.TestCase):

    # Here is a example of mock.patch used as decorator
    @mock.patch('simple_prog.third_API.get_data', return_value="data3")
    @mock.patch('simple_prog.second_API.get_data', return_value="data2")
    def test_01_mock_patch_decorator(self, represents_closer_patch, represents_farthest_patch):
        self.assertEqual(second_API().get_data(), 'data2')
        self.assertEqual(third_API().get_data(), 'data3')

    # We can do the same using the 'with' statement / No argument needed
    def test_02_mock_patch_with_statement(self):
        with mock.patch('simple_prog.second_API.get_data', return_value="data2"):
            with mock.patch('simple_prog.third_API.get_data', return_value="data3"):
                self.assertEqual(second_API().get_data(), 'data2')
                self.assertEqual(third_API().get_data(), 'data3')

    # Or separatly
    def test_03_separate_second_API(self):
        with mock.patch('simple_prog.second_API.get_data', return_value="data2"):
            self.assertEqual(second_API().get_data(), 'data2')

    def test_04_separate_third_API(self):
        with mock.patch('simple_prog.third_API.get_data', return_value="data3"):
            self.assertEqual(third_API().get_data(), 'data3')

    # It is also possible to add setUp and tearDown, respectively executed before or after the test function
    def setUp(self) -> None:
        self.second_API_patch = mock.patch('simple_prog.second_API.get_data', return_value="data2")
        self.third_API_patch = mock.patch('simple_prog.third_API.get_data', return_value="data3")
        self.second_API_patch.start()
        self.third_API_patch.start()

    def test_05_with_setup_teardown(self):
        self.assertEqual(second_API().get_data(), 'data2')
        self.assertEqual(third_API().get_data(), 'data3')

    def tearDown(self) -> None:
        self.second_API_patch.stop()
        self.third_API_patch.stop()

    # A test function can also return different value, depending of the number of calls
    def test_06_side_effects(self):
        with mock.patch('simple_prog.second_API.get_data', side_effect=["data2", "data3", "data4"]):
            # first call should return 'data2'
            self.assertEqual(second_API().get_data(), 'data2')
            # second call should return 'data3'
            self.assertEqual(second_API().get_data(), 'data3')
            # third call should return 'data4'
            self.assertEqual(second_API().get_data(), 'data4')

    # This can also be used for Exception calls
    def test_07_mock_patch_exception(self):
        with mock.patch('simple_prog.second_API.get_data', side_effect=Exception("Boom!")) as second_API_patch:
            # self.assertEqual( second_API().get_data(),'data2')  #Return 'Exception: Boom!'
            self.assertRaises(Exception, second_API_patch)

    # mock.patch can be changed as mock.patch.object to facilitate the reading
    def test_08_with_mock_patch_object(self):
        with mock.patch.object(second_API, 'get_data', return_value="data2"):
            self.assertEqual(second_API().get_data(), 'data2')


