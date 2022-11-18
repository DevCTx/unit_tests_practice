import json

import jsonschema
from jsonschema.validators import validate


def validate_json_syntax(d):
    try:
        return json.loads(d)
    except ValueError:
        print('DEBUG: JSON data contains an error')
        return None


schema = {
    "$schema": "json_questionnaire",
    "$id": "https://openquizzdb.org/",
    "type": "object",
    "required": ["titre","questions"],
    "properties": {
        "categorie": {"type": "string"},
        "titre": {"type": "string"},
        "questions": {
            "type": "array",
            "default": [],
            "items": {
                "type": "object",
                "required": ["titre","choix"],
                "properties": {
                    "titre": {"type": "string"},
                    "choix": {
                        "type": "array",
                        "default": [],
                        "minItems": 2,
                        "items": {
                            "type": "array",
                            "default": [
                                    {"type": "string"},
                                    {"type": "boolean"}]
                        }
                    }
                }
            }

        },
        "difficulte": {"type": "string"}
    }
}

# will return false because JSON not valid
# missing quotes around lastName
data = '{"categorie": "Animaux", "titre": "Les chats", "questions": [{"titre": "\u00c0 quelle classe d animaux vert\u00e9br\u00e9s regroupant pr\u00e8s de 5.400 esp\u00e8ces appartient le chat ?", "choix": [["Mammif\u00e8res", true], ["Reptiles", false], ["Oiseaux", false], ["Poissons", false]]}, {"titre": "Lorsque vous apercevez votre chat faire le gros dos, il est probablement...", "choix": [["En chasse", false], ["Content", false], ["Malade", false], ["Effray\u00e9", true]]}, {"titre": "Que fait principalement le chat de ses journ\u00e9es, selon de nombreux proverbes et idiotismes ?", "choix": [["Il mange", false], ["Il court", false], ["Il boit", false], ["Il dort", true]]}, {"titre": "Dans quel endroit du globe le chat reste-t-il synonyme de chance ou de long\u00e9vit\u00e9 ?", "choix": [["Afrique", false], ["Asie", true], ["Europe", false], ["Australie", false]]}, {"titre": "Combien le chat poss\u00e8de-t-il de doigts aux pattes ant\u00e9rieures ?", "choix": [["Six", false], ["Quatre", false], ["Cinq", true], ["Trois", false]]}, {"titre": "Quel est le cri du chat, pourtant tr\u00e8s peu utilis\u00e9 lorsque des chats communiquent entre eux ?", "choix": [["Le beuglement", false], ["Le jappement", false], ["Le miaulement", true], ["Le b\u00ealement", false]]}, {"titre": "Lequel de ces chats est le seul \u00e0 avoir des poils longs ?", "choix": [["Chartreux", false], ["Angora", true], ["Abyssin", false], ["Siamois", false]]}, {"titre": "De quelle famille de carnivores f\u00e9liformes le chat fait-il partie ?", "choix": [["Les canid\u00e9s", false], ["Les hominid\u00e9s", false], ["Les f\u00e9lid\u00e9s", true], ["Les must\u00e9lid\u00e9s", false]]}, {"titre": "Quelle manifestation sonore du chat aurait un effet relaxant sur l homme ?", "choix": [["Meuglement", false], ["Roucoulement", false], ["Ronronnement", true], ["Bourdonnement", false]]}, {"titre": "Le chat, qui poss\u00e8de une m\u00e2choire et une denture de chasseur, est un mammif\u00e8re...", "choix": [["Insectivore", false], ["Omnivore", false], ["Carnivore", true], ["Frugivore", false]]}, {"titre": "Comment appelle-t-on les longs poils pr\u00e9sents sur les moustaches du chat ?", "choix": [["Les barbules", false], ["Les br\u00e9chets", false], ["Les tectrices", false], ["Les vibrisses", true]]}, {"titre": "Combien p\u00e8se environ un chaton \u00e0 la naissance, soumis \u00e0 un \u00e9levage communautaire ?", "choix": [["700 g", false], ["100 g", true], ["300 g", false], ["500 g", false]]}, {"titre": "Bien que n \u00e9tant pas un coureur de fond, quelle vitesse maximale peut atteindre un chat ?", "choix": [["70 Km/h", false], ["50 Km/h", true], ["110 Km/h", false], ["90 Km/h", false]]}, {"titre": "Combien de temps une chatte garde-t-elle environ les petits dans son ventre ?", "choix": [["Neuf jours", false], ["Neuf minutes", false], ["Neuf semaines", true], ["Neuf mois", false]]}, {"titre": "Combien de races diff\u00e9rentes de chats sont reconnues par les instances de certification ?", "choix": [["50", true], ["80", false], ["110", false], ["140", false]]}, {"titre": "De combien d os est compos\u00e9 le squelette du chat, \u00e0 la fois axial et appendiculaire ?", "choix": [["160", false], ["250", true], ["220", false], ["190", false]]}, {"titre": "Combien de temps un chat mettra-t-il au minimum pour parcourir cent m\u00e8tres ?", "choix": [["9 secondes", true], ["18 secondes", false], ["15 secondes", false], ["12 secondes", false]]}, {"titre": "Quel est en moyenne le nombre de lap\u00e9es par seconde pour le chat ?", "choix": [["Quatre", true], ["Deux", false], ["Cinq", false], ["Trois", false]]}, {"titre": "Quel chat est le seul \u00e0 \u00eatre caract\u00e9ris\u00e9 par la quasi-absence de sa fourrure ?", "choix": [["Le siamois", false], ["Le sphynx", true], ["Le persan", false], ["Le maine coon", false]]}, {"titre": "Combien le chat a-t-il de griffes, sujettes \u00e0 une pousse continue suite \u00e0 une usure naturelle ?", "choix": [["16", false], ["18", true], ["22", false], ["20", false]]}], "difficulte": "confirm\u00e9"}'
json_data = validate_json_syntax(data)
if json_data:
    #output will be None
    try:
        validate(json_data, schema)
    except jsonschema.exceptions.ValidationError:
        print("Schema JSON incorrect")

