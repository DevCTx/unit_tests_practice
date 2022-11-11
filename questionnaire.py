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

    def poser(self):
        print("QUESTION")
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
        questions = list()
        if json_questionnaire != None :
            for json_question in json_questionnaire['questions']:
                questions.append( Question.FromJSON(json_question) )
        return questions

    def lancer(self):
        score = 0
        for question in self.questions:
            if question.poser():
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
#     Question("Quelle est la capitale de l"Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
#     Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
#     )
# ).lancer²


json_questionnaire = json.loads("""{"categorie": "Animaux", "titre": "Les chats", "questions": [{"titre": "\u00c0 quelle classe d'animaux vert\u00e9br\u00e9s regroupant pr\u00e8s de 5.400 esp\u00e8ces appartient le chat ?", "choix": [["Mammif\u00e8res", true], ["Reptiles", false], ["Oiseaux", false], ["Poissons", false]]}, {"titre": "Lorsque vous apercevez votre chat faire le gros dos, il est probablement...", "choix": [["En chasse", false], ["Content", false], ["Malade", false], ["Effray\u00e9", true]]}, {"titre": "Que fait principalement le chat de ses journ\u00e9es, selon de nombreux proverbes et idiotismes ?", "choix": [["Il mange", false], ["Il court", false], ["Il boit", false], ["Il dort", true]]}, {"titre": "Dans quel endroit du globe le chat reste-t-il synonyme de chance ou de long\u00e9vit\u00e9 ?", "choix": [["Afrique", false], ["Asie", true], ["Europe", false], ["Australie", false]]}, {"titre": "Combien le chat poss\u00e8de-t-il de doigts aux pattes ant\u00e9rieures ?", "choix": [["Six", false], ["Quatre", false], ["Cinq", true], ["Trois", false]]}, {"titre": "Quel est le cri du chat, pourtant tr\u00e8s peu utilis\u00e9 lorsque des chats communiquent entre eux ?", "choix": [["Le beuglement", false], ["Le jappement", false], ["Le miaulement", true], ["Le b\u00ealement", false]]}, {"titre": "Lequel de ces chats est le seul \u00e0 avoir des poils longs ?", "choix": [["Chartreux", false], ["Angora", true], ["Abyssin", false], ["Siamois", false]]}, {"titre": "De quelle famille de carnivores f\u00e9liformes le chat fait-il partie ?", "choix": [["Les canid\u00e9s", false], ["Les hominid\u00e9s", false], ["Les f\u00e9lid\u00e9s", true], ["Les must\u00e9lid\u00e9s", false]]}, {"titre": "Quelle manifestation sonore du chat aurait un effet relaxant sur l'homme ?", "choix": [["Meuglement", false], ["Roucoulement", false], ["Ronronnement", true], ["Bourdonnement", false]]}, {"titre": "Le chat, qui poss\u00e8de une m\u00e2choire et une denture de chasseur, est un mammif\u00e8re...", "choix": [["Insectivore", false], ["Omnivore", false], ["Carnivore", true], ["Frugivore", false]]}, {"titre": "Comment appelle-t-on les longs poils pr\u00e9sents sur les moustaches du chat ?", "choix": [["Les barbules", false], ["Les br\u00e9chets", false], ["Les tectrices", false], ["Les vibrisses", true]]}, {"titre": "Combien p\u00e8se environ un chaton \u00e0 la naissance, soumis \u00e0 un \u00e9levage communautaire ?", "choix": [["700 g", false], ["100 g", true], ["300 g", false], ["500 g", false]]}, {"titre": "Bien que n'\u00e9tant pas un coureur de fond, quelle vitesse maximale peut atteindre un chat ?", "choix": [["70 Km/h", false], ["50 Km/h", true], ["110 Km/h", false], ["90 Km/h", false]]}, {"titre": "Combien de temps une chatte garde-t-elle environ les petits dans son ventre ?", "choix": [["Neuf jours", false], ["Neuf minutes", false], ["Neuf semaines", true], ["Neuf mois", false]]}, {"titre": "Combien de races diff\u00e9rentes de chats sont reconnues par les instances de certification ?", "choix": [["50", true], ["80", false], ["110", false], ["140", false]]}, {"titre": "De combien d'os est compos\u00e9 le squelette du chat, \u00e0 la fois axial et appendiculaire ?", "choix": [["160", false], ["250", true], ["220", false], ["190", false]]}, {"titre": "Combien de temps un chat mettra-t-il au minimum pour parcourir cent m\u00e8tres ?", "choix": [["9 secondes", true], ["18 secondes", false], ["15 secondes", false], ["12 secondes", false]]}, {"titre": "Quel est en moyenne le nombre de lap\u00e9es par seconde pour le chat ?", "choix": [["Quatre", true], ["Deux", false], ["Cinq", false], ["Trois", false]]}, {"titre": "Quel chat est le seul \u00e0 \u00eatre caract\u00e9ris\u00e9 par la quasi-absence de sa fourrure ?", "choix": [["Le siamois", false], ["Le sphynx", true], ["Le persan", false], ["Le maine coon", false]]}, {"titre": "Combien le chat a-t-il de griffes, sujettes \u00e0 une pousse continue suite \u00e0 une usure naturelle ?", "choix": [["16", false], ["18", true], ["22", false], ["20", false]]}], "difficulte": "confirm\u00e9"}""")
Questionnaire(json_questionnaire).lancer()

