import json
import os.path
import sys
import unittest
from functools import partial
from unittest.mock import patch
from urllib.parse import urlparse

import questionnaire

import http.server
import socketserver
import threading


class _01_load_json_argv(unittest.TestCase):
    # The questionnaire needs a JSON file to load for being able to display the questions
    # A single .json file must be passed as an argument to the questionnaire.py
    # and must be able to be load by the load_json_argv() function
    # if not, the function return None and the program must exit with
    script_name = 'questionnaire.py'
    test_data_folder = ''
    server_adr = ''
    test_args = []

    def get_test_args(self):
        return self.test_args

    def test_01_load_json_argv_with_one_good_json_file(self):
        self.test_args = [self.script_name, os.path.join( self.server_adr,
                                                    self.test_data_folder,'cinema_alien_debutant.json')]
        print(f"\n{self} : Not None (OK) \n{' '.join(self.test_args)}")
        with patch.object(sys, 'argv', self.test_args):
            q = questionnaire.load_json_argv(self.test_args)
            self.assertIsNotNone(q)
#
#     def test_02_load_json_argv_with_no_argv(self):
#         testargs = [self.script_name]
#         print(f"\n{self} : None \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_03_load_json_argv_with_more_than_one_argv(self):
#         testargs = [self.script_name,
#                      os.path.join( self.server_adr, self.test_data_folder,'cinema_alien_debutant.json'),
#                      os.path.join( self.server_adr, self.test_data_folder,'animaux_leschats_debutant.json')]
#         print(f"\n{self} : None \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_04_load_json_argv_with_argv_without_json_extension(self):
#         testargs = [self.script_name, os.path.join( self.server_adr,
#                                                     self.test_data_folder,'json_file_without_extension')]
#         print(f"\n{self} : None \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_05_load_json_argv_with_non_existent_json_file(self):
#         testargs = [self.script_name, os.path.join( self.server_adr,
#                                                     self.test_data_folder,'non-existent-file.json')]
#         print(f"\n{self} : None \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_06_load_json_argv_with_empty_json_file(self):
#         testargs = [self.script_name,  os.path.join( self.server_adr,
#                                                     self.test_data_folder,'empty.json')]
#         print(f"\n{self} : None \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#
# class _02_load_json_argv_with_another_name(_01_load_json_argv):
#     # If the name of the questionnaire.py change, the error messages must be adapted.
#     script_name = 'test.py'
#
# class _03_load_json_argv_with_file_in_folder(_01_load_json_argv):
#     # If argv file is in a data folder, it should be working as well
#     test_data_folder = 'test_data'
#
# class _04_load_json_argv_with_file_in_folder_and_another_name(_02_load_json_argv_with_another_name,
#                                                               _03_load_json_argv_with_file_in_folder):
#     # Must be able to combine both : another name for the questionnaire.py and a folder for the data to display
#     pass
#
# class _05_load_json_argv_with_data_online(unittest.TestCase):
#     # Must be able to work with a json file online : here is a test of simple json file
#     def test_01_load_json_argv_with_json_file_sample_online(self):
#         testargs = ['questionnary.py', 'https://countwordsfree.com/example.json']
#         print(f"\n{self} : Not None (OK) \n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNotNone(q)
#
#     def test_02_load_json_argv_with_invalid_json_file_sample_online(self):
#         testargs = ['questionnary.py', 'https://countwordsfree.com/example2.json']
#         print(f"\n{self} : None\n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_03_load_json_argv_with_invalid_url(self):
#         testargs = ['questionnary.py', 'https://countwordsfre.com/example.json']
#         print(f"\n{self} : None\n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#     def test_04_load_json_argv_with_empty_or_uncompleted_file_online(self):
#         testargs = ['questionnary.py', 'https://countwordsfree.com/empty_or_uncompleted_file']
#         print(f"\n{self} : None\n{' '.join(testargs)}")
#         with patch.object(sys, 'argv', testargs):
#             q = questionnaire.load_json_argv(testargs)
#             self.assertIsNone(q)
#
#
# Thread Server Handler for test_load_json_argv_with_json_argv_online
# documentation at https://docs.python.org/fr/3/library/http.server.html
# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass
#
# class _06_load_json_argv_with_data_via_localhost_8000(_01_load_json_argv):
#     # Here is simulation of a simple HTTP server via localhost for being able to test more files (simulated online)
#     # This is launched as Thread and need the Thread Server Handler
#
#     # CAREFUL : localhost not always recognized, may be prudent to use 127.0.0.1
#     # Port 0 can also be used and means to select an arbitrary unused port
#     HOST, PORT = "localhost", 8000
#     Handler = http.server.SimpleHTTPRequestHandler  # Open a HTTP server to access to the current directory
#     httpd = None
#
#     def setUp(self) -> None:
#         # Needs to create a temporary server (equivalent to python -m http.server) into a thread
#         # documentation at https://docs.python.org/fr/3/library/http.server.html
#
#         self.httpd = ThreadedTCPServer((self.HOST, self.PORT), self.Handler)
#         if self.httpd:
#             ip, port = self.httpd.server_address
#             self.server_adr = f"http://{ip}:{port}/"
#
#             # Start a thread with the server -- that thread will then start one
#             # more thread for each request
#             server_thread = threading.Thread(target=self.httpd.serve_forever)
#             # Exit the server thread when the main thread terminates
#             server_thread.daemon = True
#             server_thread.start()
#             # print(f"\nThis directory is serving at {self.server_adr} in {server_thread.name}")
#
#     def tearDown(self) -> None:
#         if self.httpd:
#             self.httpd.shutdown()
#             self.httpd.server_close()
#         self.server_adr = ''


