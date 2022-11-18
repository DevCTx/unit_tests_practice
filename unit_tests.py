import os.path
import sys
import unittest
from unittest.mock import patch

import questionnaire

import http.server
import socketserver
import threading

# MOCK is used to replace something that is used or existed in the scope (here : questionnaire.py)
# PATCH is used to replace something that is imported or created by the scope (here : questionnaire.py)
# Great simple documentation at https://queirozf.com/entries/python-unittest-examples-mocking-and-patching

class _01_load_json_argv(unittest.TestCase):
    # The questionnaire needs a JSON file to load for being able to screen the questions
    # Only one .json file must be passed as argument to the questionnaire.py
    # and must be able to be load by the load_json_argv() function
    # if not, the function return None and the program must exit with
    script_name = 'questionnaire.py'
    test_data_folder = ''
    server_adr = ''

    def test_01_load_json_argv_with_one_good_json_file(self):
        testargs = [self.script_name, os.path.join( self.server_adr,
                                                    self.test_data_folder,'cinema_alien_debutant.json')]
        print(f"\n{self} : Not None (OK) \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNotNone(q)

    def test_02_load_json_argv_with_no_argv(self):
        testargs = [self.script_name]
        print(f"\n{self} : None \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNone(q)

    def test_03_load_json_argv_with_more_than_one_argv(self):
        testargs = [self.script_name,
                     os.path.join( self.server_adr, self.test_data_folder,'cinema_alien_debutant.json'),
                     os.path.join( self.server_adr, self.test_data_folder,'animaux_leschats_debutant.json')]
        print(f"\n{self} : None \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNone(q)

    def test_04_load_json_argv_with_argv_without_json_extension(self):
        testargs = [self.script_name, os.path.join( self.server_adr,
                                                    self.test_data_folder,'json_file_without_extension')]
        print(f"\n{self} : None \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNone(q)

    def test_05_load_json_argv_with_non_existent_json_file(self):
        testargs = [self.script_name, os.path.join( self.server_adr,
                                                    self.test_data_folder,'non-existent-file.json')]
        print(f"\n{self} : None \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNone(q)

    def test_06_load_json_argv_with_empty_json_file(self):
        testargs = [self.script_name,  os.path.join( self.server_adr,
                                                    self.test_data_folder,'empty.json')]
        print(f"\n{self} : None \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNone(q)


class _02_load_json_argv_with_another_name(_01_load_json_argv):
    script_name = 'test.py'

class _03_load_json_argv_with_file_in_folder(_01_load_json_argv):
    test_data_folder = 'test_data'

class _04_load_json_argv_with_file_in_folder_and_another_name(_02_load_json_argv_with_another_name,
                                                              _03_load_json_argv_with_file_in_folder):
    pass

class _05_load_json_argv_with_data_online(unittest.TestCase):
    def test_load_json_argv_with_json_file_sample_online(self):
        testargs = ['questionnary.py', 'https://countwordsfree.com/example.json']
        print(f"\n{self} : Not None (OK) \n{' '.join(testargs)}")
        with patch.object(sys, 'argv', testargs):
            q = questionnaire.load_json_argv(testargs)
            self.assertIsNotNone(q)

# # Thread Server Handler for test_load_json_argv_with_json_argv_online
# # documentation at https://docs.python.org/fr/3/library/http.server.html
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class _06_load_json_argv_with_data_via_localhost_8000(_01_load_json_argv):
    # CAREFUL : localhost not always recognized, may be prudent to use 127.0.0.1
    # Port 0 can also be used and means to select an arbitrary unused port
    HOST, PORT = "localhost", 8000
    Handler = http.server.SimpleHTTPRequestHandler  # Open a HTTP server to access to the current directory
    httpd = None

    def setUp(self) -> None:
        # Needs to create a temporary server (equivalent to python -m http.server) into a thread
        # documentation at https://docs.python.org/fr/3/library/http.server.html

        self.httpd = ThreadedTCPServer((self.HOST, self.PORT), self.Handler)
        if self.httpd:
            ip, port = self.httpd.server_address
            self.server_adr = f"http://{ip}:{port}/"

            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            server_thread = threading.Thread(target=self.httpd.serve_forever)
            # Exit the server thread when the main thread terminates
            server_thread.daemon = True
            server_thread.start()
            # print(f"\nThis directory is serving at {self.server_adr} in {server_thread.name}")

    def tearDown(self) -> None:
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        self.server_adr = ''





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
