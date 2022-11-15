import os.path
import unittest
from unittest.mock import patch
import questionnaire

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

class Unit_Tests_Questionnaire( unittest.TestCase ):

    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("test_data","cinema_alien_debutant.json")
        q = questionnaire.Questionnaire.From_JSON_Questionnaire(filename)
        self.assertIsNone(q)

if __name__ == "__main__":
    unittest.main()