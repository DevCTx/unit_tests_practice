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
import unicodedata

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
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromData(data):
        # Question : Titre, Choix, Bonne Reponse
        # From Data : Choix, Bonne Reponse, Titre
        q = Question(data[2], data[0], data[1])
        return q

    def FromJSON(json_question):
        # Question : Titre, Choix, Bonne Reponse
        # From JSON Question : Titre, Choix[4]:[Reponse_1,True],[Reponse_2,False],[Reponse_3,False],[Reponse_4,False]
        bonne_reponse = None
        choix = []
        for i in range (0, len(json_question['choix'])):
            choix.append(json_question['choix'][i][0])
            if json_question['choix'][i][1]==True :
                bonne_reponse = json_question['choix'][i][0]
        return Question(json_question['titre'], choix, bonne_reponse)

    def poser(self, index):
        print(f"QUESTION {index}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:

    schema = {
        "$schema": "json_questionnaire",
        "$id": "https://openquizzdb.org/",
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
                            "default": [],
                            "minItems": 2,
                            "items": {
                                "type": "array",
                                "default": []
                            }
                        }
                    }
                }
            },
            "difficulte": {"type": "string"}
        }
    }

    def __init__(self, json_questionnaire):

        # Verification du format questionnaire (categorie et difficulte non bloquant, titre ou questions bloquants)
        self.categorie = json_questionnaire['categorie'] if json_questionnaire.get('categorie') else 'inconnue'
        self.difficulte = json_questionnaire['difficulte'] if json_questionnaire.get('difficulte') else 'inconnue'

        if not json_questionnaire.get('titre') or not json_questionnaire.get('questions'):
            raise Exception("JSON_Questionnaire_format_error")
        else:
            self.titre = json_questionnaire['titre']
            self.questions = []
            for json_question in json_questionnaire['questions']:
                self.questions.append( Question.FromJSON(json_question) )

    # # Convertit un questionnaire JSON en questions sous format questionnaire
    # def From_JSON_Questionnaire(self, json_questionnaire):
    #     if json_questionnaire != None :
    #         for json_question in json_questionnaire['questions']:
    #             questions.append( Question.FromJSON(json_question) )
    #     return questions

    def lancer(self):
        # Lancement du questionnaire
        print(f"Catégorie : {self.categorie}")
        print(f"Difficulté : {self.difficulte}")
        print(f"Titre : {self.titre}\n")

        score = 0
        index = 0
        for question in self.questions:
            index+=1
            if question.poser(index):
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
    # if json_data :
    #     Questionnaire(json_data).lancer()

if __name__ == "__main__":
    main()
