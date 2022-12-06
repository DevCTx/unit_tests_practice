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
    return print(f"{bcolors.FAIL}Error : {msg}{bcolors.ENDC}")


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
        for i in range(0, len(json_question['choix'])):
            choice.append(json_question['choix'][i][0])
            if json_question['choix'][i][1] == True:
                is_answer = i + 1
        return Question(json_question['titre'], choice, is_answer)

    def ask(self, index):
        print(f"QUESTION {index}")
        print("  " + self.title)
        for i in range(len(self.choice)):
            print("  ", i + 1, "-", self.choice[i])

        if Question.request_choice_to_user(1, len(self.choice)) == self.is_answer:
            print("Bonne réponse\n")
            return True
        else:
            print("Mauvaise réponse\n")
            return False

    def request_choice_to_user(min, max):
        str_answer = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") : ")
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
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["titre", "questions"],
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

    def __init__(self, json_questionnaire, file_path):
        '''Test the expected json schema before to initiate'''

        try:
            validate(json_questionnaire, self.schema)
        except jsonschema.exceptions.ValidationError:
            printerr(f"Incompatible Json schema in file {file_path}")
        else:
            # 'titre' or 'questions' are required properties
            # all the types are already verified into the schema validator but the len=0 may also identify an error
            if len(json_questionnaire.get('titre')) <= 0:
                printerr(f"The title of the quizz is missing in file {file_path}")
            else:
                self.titre = json_questionnaire['titre']

                # 'categorie', 'difficulte' : non-critical properties, but better to be completed as unknown if absent
                self.categorie = json_questionnaire['categorie'] if json_questionnaire.get('categorie') else 'inconnue'
                self.difficulte = json_questionnaire['difficulte'] if json_questionnaire.get(
                    'difficulte') else 'inconnue'

                self.questions = []
                for idx, json_question in enumerate(json_questionnaire['questions']):
                    if len(json_question['titre']) <= 0:  # This is not critical but the question won't be added
                        printerr(f"Skipped question : nothing to ask in question {idx} file {file_path}")
                    else:
                        good_answers = [choix[0] for choix in json_question['choix'] if choix[1] == True]
                        if len(good_answers) != 1:  # This is not critical but the question won't be added
                            printerr(f"Skipped question : no one or more than one good answer "
                                     f"in question {idx} file {file_path}")
                        else:
                            self.questions.append(Question.FromJSON(json_question))

    def run(self):
        score = 0
        index = 0
        try:
            # Launch of the questionnaire
            print(f"=== QUESTIONNAIRE ===")
            print(f"Catégorie : {self.categorie}")
            print(f"Difficulté : {self.difficulte}")
            print(f"Titre : {self.titre}\n")
            if len(self.questions) <= 0:
                print("No compatible question in this quizz")
            else:
                for question in self.questions:
                    index += 1
                    if question.ask(index):
                        score += 1

                print("Score final :", score, "sur", len(self.questions))
        except:
            pass
        return score


def load_json_argv(sysargv):
    '''Return the json questionnaire if correctly loaded else None'''
    json_data = None

    if len(sysargv) != 2:
        printerr(
            f"Error in argument, should add a single .json questionnaire. Example : {ntpath.basename(sys.argv[0])} questionnaire_to_read.json")
        return None, None

    sysargv_path = sysargv[1]

    root, extension = os.path.splitext(sysargv_path)
    if extension != ".json":
        printerr(
            f"Incorrect extension, add a .json questionnaire. Example : {ntpath.basename(sys.argv[0])} questionnaire_to_read.json")
        return None, sysargv_path

    if validators.url(sysargv_path):  # si le fichier JSON est une URL
        json_data = load_json_data_from_URL(sysargv_path)
    else:
        json_data = load_json_data_from_file(sysargv_path)

    return json_data, sysargv_path

def load_json_data_from_URL(URL_path):
    try:
        response = requests.get(URL_path)
    except:
        printerr(f"Invalid URL at {URL_path}")
        return None
    else:
        if response.status_code == 404:
            printerr(f"File not found at URL {URL_path}")
            return None
        else:
            try:
                json_data = json.loads(response.text)  # Decode JSON String
            except:
                printerr(f"Incompatible or no data in JSON file at URL {URL_path}")
                return None
    return json_data

def load_json_data_from_file(file_path):
    try:  # Opening of the JSON file
        json_file = open(file_path, "r")
    except OSError:
        printerr(f"Invalid permissions or path to {file_path}")
        return None
    else:
        with json_file:  # Handle the memory needed for the file
            try:
                json_data = json.load(json_file)  # Read File and Decode JSON String
            except json.decoder.JSONDecodeError:
                printerr(f"Incompatible or no data in JSON file {file_path}")
                return None
    return json_data

def main():
    json_data, file_path = load_json_argv(sys.argv)

    if json_data:
        Questionnaire(json_data, file_path).run()


if __name__ == "__main__":
    main()
