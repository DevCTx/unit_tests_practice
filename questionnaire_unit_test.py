import json
import os.path
import sys
import unittest

from unittest.mock import patch

import pytest
from pytest import fixture

import http.server
import socketserver
import threading

import questionnaire


class _01_load_json_argv(unittest.TestCase):
    # The questionnaire needs a JSON file to load for being able to display the questions
    # A single .json file must be passed as an argument to the questionnaire.py
    # and must be able to be load by the load_json_argv() function
    # if not, the function return None and the program must exit with
    script_name = 'questionnaire.py'
    test_data_folder = ''
    server_adr = ''
    test_args = []

    def return_value_expected(self, test_args, json_expected=True, file_path_expected=True):
        print(f"\n{' '.join(test_args)} -> {'Json_Data' if json_expected else 'None'},"
              f" {'File_Path' if file_path_expected else 'None'}")
        with patch.object(sys, 'argv', test_args):
            json_returned, filepath_returned = questionnaire.load_json_argv(test_args)
            # Tests json_returned
            if json_expected:
                self.assertIsNotNone(json_returned)
            else:
                self.assertIsNone(json_returned)
            # Tests filepath_returned
            if file_path_expected:
                self.assertIsNotNone(filepath_returned)
            else:
                self.assertIsNone(filepath_returned)

    def test_01_load_json_argv_with_one_good_json_file(self):
        test_args = [self.script_name,
                     os.path.join(self.server_adr, self.test_data_folder, 'initial_json_test_file.json')]
        self.return_value_expected(test_args)

    def test_02_load_json_argv_with_no_argv(self):
        path = os.path.join(self.server_adr, self.test_data_folder)
        if path != '':
            test_args = [self.script_name, os.path.join(self.server_adr, self.test_data_folder)]
            self.return_value_expected(test_args, None)
        else:
            test_args = [self.script_name]
            self.return_value_expected(test_args, None, None)

    # def test_03_load_json_argv_with_more_than_one_argv(self):
    #     test_args = [self.script_name,
    #                  os.path.join( self.server_adr, self.test_data_folder,'initial_json_test_file.json.json'),
    #                  os.path.join( self.server_adr, self.test_data_folder,'second_json_test_file.json')]
    #     self.return_value_expected(test_args, None, None)
    #
    # def test_04_load_json_argv_with_argv_without_json_extension(self):
    #     test_args = [self.script_name,
    #                  os.path.join( self.server_adr,self.test_data_folder,'json_file_without_extension')]
    #     self.return_value_expected(test_args, None)
    #
    # def test_05_load_json_argv_with_non_existent_json_file(self):
    #     test_args = [self.script_name,
    #                  os.path.join(self.server_adr,self.test_data_folder, 'non-existent-file.json')]
    #     self.return_value_expected(test_args, None)
    #
    # def test_06_load_json_argv_with_empty_json_file(self):
    #     test_args = [self.script_name,
    #                  os.path.join(self.server_adr,self.test_data_folder,'empty.json')]
    #     self.return_value_expected(test_args, None)


#
# class _02_load_json_argv_with_another_name(_01_load_json_argv):
#     # If the name of the questionnaire.py change, the error messages must be adapted.
#     script_name = 'test.py'
#
class _03_load_json_argv_with_file_in_folder(_01_load_json_argv):
    # If argv file is in a data folder, it should be working as well
    test_data_folder = 'json_file_tests/'


# class _04_load_json_argv_with_file_in_folder_and_another_name(_02_load_json_argv_with_another_name,
#                                                               _03_load_json_argv_with_file_in_folder):
#     # Must be able to combine both : another name for the questionnaire.py and a folder for the data to display
#     pass
#
# class _05_load_json_argv_with_data_online(unittest.TestCase):
#     # Must be able to work with a json file online : here is a test of simple json file
#     script_name = 'questionnaire.py'
#     def return_value_expected(self, test_args, json_expected=True, file_path_expected=True):
#         print(f"\n{' '.join(test_args)} -> {'Json_Data' if json_expected else 'None' },"
#                                         f" {'File_Path' if file_path_expected else 'None'}")
#         with patch.object(sys, 'argv', test_args):
#             json_returned, filepath_returned = questionnaire.load_json_argv(test_args)
#             # Tests json_returned
#             if json_expected:
#                 self.assertIsNotNone(json_returned)
#             else:
#                 self.assertIsNone(json_returned)
#             # Tests filepath_returned
#             if file_path_expected:
#                 self.assertIsNotNone(filepath_returned)
#             else:
#                 self.assertIsNone(filepath_returned)
#
#     def test_01_load_json_argv_with_json_file_sample_online(self):
#         test_args = [self.script_name, 'https://countwordsfree.com/example.json']
#         self.return_value_expected(test_args)
#
#     def test_02_load_json_argv_with_invalid_json_file_sample_online(self):
#         test_args = [self.script_name, 'https://countwordsfree.com/non-existant.json']
#         self.return_value_expected(test_args, None)
#
#     def test_03_load_json_argv_with_invalid_url(self):
#         test_args = [self.script_name, 'https://countwordsfre.com/example.json']
#         self.return_value_expected(test_args, None)
#
#     def test_04_load_json_argv_with_empty_or_uncompleted_file_online(self):
#         test_args = [self.script_name, 'https://countwordsfree.com/empty_or_uncompleted_file']
#         self.return_value_expected(test_args, None)


