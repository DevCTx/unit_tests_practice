# PROJET QUESTIONNAIRE V3 : POO
#
# - Pratiquer sur la POO
# - Travailler sur du code existant
# - Mener un raisonnement
#
# -> Définir les entitées (données, actions)
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#
import json
import ntpath
import os
import sys

import requests
import validators
import jsonschema
from jsonschema.validators import validate

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printerr(msg):
    return print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")


class Question:
    def __init__(self, title, choice, is_answer):
        self.title = title
        self.choice = choice
        self.is_answer = is_answer

    def FromJSON(json_question):
        # Question : Titre, Choix, Bonne Reponse
        # From JSON Question : Titre, Choix[4]:[Reponse_1,True],[Reponse_2,False],[Reponse_3,False],[Reponse_4,False]
        is_answer = None
        choice = []
        for i in range (0, len(json_question['choix'])):
            choice.append(json_question['choix'][i][0])
            if json_question['choix'][i][1]==True :
# Enregistre le numero de la bonne reponse
#                is_answer = json_question['choix'][i][0]
                is_answer = i
        return Question(json_question['titre'], choice, is_answer)

    def ask(self, index):
        print(f"QUESTION {index}")
        print("  " + self.title)
        for i in range(len(self.choice)):
            print("  ", i+1, "-", self.choice[i]+"\n")

        if Question.request_choice_to_user(1, len(self.choix)) == self.is_answer:
            print("Bonne réponse\n")
            return True
        else:
            print("Mauvaise réponse\n")
            return False

    def request_choice_to_user(min, max):
        str_answer = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            int_answer = int(str_answer)
            if min <= int_answer <= max:
                return int_answer
            else:
                print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.request_choice_to_user(min, max)
    
class Questionnaire:

    schema = {
        "$schema": "http://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [ "titre", "questions" ],
        "properties": {
            "categorie": {"type": "string"},
            "titre": {"type": "string"},
            "questions": {
                "type": "array",
                "default": [],
                "items": {
                    "type": "object",
                    "properties": {
                        "titre": {"type": "string"},
                        "choix": {
                            "type": "array",
                            "minItems": 2,
                            "items": {
                                "type": "array",
                                "minItems": 2,
                                "prefixItems": [{"type": "string"}, {"type": "boolean"}],
                                "items": False
                            }
                        }
                    }
                }
            },
            "difficulte": {"type": "string"}
        }
    }

    def __init__(self, json_questionnaire):
        '''Test the expected json schema before to initiate'''

        try
            validate(json_questionnaire, self.schema)
        except jsonschema.exceptions.ValidationError:
            printerr(f"Incompatible Json schema in file : {filename}")
        else:
            # 'categorie', 'difficulte' : non-blocking properties, but better to be completed as unknown if absent
            self.categorie = json_questionnaire['categorie'] if json_questionnaire.get('categorie') else 'inconnue'
            self.difficulte = json_questionnaire['difficulte'] if json_questionnaire.get('difficulte') else 'inconnue'

            # 'titre' or 'questions' : required properties already checked into schema
            self.titre = json_questionnaire['titre']
            self.questions = []
            for json_question in json_questionnaire['questions']:
                self.questions.append( Question.FromJSON(json_question) )

    def run(self):
        # Launch of the questionnaire
        print(f"Catégorie : {self.categorie}")
        print(f"Difficulté : {self.difficulte}")
        print(f"Titre : {self.titre}\n")

        score = 0
        index = 0
        for question in self.questions:
            index+=1
            if question.ask(index):
                score += 1

        print("Score final :", score, "sur", len(self.questions))
        return score



def load_json_argv( sysargv ):
    '''Return the json questionnaire if correctly loaded else None'''
    json_data = None

    if len(sysargv)!=2:
        printerr (f"Error in argument, should add one .json questionnaire. Example : {ntpath.basename(sys.argv[0])} questionnaire_to_read.json")
        return None

    root, extension = os.path.splitext( sysargv[1] )
    if extension!=".json":
        printerr(f"Incorrect extension, add a .json questionnaire. Example : {ntpath.basename(sys.argv[0])} questionnaire_to_read.json")
        return None

    filename = sysargv[1]

    if validators.url(filename) :    # si le fichier JSON est une URL
        try:
            response = requests.get(filename)
        except:
            raise Exception("here")
        else:
            if response.status_code == 404:
                printerr(f"Url Not found at : {filename}")
                return None
            else:
                try:
                    json_data = json.loads(response.text)
                except:
                    printerr(f"Incompatible or no data in JSON file at URL : {filename}")
                    return None
    else:
        try:    # Opening of the JSON file
            json_file = open(filename, "r")
        except OSError:
            printerr(f"Invalid File : {filename}")
            return None
        except FileNotFoundError:
            printerr(f"No File : {filename}")
            return None
        else:
            with json_file:     # Handle the memory needed for the file
                try:    # Loading of the file as compatible JSON file
                    json_data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    printerr(f"Incompatible or no data in JSON file : {filename}")
                    return None

    return json_data



def main():

    json_data = load_json_argv( sys.argv )

    if json_data:
       Questionnaire(json_data).run()

if __name__ == "__main__":
    main()
