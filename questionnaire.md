[README.md](./README.md) > [questionnaire.md](./questionnaire.md)

# Questionnaire.py

Displays the quiz in argument and counts the number of good answers

```commandline
python questionnaire.py <questionnaire.json>
```

## Sample :

```commandline
python questionnaire.py .\json_questionnaires\animaux_leschats_confirme.json
```
```commandline
=== QUESTIONNAIRE ===
Catégorie : Animaux
Difficulté : confirmé
Titre : Les Chats

QUESTION 1/20
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
- [`Error in argument`] if __no one or more than one argument is passed__
- [`Incorrect extension`] if __the file as no json extension__ 
- [`Invalid permissions or path`] if __the path to the file can not be reached__  
- [`Invalid permissions or path`] if __the system has not the permission to open the file__  
- [`Invalid URL`] if __the path to the server can not be reached__  
- [`File not found`] if __the file can not be reached on the distant server__
- [`Incompatible or no data in JSON file`] if __the json file cannot be loaded and decoded__
- [`Incompatible Json schema`] if __the loaded json file does not match the expected schema__
- [`The title of the quizz is missing and mandatory`] if __the `titre` property is an empty string__
- [`The questions of the quizz are missing and mandatory`] if __the `questions` property is an empty array__

These warnings may also be printed but are __not critical__ to use the quiz
- [`Skipped question : question is empty`] if __the `titre` property of a question is an empty string__
- [`Skipped answer : answer is empty`] if __the first parameter of a `choix` in a question is an empty string__
- [`Skipped question : no one or more than one good answers`] if a question has no one or more than one `boolean` 
at `true` in the possible answers of a single question

At least, if all questions have been skipped, [`Désolé, aucune question n'est compatible avec ce quizz`] will be printed.

---
## Expected Json Schema

```categorie``` and ```difficulte``` properties are not required but ```titre``` and ```questions``` are mandatory


Each question must have at least 2 possible answers and each answer must be defined by a ```string``` and 
a ```boolean``` only


```json lines
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
                                "prefixItems": [
                                  {"type": "string"}, 
                                  {"type": "boolean"}
                                ],
                                "items": False
                            }
                        }
                    }
                }
            },
            "difficulte": {"type": "string"}
        }
    }
}
```
Note : The `json-schema.org/draft/2020-12/` allows the `prefixItems` property to specify the types of the first 
items into this part and accepts to define `items` at false to mean that nothing more than the prefix items can be 
added into this part. This is however not supported by `json-schema.org/draft/2019-09/` used by a lot of json 
validator online.

Therefore, it is necessary to specify `[]` in place of `False` into the last `items` property to test
the json files into json validator using `json-schema.org/draft/2019-09/`. The type of prefixItems can unfortunatly be 
verified by the schema with `json-schema.org/draft/2020-12/` only.

Sample : https://www.jsonschemavalidator.net/s/fhyE6WC0


[README.md](./README.md) > [questionnaire.md](./questionnaire.md)