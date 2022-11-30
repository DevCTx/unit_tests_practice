# Questionnaire_import.py

These quizzes were uploaded from http://www.openquizzdb.org/ or https://www.kiwime.com/oqdb/files/

The API that allowed them to be uploaded for free has been disconnected and is no longer available. Some quizzes have 
thus been transferred to www.codeavecjonathan.com to simulate a download and be manipulated through this exercise


### Initial json quizz format :
```json
{
    "fournisseur" : "OpenQuizzDB - Fournisseur de contenu libre (https://www.openquizzdb.org)"
    "rédacteur" : "Phillippe  Bresoux"
    "difficulté" : "3/5"
    "version" : 1
    "mise-à-jour" : 2022-04-29
    "catégorie-nom-slogan" :
    {
        "fr" :{
                "catégorie" : "Animaux"
                "nom" : "Nos amis les chats"
                "slogan" : "Adoptez un nouveau compagnon"
            }
        "en":{}
        "es":{}
        "it" : {}
        "de" : {}
        "nl" : {}
    }
    "quizz" :
    {
        "fr" :
        {
            "débutant" : [10 items
                0 : {
                    "id": 1,
                    "question": "À quelle classe d'animaux vertébrés appartient le chat ?",
                    "propositions": [
                        "Mammifères",
                        "Reptiles",
                        "Oiseaux",
                        "Poissons"
                    ],
                    "réponse": "Mammifères",
                    "anecdote": "De nombreux mammifères élevés par l'homme jusqu'au XIXème siècle ..."
                    }
                1: {}
                ...
                10: {}
            "confirmé" : [10 items]
            "expert" : [10 items]
        }
    }
}
```
Each json quiz has 3 categories of difficulty [```débutant```, ```confirmé``` or ```expert```] 
(beginner, advanced or expert)

Each category comprises 10 questions with 4 possible answers to be proposed to the user.

The good answer is saved under ```réponse``` 
___

> questionnaire_import.py

loads json quiz files and converts them to a new format by creating one file per difficulty category

### json quizz format after import :
```json
{
  categorie : "Animaux"
  titre : "Les chats"
  questions: [ 20 items 
    0:{
        titre: "À quelle classe d'animaux vertébrés appartient le chat ?"
        choix:[
          0:["Mammifères",true]
          1:["Reptiles",false]
          2:["Oiseaux";false]
          3:["Poissons",false]
        ]
    }
    1:{}
    ...
    20:{}
  ]
  difficulte : confirmé
}
```
This file represents the second ```confirmé``` difficulty and therefore contains the first 20 questions
The ```débutant``` quiz contains only the first 10 questions and the ```expert``` quiz contains all the questions

The only rubrics kept are: ```catégorie```, ```nom```, of ```catégorie-nom-slogan``` in French (fr) and the items of the
```quizz``` in French(fr). These last ones are compiled to have 4 propositions and a boolean parameter indicating if the
answer is the good one. 

---
### The schema must so match with the one tested in ./questionnaire.py
```json
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
                            "items": False
                        }
                    }
                }
            }
        },
        "difficulte": {"type": "string"}
    }
}
```

