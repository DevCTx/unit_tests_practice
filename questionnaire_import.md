[README.md](./README.md) > [questionnaire_import.md](./questionnaire_import.md)

# Questionnaire_import.py

Loads some quizzes from a sample list in the program :
* openquizzdb_50.json
* openquizzdb_86.json
* openquizzdb_241.json
* openquizzdb_90.json

and converts them into a specific json [format](./questionnaire.md#expected-json-schema) before to save them 
into the [json_questionnaires](./json_questionnaires) folder

Those quizzes were initially downloaded from http://www.openquizzdb.org/ or https://www.kiwime.com/oqdb/files/ but the 
API that allowed to do it for free has been disconnected and is no longer available. Those quizzes have 
thus been transferred on www.codeavecjonathan.com to be manipulated through this exercise


### Sample of the initial json quiz format :
```json
{
    "fournisseur" : "OpenQuizzDB - Fournisseur de contenu libre (https://www.openquizzdb.org)",
    "rédacteur" : "Phillippe  Bresoux",
    "difficulté" : "3/5",
    "version" : 1,
    "mise-à-jour" : "2022-04-29",
    "catégorie-nom-slogan" :
    {
        "fr" :{
                "catégorie" : "Animaux"
                "nom" : "Nos amis les chats"
                "slogan" : "Adoptez un nouveau compagnon"
            },
        "en":{},
        "es":{},
        "it":{},
        "de":{},
        "nl":{},
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
                        "Poissons",
                    ],
                    "réponse": "Mammifères",
                    "anecdote": "De nombreux mammifères élevés par l'homme jusqu'au XIXème siècle ...",
                    },
                1: {},
                ...
                10: {}
            ],
            "confirmé" : [10 items],
            "expert" : [10 items],
        },
        "en":{},
        "es":{},
        "it":{},
        "de":{},
        "nl":{},
    }
}
```
Each json quiz has 3 categories of difficulty [```débutant```, ```confirmé``` or ```expert```] 
(beginner, advanced or expert)

Each category comprises 10 questions with 4 possible answers to be proposed to the user.

The good answer is saved under ```réponse``` 
___

> python questionnaire_import.py

loads json quiz files and converts them to a new json format by creating one file per difficulty category

### Sample of the json quizz format after import :
```json
{
  "categorie" : "Animaux",
  "titre" : "Les chats",
  "questions": [ 20 items 
    0:{
        "titre": "À quelle classe d'animaux vertébrés appartient le chat ?"
        "choix":[
          ["Mammifères",true],
          ["Reptiles",false],
          ["Oiseaux",false],
          ["Poissons",false]
        ]
    },
    1:{},
    ...
    20:{}
  ]
  "difficulte" : "confirmé"
}
```
This file represents the second ```confirmé``` difficulty and therefore contains the first 20 questions
The ```débutant``` quiz contains only the first 10 questions and the ```expert``` quiz contains the whole 30 questions

The only keys kept are: ```catégorie```, ```nom```, of ```catégorie-nom-slogan``` in French (```fr```) and the items of
the ```quizz``` in French(```fr```). These last ones are compiled to have 4 propositions and a boolean parameter 
indicating if the answer is the good one. 

---
### The schema must so match with the one tested in [./questionnaire.py](./questionnaire.md#expected-json-schema)
