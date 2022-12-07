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


def print_error(msg):
    return print(f"{bcolors.FAIL}Error : {msg}{bcolors.ENDC}")

def print_warning(msg):
    return print(f"{bcolors.WARNING}Warning : {msg}{bcolors.ENDC}")

def print_bold(msg):
    return print(f"{bcolors.BOLD}{msg}{bcolors.ENDC}")

class Question:
    def __init__(self, title, choice, is_answer):
        self.title = title
        self.choice = choice
        self.is_answer = is_answer

    def ask(self, index, nb_questions):
        print_bold(f"QUESTION {index}/{nb_questions}")
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
                    "required": ["titre", "choix"],
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

    def __new__(cls, json_questionnaire, file_path):
        '''Test the expected json schema before to initiate a Questionnaire'''
        try:
            validate(json_questionnaire, cls.schema)
        except jsonschema.exceptions.ValidationError:
            print_error(f"Incompatible Json schema in file {file_path}")
            return None
        else:
            # 'titre' or 'questions' are required properties
            # all the types are already verified into the schema validator but the len=0 may also identify an error
            if len(json_questionnaire.get('titre')) <= 0:
                print_error(f"The title of the quizz is missing and mandatory in file {file_path}")
                return None
            else:
                if len(json_questionnaire.get('questions')) <= 0:
                    print_error(f"The questions of the quizz are missing and mandatory in file {file_path}")
                    return None
                else:
                    return super().__new__(cls)

    def __init__(self, json_questionnaire, file_path):
        '''Initiate a Questionnaire after __new__ checked the required settings'''

        self.titre = json_questionnaire['titre']

        # 'categorie', 'difficulte' : non-critical properties, but better to be completed as unknown if absent
        self.categorie = json_questionnaire['categorie'] if json_questionnaire.get('categorie') else 'inconnue'
        self.difficulte = json_questionnaire['difficulte'] if json_questionnaire.get('difficulte') else 'inconnue'

        self.questions = []
        for idx, json_question in enumerate(json_questionnaire['questions']):
            if len(json_question['titre']) <= 0:  # This is not critical but the question won't be added
                print_warning(f"Skipped question : question is empty in question {idx+1} file {file_path}")
            else:
                # Print a warning message if one answer of the question is empty
                # Must be done before to check the boolean because the good answer may have an empty string

                for idc, choice in enumerate(json_question['choix']):
                    if len(choice[0]) <= 0:
                        print_warning(f"Skipped answer : answer is empty in question {idx+1} file {file_path}")
                        json_question['choix'].pop(idc)

                good_answer = [(choice[0], idc) for idc, choice in enumerate(json_question['choix']) if choice[1]]
                if len(good_answer) != 1:  # This is not critical but the question won't be added
                    print_warning(f"Skipped question : no one or more than one good answers in question {idx+1} file {file_path}")
                else:
                    answers = [choice[0] for choice in json_question['choix']]
                    self.questions.append(Question(json_question['titre'], answers, good_answer[0][1]+1))

    def run(self):
        score = 0
        index = 0
        try:
            # Launch of the questionnaire
            print_bold(f"=== QUESTIONNAIRE ===")
            print(f"Catégorie : {self.categorie}")
            print(f"Difficulté : {self.difficulte}")
            print(f"Titre : {self.titre}\n")
            if len(self.questions) <= 0:
                # No compatible questions for this quiz
                print("Désolé, aucune question n'est compatible avec ce quizz\n")
            else:
                for question in self.questions:
                    index += 1
                    if question.ask(index,len(self.questions)):
                        score += 1

                print("Score final :", score, "sur", len(self.questions))
        except:
            pass    # Allows to quit the program by Ctrl+C
        return score


def load_json_argv(sysargv):
    '''Return the json questionnaire if correctly loaded else None'''
    json_data = None

    if len(sysargv) != 2:
        print_error(
            f"Error in argument, should add a single .json questionnaire. Example : {os.path.basename(sys.argv[0])} questionnaire_to_read.json")
        return None, None

    sysargv_path = sysargv[1]

    root, extension = os.path.splitext(sysargv_path)
    if extension != ".json":
        print_error(
            f"Incorrect extension, add a .json questionnaire. Example : {os.path.basename(sys.argv[0])} questionnaire_to_read.json")
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
        print_error(f"Invalid URL at {URL_path}")
        return None
    else:
        if response.status_code == 404:
            print_error(f"File not found at URL {URL_path}")
            return None
        else:
            try:
                json_data = json.loads(response.text)  # Decode JSON String
            except:
                print_error(f"Incompatible or no data in JSON file at URL {URL_path}")
                return None
    return json_data

def load_json_data_from_file(file_path):
    try:  # Opening of the JSON file
        json_file = open(file_path, "r")
    except OSError:
        print_error(f"Invalid permissions or path to {file_path}")
        return None
    else:
        with json_file:  # Handle the memory needed for the file
            try:
                json_data = json.load(json_file)  # Read File and Decode JSON String
            except json.decoder.JSONDecodeError:
                print_error(f"Incompatible or no data in JSON file {file_path}")
                return None
    return json_data

def main():
    json_data, file_path = load_json_argv(sys.argv)

    if json_data:
        questionnaire = Questionnaire(json_data, file_path)
        if questionnaire :
            questionnaire.run()


if __name__ == "__main__":
    main()