# MOCK is used to replace something that is used or existed in the scope (here : questionnaire.py)
# PATCH is used to replace something that is imported or created by the scope (here : questionnaire.py)
# Great simple documentation at https://queirozf.com/entries/python-unittest-examples-mocking-and-patching


class _07_load_json_argv_with_simulating_data_online(unittest.TestCase):
    # Use the patch method to simulate some Must be able to work with a json file online : here is a test of simple json file
    script_name = 'questionnaire.py'
    test_data_folder = ''
    server_adr = 'https://whatever.com/'

    '''
    def test_01_load_json_argv_with_json_file_sample_online(self):
        testargs = ['questionnary.py', 'https://countwordsfre.com/example.json']
        print(f"\n{self} : Not None (OK) \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNotNone(q)

    This call answers :
    test_01_load_json_argv_with_json_file_sample_online (unit_tests._07_load_json_argv_with_data_online) : Not None (OK)
    questionnary.py https://countwordsfre.com/example.json
    Invalid URL at : https://countwordsfre.com/example.json
    '''

    # So we can simulate the requests.get(filename) to get 200 or 404
    def test_01_load_json_argv_with_false_url_and_unsuccessful_requests_get(self):
        with patch("requests.get") as request_get_mock:
            request_get_mock.return_value(None)
            request_get_mock.return_value.status_code = 404     # File Not Found

            testargs = [self.script_name, os.path.join(self.server_adr,
                                                       self.test_data_folder, 'cinema_alien_debutant.json')]
            print(f"\n{self} : None \n{' '.join(testargs)}")
            with patch.object(sys, 'argv', testargs):
                q = questionnaire.load_json_argv(testargs)
                self.assertIsNone(q)

    def test_01_load_json_argv_with_false_url_and_simulated_json_loads(self):
        with patch("requests.get") as request_get_mock:
            request_get_mock.return_value(None)
            request_get_mock.return_value.status_code = 200     # Success to File
            with patch("json.loads") as json_loads_mock:
                json_loads_mock.return_value = {'categorie': 'TEST'}

                testargs = [self.script_name, os.path.join(self.server_adr,
                                                           self.test_data_folder, 'cinema_alien_debutant.json')]

                print(f"\n{self} : Not None (OK)\n{' '.join(testargs)}")
                with patch.object(sys, 'argv', testargs):
                    q = questionnaire.load_json_argv(testargs)
                    self.assertIsNotNone(q)



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
