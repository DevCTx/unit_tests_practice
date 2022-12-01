[README.md](./README.md) > [questionnaire.md](./questionnaire.md)

# Questionnaire.py

Displays the quizz in argument and counts the number of good answers

```commandline
python questionnaire.py <questionnaire.json>
```

## Sample :

```commandline
python questionnaire.py .\json_questionnaires\animaux_leschats_confirme.json
```
```commandline
Catégorie : Animaux
Difficulté : confirmé
Titre : Les chats

QUESTION 1
  À quelle classe d'animaux vertébrés regroupant près de 5.400 espèces appartient le chat ?
   1 - Mammifères
   2 - Reptiles
   3 - Oiseaux
   4 - Poissons
Votre réponse (entre 1 et 4) :
```
```commandline
Bonne réponse

Score final : 14 sur 20
```
---

Questionnaire.py can accept a json file from :
* the current folder 
* a different folder
* an URL

Questionnaire.py tries to load the json file in argument or print :
- [```Error in argument```] if no one or more than one argument is passed
- [```Incorrect extension```] if the file as no json extension 
- [```Invalid Path```] if the path to the file can not be reached  
- [```No File```] if the file can not be find into the path folder 
- [```Invalid URL```] if the path to the server can not be reached  
- [```File not found```] if the file can not be reached on the distant server
- [```Incompatible or no data in JSON file```] if the json file cannot be loaded and decoded
- [```Incompatible Json schema```] if the loaded json file does not match the 
expected [schema](./questionnaire.md#expected-json-schema)
- [```The title of the quizz is missing```] if the titre is an empty string

These messages may also be printed but are <u>not critical</u> to the quiz
- [```Skipped question : nothing to ask in question```] if the question is an empty string
- [```Skipped question : no one or more than one good answer in question```] if a question has no one or more than 
one ```boolean```  at ```True``` in its answers

At least, if all questions have been skipped, [```No compatible question in this quizz```] will be printed.

---
## Expected Json Schema

```categorie``` and ```difficulte``` properties are not required but ```titre``` and ```questions``` are mandatory


Each questions must have at least 2 possible answers and each answers must be defined by a ```string``` and 
a ```boolean``` only


```json lines
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
                            "prefixItems": [
                                {"type": "string"}, 
                                {"type": "boolean"}
                            ],
                            "items": false
                        }
                    }
                }
            }
        },
        "difficulte": {"type": "string"}
    }
}
```

