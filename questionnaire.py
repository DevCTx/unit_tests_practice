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
        choix = list()
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
    # def __init__(self, questions):
    #     self.questions = questions

    def __init__(self, json_questionnaire):
        self.questions = self.From_JSON_Questionnaire(json_questionnaire)

    # Convertit un questionnaire JSON en questions sous format questionnaire
    def From_JSON_Questionnaire(self, json_questionnaire):
        questions = []
        if json_questionnaire != None :
            for json_question in json_questionnaire['questions']:
                questions.append( Question.FromJSON(json_question) )
        return questions

    def lancer(self):
        score = 0
        index = 0
        for question in self.questions:
            index+=1
            if question.poser(index):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


"""questionnaire = (
    ("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    ("Quelle est la capitale de l"Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    ("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
                )

lancer_questionnaire(questionnaire)"""

# q1 = Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris")
# q1.poser()

# data = (("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris", "Quelle est la capitale de la France ?")
# q = Question.FromData(data)
# print(q.__dict__)

# Questionnaire(
#     (
#     Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"),
#     Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
#     Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
#     )
# ).lancer()

def main():

    if len(sys.argv)!=2:
        print(f"Argument insuffisant : Entrer un fichier JSON en paramètre, exemple : {ntpath.basename(sys.argv[0])} questionnaire_a_lire.json")
        sys.exit()

    root, extension = os.path.splitext(sys.argv[1])
    if extension!=".json":
        print(f"Extension incorrecte : Entrer un fichier JSON en paramètre, exemple : questionnaire.py questionnaire_a_lire.json")
        sys.exit()

    filename = sys.argv[1]
    try:    # Ouverture du fichier JSON
        json_file = open(filename, "r")
    except:
        print("Aucun fichier :", filename)
        sys.exit()
    else:
        with json_file:
            try:    # Lecture du fichier JSON
                json_questionnaire = json.load(json_file)
            except json.decoder.JSONDecodeError:
                print("Aucune donnée JSON dans fichier :",filename)
                sys.exit()

    # Lancement du questionnaire
    print(f"Catégorie : {json_questionnaire['categorie']}")
    print(f"Titre : {json_questionnaire['titre']}")
    print(f"Difficulté : {json_questionnaire['difficulte']}\n")
    Questionnaire(json_questionnaire).lancer()

if __name__ == "__main__":
    main()