# Thread Server Handler for test_load_json_argv_with_json_argv_online
# documentation at https://docs.python.org/fr/3/library/http.server.html
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class _06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown(_03_load_json_argv_with_file_in_folder):
    # Here is simulation of a simple HTTP server via localhost for being able to test more files (simulated online)
    # This is launched as Thread and uses a Thread Server Handler http.server.SimpleHTTPRequestHandler
    # Equivalent to `python -m http.server` into a thread
    # documentation at https://docs.python.org/fr/3/library/http.server.html

    # CAREFUL : localhost not always recognized, better to use 127.0.0.1
    # Port 0 can also be used and means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 8000
    server_adr = f"http://{HOST}:{PORT}/"
    # Open a HTTP server to access to the current directory
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = None

    def setUp(self) -> None:
        self.httpd = ThreadedTCPServer((self.HOST, self.PORT), self.Handler)
        if self.httpd:
            # Start a thread with the server
            server_thread = threading.Thread(target=self.httpd.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True
            server_thread.start()
            print(f"\n\nConnection to {self.server_adr} in {server_thread.name}", end=' ')

    def tearDown(self) -> None:
        print(f"\nDisconnection from {self.server_adr}")
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        self.server_adr = ''

@unittest.skipUnless( 'pytest' in sys.argv[0] or 'PYTEST_CURRENT_TEST' in os.environ, reason='requires pytest')
# Use 'pytest' in sys.argv[0] because 'PYTEST_CURRENT_TEST' in os.environ can be used only after 1 test ran
class _07_load_json_argv_with_data_via_localhost_8000_in_fixture(_03_load_json_argv_with_file_in_folder):
    # Here is simulation of a simple HTTP server via localhost for being able to test more files (simulated online)
    # This is launched as Thread and need the Thread Server Handler

    # CAREFUL : localhost not always recognized, better to use 127.0.0.1
    # Port 0 can also be used and means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 8000
    server_adr = f"http://{HOST}:{PORT}/"
    Handler = http.server.SimpleHTTPRequestHandler  # Open a HTTP server to access to the current directory
    httpd = None

    @pytest.fixture(scope='class', autouse=True)
    def fixture_HTTPServer_Handler(self):
        self.HTTPServer_Connection()
        yield
        self.HTTPServer_Disconnection()

    def HTTPServer_Connection(self):
        self.httpd = ThreadedTCPServer((self.HOST, self.PORT), self.Handler)
        if self.httpd:
            # ip, port = self.httpd.server_address
            # self.server_adr = f"http://{ip}:{port}/"\     # Careful : issues with properties in thread using fixtures

            # Start a thread with the server
            server_thread = threading.Thread(target=self.httpd.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True
            server_thread.start()
            print(f"\n\nHTTP Connection to {self.server_adr} in {server_thread.name}", end=' ')

    def HTTPServer_Disconnection(self):
        print(f"\nHTTP Disconnection from {self.server_adr}")
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        self.server_adr = ''


class _08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass(_03_load_json_argv_with_file_in_folder):
    # CAREFUL : localhost not always recognized, better to use 127.0.0.1
    # Port 0 can also be used and means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 8000
    server_adr = f"http://{HOST}:{PORT}/"
    # Open a HTTP server to access to the current directory
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadedTCPServer((cls.HOST, cls.PORT), cls.Handler)
        if cls.httpd:
            # Start a thread with the server
            server_thread = threading.Thread(target=cls.httpd.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True
            server_thread.start()
            print(f"\n\nConnection to {cls.server_adr} in {server_thread.name}", end=' ')

    @classmethod
    def tearDownClass(cls) -> None:
        print(f"\nDisconnection from {cls.server_adr}")
        if cls.httpd:
            cls.httpd.shutdown()
            cls.httpd.server_close()
        cls.server_adr = ''


class _09_load_json_argv_with_simulated_server(unittest.TestCase):
    # Use the patch method to simulate the answer of an HTTP Server
    script_name = 'questionnaire.py'
    test_data_folder = ''
    server_adr = 'http://non-existent-url.com/'    # non existent url

    def return_value_expected(self, test_args, json_expected=True, file_path_expected=True):
        print(f"\n{' '.join(test_args)} -> {'Json_Data' if json_expected else 'None' },"
                                        f" {'File_Path' if file_path_expected else 'None'}")
        with patch.object(sys, 'argv', test_args):
            json_returned, filepath_returned = questionnaire.load_json_argv(test_args)
            # Tests json_returned
            if json_expected:
                self.assertIsNotNone(json_returned)
            else:
                self.assertIsNone(json_returned)
            # Tests filepath_returned
            if file_path_expected:
                self.assertIsNotNone(filepath_returned)
            else:
                self.assertIsNone(filepath_returned)

    def test_01_load_json_argv_with_simulated_FileNotFound_answer(self):
        json_filename = 'initial_json_test_file.json'
        test_args = [self.script_name, os.path.join(self.server_adr,self.test_data_folder, json_filename)]

        with patch("requests.get") as request_get_mock:
            request_get_mock.return_value(None)
            request_get_mock.return_value.status_code = 404     # File Not Found
            self.return_value_expected(test_args, None)

    def test_02_load_json_argv_with_simulated_success_request_and_fake_data(self):
        json_filename = 'initial_json_test_file.json'
        test_args = [self.script_name, os.path.join(self.server_adr,self.test_data_folder, json_filename)]

        local_json_filename = os.path.join(self.test_data_folder, json_filename)
        json_data = questionnaire.load_json_data_from_file(local_json_filename)

        with patch("requests.get") as request_get_mock:
            request_get_mock.return_value(None)
            request_get_mock.return_value.status_code = 200             # Success to File
            request_get_mock.return_value.text = json.dumps(json_data)  # Simulates the string read online

            with patch("json.loads") as json_loads_mock:
                json_loads_mock.return_value = json_data             # Simulates the json data loads from URL string

                self.return_value_expected(test_args)


# class Unit_Tests_Question( unittest.TestCase ):
#
#     def test_poser_question_bonne_mauvaise_reponse(self):
#         choix = ("choix_1","choix_2","choix_3","choix_4")
#         q = questionnaire.Question("titre",choix,"choix_2")
#         with patch("builtins.input", return_value="1"):
#             self.assertFalse(q.poser(1),"Mauvaise réponse")
#         with patch("builtins.input", return_value="2"):
#             self.assertTrue( q.poser(1),"Bonne Réponse")
#         with patch("builtins.input", return_value="3"):
#             self.assertFalse( q.poser(1))
#         with patch("builtins.input", return_value="4"):
#             self.assertFalse( q.poser(1))
#
#     def test_poser_question_hors_limites(self):
#         choix = ("choix_1","choix_2","choix_3","choix_4")
#         q = questionnaire.Question("titre",choix,"choix_2")
#         with patch("builtins.input", return_value="5"):
#             with self.assertRaises(RecursionError):
#                 self.assertEqual(q.poser(1), "Valeur suppérieure")
#         with patch("builtins.input", return_value="0"):
#             with self.assertRaises(RecursionError):
#                 self.assertEqual(q.poser(1), "Valeur 0")
#         with patch("builtins.input", return_value="-1"):
#             with self.assertRaises(RecursionError):
#                 self.assertEqual(q.poser(1), "Valeur négative")
#         with patch("builtins.input", return_value="a"):
#             with self.assertRaises(RecursionError):
#                 self.assertEqual( q.poser(1), "Valeur alpha")
#         with patch("builtins.input", return_value="#"):
#             with self.assertRaises(RecursionError):
#                 self.assertEqual( q.poser(1), "Valeur particulière")

# class Unit_Tests_Questionnaire( unittest.TestCase ):
#
#     def test_questionnaire_lancer_alien_debutant(self):
#         filename = os.path.join("test_data","cinema_alien_debutant.json")
#         q = questionnaire.load_json_data_argv(filename)
#         self.assertIsInstance({dict:4},q)


if __name__ == "__main__":
    unittest.main()
