[README.md](./README.md)

# Unit Tests Practice

#### This repository has been prepared to practice the `unittest` automated testing framework
#### It is based on the use of simple quizzes importer and viewer.

---

## questionnaire_import.py
>python ./questionnaire_import.py 

Loads some quizzes from a sample list in the program and converts them into a specific [json format](./questionnaire.md#expected-json-schema) before to save them 
into the [json_questionnaires](./json_questionnaires) folder

More info : [questionnaire_import.md](./questionnaire_import.md)

---

## questionnaire.py
>python ./questionnaire.py <questionnaire.json>

Displays the quiz in argument and counts the number of good answers

More info : [questionnaire.md](./questionnaire.md)

---

## questionnaire_unit_tests.py
>python ./questionnaire_unit_tests.py

Uses the `unittest` automated framework but not only to test questionnaire.py

More info : [questionnaire_unit_test.md](./questionnaire_unit_test.md)

Uses the files: 
- json_00_empty.json
- json_00_without_extension
- json_01_good_format.json
- json_01_another_good_format.json
- pytest.ini

and files into [json_test_files](./json_test_files) folder

---

## [Requirements](./Requirements)
jsonschema==4.17.0
parameterized==0.8.1
requests==2.28.1
validators==0.20.0

