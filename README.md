[README.md](./README.md)

# Unit Tests Practice

#### This repository has been prepared to practice the 'unittest' automated testing framework through different angles
#### It is based on the use of simple quizzes importer and viewer.

---

>python ./questionnaire_import.py 

Loads some quizzes from a sample list in the program and converts them into a specific json [format](./questionnaire.md#expected-json-schema) before to save them 
into the [json_questionnaires](./json_questionnaires) folder

More info : [questionnaire_import.md](./questionnaire_import.md)

---

>python ./questionnaire.py <questionnaire.json>

Displays the quizz in argument and counts the number of good answers

More info : [questionnaire.md](./questionnaire.md)

---


