[README.md](./README.md)

# Unit Tests Practice

#### This repository has been prepared to practice the `unittest` automated testing framework through different angles
#### It is based on the use of simple quizzes importer and viewer.

---

## questionnaire_import.py
>python ./questionnaire_import.py 

Loads some quizzes from a sample list in the program and converts them into a specific json [format](./questionnaire.md#expected-json-schema) before to save them 
into the [json_questionnaires](./json_questionnaires) folder

More info : [questionnaire_import.md](./questionnaire_import.md)

---

## questionnaire.py
>python ./questionnaire.py <questionnaire.json>

Displays the quizz in argument and counts the number of good answers

More info : [questionnaire.md](./questionnaire.md)

---

## questionnaire_unit_tests.py
>python ./questionnaire_unit_tests.py

Uses the `unittest` automated framework but not only to test questionnaire.py

More info : [questionnaire_unit_test.md](./questionnaire_unit_test.md)

Uses : 
- initial_json_test_file.json
- second_json_test_file.json
- json_file_without_extension
- empty.json

and files into [json_test_files](./json_test_files) folder

---


