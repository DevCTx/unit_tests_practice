[README.md](./README.md) > [questionnaire_unit_test.md](./questionnaire_unit_test.md)

# Questionnaire_unit_tests.py 

Uses the 'unittest' automated framework but not only to test questionnaire.py

```commandline
python ./questionnaire_unit_tests.py
```
Note : All tests are described following the format :\
`test number`->`returned values` if receives __argument(s)__ then prints `message`

---
### Level 1 : Basic Unit tests about the arguments received by questionnaire.py

the argument are read and handled by the `load_json_argv` function which should return the json data `<Json_Data>`
and the file path `<File_Path>`
`
 
- `test_01` -> `<Json_Data>, <File_Path>` if receives __a good json file__ then prints no message

- `test_02` -> `None, None` if receives __no file__ then prints the message :\
```Error : Error in argument, should add a single .json questionnaire```

- `test_03` -> `None, None` if receives __more than one file__ then prints the message :\
```Error : Error in argument, should add a single .json questionnaire```

- `test_04` -> `None, <File_Path>` if receives __a file without json extension__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire```

- `test_05` -> `None, <File_Path>` if receives __a non-existent file__ then prints the message :\
```Error : Invalid permissions or path to non-existent-file.json```

- `test_06` -> `None, <File_Path>` if receives __an empty json file__ then prints the message :\
```Error : Incompatible or no data in JSON file empty.json```

---
### Level 2 : Same tests but with a different name of program
If the name of the questionnaire.py change, the error messages should adapt.\
The class test is derived from the level 1 but simulates a program named `test.py`

---
### Level 3 : Same tests but with a file into a folder

The class derives from the level 1 and executes the same tests except that 
a [json_test_files](./json_test_files) folder is added to the path of the file given in argument

The printed message of test 2 is quite different from the Level 1 since the file path is given in argument.
- `test_02` -> `None, <File_Path>` if receives __no file__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire.```

---
### Level 4 : Same tests but with another name and a file into a folder 

The class derives from the level 2 and 3 and executes the same tests under `test.py` name and with files 
from [json_test_files](./json_test_files)

The printed message of test 2 is so quite different from the Level 1 as well.
- `test_02` -> `None, <File_Path>` if receives __no file__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire.```

---
### Level 5 : Tests with data online 

A free json file is available at the url : https://countwordsfree.com/example.json

- `test_01` -> `<Json_Data>, <File_Path>` if receives __a valid json file on a valid url path__ then prints no message.


- `test_02` -> `None, <File_Path>` if receives __a invalid json file on a valid url path__ then prints the message :\
```Error : File not found at URL https://countwordsfree.com/non-existant.json```


- `test_03` -> `None, <File_Path>` if receives __a valid json file but on a invalid url path__ then prints the message :\
```Error : Invalid URL at https://countwordsfre.com/example.json```


- `test_04` -> `None, <File_Path>` if receives __a file without json extension on a valid url path__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire.```

---
### Level 6 : Tests with data on http://localhost 

To go further and test wrong or empty json files, it is necessary to simulate a simple HTTP server 
via localhost(`http://127.0.0.1`) for example.

The simple HTTP server is started through a thread by the `setUp` method and close by the `tearDown` method.\
Those 2 `unittest.TestCase` methods are respectively called before and after each test of the class and can be overwritten.

The class derives from the level 1 and therefore executes the same tests but through an HTTP connection.

- `test_01` -> `<Json_Data>, <File_Path>` if receives __a good json file__ then prints no message.


The printed message of test 2 is quite different from the Level 1 since the URL is given in argument.
- `test_02` -> `None, <File_Path>` if receives __no file__ then prints a message \
```Error : Incorrect extension, add a .json questionnaire```

Idem for test 5 and 6 because the argument given here is a URL and not a file.

- `test_05` -> `None, File_Path` if receives __a non-existent file__ then prints the message :\
```Error : File not found at URL <URL>```


- `test_06` -> `None, File_Path` if receives __an empty json file__ then prints the message :\
```Error : Incompatible or no data in JSON file at URL <URL>```


---
### Level 7 : Optimized Level 6 with pytest  

Rather than opening and closing an HTTP server for each test, it would be better to open and close it once for all tests
in the class.

This can be done by creating a fixture defined on the `class` scope and using the option `autouse=True` to automatically
applied it to all the tests of the parent class.

The fixture opens the server, before all the tests run, and closes the server when it will be called a second time after
all tests ran.
```commandline
HTTP Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
...
<tests>
...
HTTP Disconnection from http://127.0.0.1:8000/
```
Note : According to the fixture used in this test, this class will be executed only using `pytest` and will be skipped 
using `unittests`
```commandline
pytest -v -k questionnaire_unit_test.py -s
```

---
### Level 8 : Optimized Level 6 with unittests built-in `@classmethod` tag

In the same idea as Level 7 with fixtures, it is possible to call the built-in methods `setUpClass` and `tearDownClass` 
at the beginning and at the end of the tests of the class. To do this, the `self` argument must be modified to `cls` 
because these built-in functions are private to the unittest class, and the built-in `@classmethod` tag must be added
over the class in order to force the access to them.

---
### Level 9 : Tests with a patch on network requests

Finally, unit tests should be isolated and not depend on the system or the network in order to be able, for example, to measure 
exactly the time needed to proceed without a external dependency.

It should so better to simulate the answers of the network requests like ``Success (200)`` 
or ``File Not Found (404)`` for example, to get the best knowledge of the program behavior.

This may require to rewrite the tests because the reading of the file from URL must also be simulated, like in this 2 
tests trying to read files from a non-existent Web URL.

- `test_01` -> `None, File_Path` if receives __a json file on a non-existent Web URL with a simulated
``File Not Found (404)`` answer to the network request__ then prints the message :
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/initial_json_test_file.json
```
- `test_02` -> `Json_Data, File_Path` if receives __a json file on a non-existent Web URL with a simulated 
``Success (200)`` answer to the network request__ then prints no message.
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> Json_Data, File_Path
```
In that case, the property `status_code` of the response must be updated to the code `200 (OK)` and the property `text`
of the response must contain the read json data. This is simulated by the reading of a local file from the given path 
without the server part like ``./initial_json_test_file.json`` in this example.

---
### Level 10 : Json Tests

These tests are prepared to know if a `Questionnaire` instance is created or not according to the json file received in 
argument. 

If all the conditions of the [expected json format](./questionnaire.md#expected-json-schema) is respected, the `__new__`
method creates an instance of `Questionnaire` and the `__init__` method initializes it, else `__new__` returns `None`.

All json file tested should be a valid json file or the message following will be printed :\
```--> Wrong arguments, should be test on load_json_argv```

For example :
- `test_00` -> `None` if receives __empty file__ then prints the message :\
```Error : Incompatible or no data in JSON file <file>``` then\
```--> Wrong arguments, should be test on load_json_argv```

The next tests returns a `Questionnaire instance` to be handled by the `run` function and prints no message
- `test_01` -> `Questionnaire` if receives __a good format file__ 
- `test_02` -> `Questionnaire` if receives __a file without not mandatory category__ 
- `test_03` -> `Questionnaire` if receives __a file with empty not mandatory category__ 
- `test_04` -> `Questionnaire` if receives __a file without not mandatory difficulty__ 
- `test_05` -> `Questionnaire` if receives __a file with empty not mandatory difficulty__ 
- `test_10` -> `Questionnaire` if receives __a file with more keys__ 

According to the [expected json format](./questionnaire.md#expected-json-schema), the properties `categorie` and 
`difficulté` are not required, so they will be saved as unknown (`inconnue`) if they are non-existent or empty
and won't disturb the good behavior of the application.

If the json file does not respect the [expected json format](./questionnaire.md#expected-json-schema), the message\
`Error : Incompatible Json schema in file <file>` will be printed, like for the following tests :
- `test_06` -> `None` if receives __a file without mandatory title__ 
- `test_08` -> `None` if receives __a file without mandatory questions__ 
- `test_11` -> `None` if receives __a file without title in questions__ 
- `test_13` -> `None` if receives __a file without choice in questions__ 
- `test_14` -> `None` if receives __a file with a empty choice array in questions__ 
- `test_15` -> `None` if receives __a file with only one choice in questions__ 
- `test_16` -> `None` if receives __a file without answer in choices in questions__ 
- `test_19` -> `None` if receives __a file without boolean indicator specifying a right or wrong answer__ 
- `test_20` -> `None` if receives __a file with an integer in place of the boolean__ 
- `test_23` -> `None` if receives __a file with an empty array in choices in questions__ 

Then, if the title or questions are missing, the `__ini__` function will also answer `None`

- `test_07` -> `None` if receives __a file with empty title__ and prints the message:\
```Error : The title of the quizz is missing and mandatory in file <file>```


- `test_09` -> `None` if receives __a file with an empty array in choices in questions__ and prints the message :\
```Error : The questions of the quizz are missing and mandatory in file <file>```


Next, the `__init__` function will initialize the `Questionnaire` instance but may skip some incompatible parts of 
the quiz if they are empty, or if there is no answer or more than one answer in a question, and will print one or more 
warning messages depending on the number of cases encountered.

- `test_12` -> `Questionnaire` if receives __a file with an empty title in a question__ , skip the question, and prints:\
```Warning : Skipped question : question is empty in question <number> file <file>```


- `test_17` -> `Questionnaire` if receives __a file with an empty wrong answer in choices in questions__ , skip the 
question, and prints:\
```Warning : Skipped answer : answer is empty in question <number> file <file>```


- `test_18` -> `Questionnaire` if receives __a file with an empty good answer in choices in questions__ , skip the 
answer and the question if there is no more good answer, and prints:\
```Warning : Skipped answer : answer is empty in question <number> file <file>```\
```Warning : Skipped question : no one or more than one good answers in question <number> file <file>```


- `test_21` -> `Questionnaire` if receives __a file without good answer in choices in questions__ , skip the question,
and prints:\
```Warning : Skipped question : no one or more than one good answers in question <number> file <file>```


- `test_22` -> `Questionnaire` if receives __a file with more than one good answer in choices in questions__ ,
skip the question, and prints:\
```Warning : Skipped question : no one or more than one good answers in question <number> file <file>```


Finally, the `__init__` function will initialize the `Questionnaire` instance but the `run` function will 
skip the whole quizz if there is no compatible question in with the `questionnaire.py` application and 
will print the following message to the user : \
```Désolé, aucune questions n'est compatible avec ce quizz``` 

- `test_24` -> `Questionnaire` if receives __a file with questions without good answer only__ ,
skip all the questions, and prints:\
```Warning : Skipped question : no one or more than one good answers in question <number> file <file>```\
```Warning : Skipped question : no one or more than one good answers in question <number> file <file>```

---
### More Unit Tests and Documentations

More information and independent tests about marks, fixtures, patch, local server in thread, json schema, pytest.ini or
conftest.py files, etc ... are available in [more_unit_tests_docs](./more_unit_test_docs) folder.

Thank you for reading.

---
### Final results with unittests

```commandline 
python .\questionnaire_unit_test.py                        

questionnaire.py json_01_good_format.json -> Json_Data, File_Path
.
questionnaire.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
.
questionnaire.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
.
test.py json_01_good_format.json -> Json_Data, File_Path
.
test.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
.
test.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
.
questionnaire.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
.
questionnaire.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
.
questionnaire.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
.
test.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
.
test.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
.
test.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
.
questionnaire.py https://countwordsfree.com/example.json -> Json_Data, File_Path
.
questionnaire.py https://countwordsfree.com/non-existant.json -> None, File_Path
Error : File not found at URL https://countwordsfree.com/non-existant.json
.
questionnaire.py https://countwordsfre.com/example.json -> None, File_Path
Error : Invalid URL at https://countwordsfre.com/example.json
.
questionnaire.py https://countwordsfree.com/empty_or_uncompleted_file -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
Connection to http://127.0.0.1:8000/ in Thread-1 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:38] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-3 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json http://127.0.0.1:8000/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-5 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-6 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:40] code 404, message File not found
127.0.0.1 - - [07/Dec/2022 15:07:40] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-8 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:40] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
Disconnection from http://127.0.0.1:8000/
.
Connection to http://127.0.0.1:8000/ in Thread-10 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:41] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
.
questionnaire.py http://127.0.0.1:8000/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json http://127.0.0.1:8000/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:41] code 404, message File not found
127.0.0.1 - - [07/Dec/2022 15:07:41] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
.
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:07:41] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
.
Disconnection from http://127.0.0.1:8000/

questionnaire.py http://non-existent-url.com/json_01_good_format.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/json_01_good_format.json
.
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> Json_Data, File_Path
.
Questionnaire( <json data>, json_test_files\json_00_empty.json ) --> None
Error : Incompatible or no data in JSON file json_test_files\json_00_empty.json
--> Wrong arguments, should be test on load_json_argv
.
Questionnaire( <json data>, json_test_files\json_01_good_format.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_02_without_category.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_03_with_empty_category.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_04_without_difficulty.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_05_with_empty_difficulty.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_06_without_title.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_06_without_title.json
.
Questionnaire( <json data>, json_test_files\json_07_with_empty_title.json ) --> None
Error : The title of the quizz is missing and mandatory in file json_test_files\json_07_with_empty_title.json
.
Questionnaire( <json data>, json_test_files\json_08_without_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_08_without_questions.json
.
Questionnaire( <json data>, json_test_files\json_09_with_empty_questions.json ) --> None
Error : The questions of the quizz are missing and mandatory in file json_test_files\json_09_with_empty_questions.json
.
Questionnaire( <json data>, json_test_files\json_10_with_more_keys.json ) --> Questionnaire
.
Questionnaire( <json data>, json_test_files\json_11_without_title_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_11_without_title_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_12_with_empty_title_in_questions.json ) --> Questionnaire
Warning : Skipped question : question is empty in question 1 file json_test_files\json_12_with_empty_title_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_13_without_choice_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_13_without_choice_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_14_with_empty_choice_array_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_14_with_empty_choice_array_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_15_with_only_one_choice_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_15_with_only_one_choice_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_16_without_answer_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_16_without_answer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_17_with_empty_wrong_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped answer : answer is empty in question 1 file json_test_files\json_17_with_empty_wrong_answer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped answer : answer is empty in question 1 file json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_19_without_boolean_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_19_without_boolean_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_20_with_integer_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_20_with_integer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_21_without_no_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_21_without_no_good_answer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_22_with_more_than_one_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_22_with_more_than_one_good_answer_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_23_with_an_empty_array_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_23_with_an_empty_array_in_choices_in_questions.json
.
Questionnaire( <json data>, json_test_files\json_24_with_questions_without_good_answer_only.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_24_with_questions_without_good_answer_only.json
Warning : Skipped question : no one or more than one good answers in question 2 file json_test_files\json_24_with_questions_without_good_answer_only.json
.
----------------------------------------------------------------------
Ran 73 tests in 5.675s

OK (skipped=6)
```
---
### Final results with pytest

```commandline
pytest -v -k questionnaire_unit_test.py -s
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0 -- C:\Users\cedri\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe
cachedir: .pytest_cache
rootdir: C:\MyPythonApps\unit_tests_practice, configfile: pytest.ini
collecting 6 items                                                                                                                                                                                       o
k
collected 127 items / 54 deselected / 73 selected

questionnaire_unit_test.py::_01_load_json_argv::test_01_load_json_argv_with_one_good_json_file
questionnaire.py json_01_good_format.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_02_load_json_argv_with_no_argv
questionnaire.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_06_load_json_argv_with_empty_json_file
questionnaire.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_01_load_json_argv_with_one_good_json_file
test.py json_01_good_format.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_02_load_json_argv_with_no_argv
test.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_03_load_json_argv_with_more_than_one_argv
test.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_04_load_json_argv_with_argv_without_json_extension
test.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_05_load_json_argv_with_non_existent_json_file
test.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_06_load_json_argv_with_empty_json_file
test.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_01_load_json_argv_with_one_good_json_file
questionnaire.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_02_load_json_argv_with_no_argv
questionnaire.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_06_load_json_argv_with_empty_json_file
questionnaire.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_01_load_json_argv_with_one_good_json_file
test.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_02_load_json_argv_with_no_argv
test.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_03_load_json_argv_with_more_than_one_argv
test.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_04_load_json_argv_with_argv_without_json_extension
test.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_05_load_json_argv_with_non_existent_json_file
test.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_06_load_json_argv_with_empty_json_file
test.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
PASSED

questionnaire_unit_test.py::_05_load_json_argv_with_data_online::test_01_load_json_argv_with_json_file_sample_online
questionnaire.py https://countwordsfree.com/example.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_05_load_json_argv_with_data_online::test_02_load_json_argv_with_invalid_json_file_sample_online
questionnaire.py https://countwordsfree.com/non-existant.json -> None, File_Path
Error : File not found at URL https://countwordsfree.com/non-existant.json
PASSED

questionnaire_unit_test.py::_05_load_json_argv_with_data_online::test_03_load_json_argv_with_invalid_url
questionnaire.py https://countwordsfre.com/example.json -> None, File_Path
Error : Invalid URL at https://countwordsfre.com/example.json
PASSED

questionnaire_unit_test.py::_05_load_json_argv_with_data_online::test_04_load_json_argv_with_empty_or_uncompleted_file_online
questionnaire.py https://countwordsfree.com/empty_or_uncompleted_file -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_01_load_json_argv_with_one_good_json_file
Connection to http://127.0.0.1:8000/ in Thread-1 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:54] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_02_load_json_argv_with_no_argv
Connection to http://127.0.0.1:8000/ in Thread-3 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_03_load_json_argv_with_more_than_one_argv
Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json http://127.0.0.1:8000/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_04_load_json_argv_with_argv_without_json_extension
Connection to http://127.0.0.1:8000/ in Thread-5 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_05_load_json_argv_with_non_existent_json_file
Connection to http://127.0.0.1:8000/ in Thread-6 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:56] code 404, message File not found
127.0.0.1 - - [07/Dec/2022 15:08:56] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_06_load_json_argv_with_empty_json_file
Connection to http://127.0.0.1:8000/ in Thread-8 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:57] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_01_load_json_argv_with_one_good_json_file
HTTP Connection to http://127.0.0.1:8000/ in Thread-10 (serve_forever) 
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:57] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_02_load_json_argv_with_no_argv
questionnaire.py http://127.0.0.1:8000/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json http://127.0.0.1:8000/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py http://127.0.0.1:8000/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:57] code 404, message File not found
127.0.0.1 - - [07/Dec/2022 15:08:57] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_06_load_json_argv_with_empty_json_file
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:57] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
PASSED
HTTP Disconnection from http://127.0.0.1:8000/

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_01_load_json_argv_with_one_good_json_file 
Connection to http://127.0.0.1:8000/ in Thread-14 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:58] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_02_load_json_argv_with_no_argv
questionnaire.py http://127.0.0.1:8000/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json http://127.0.0.1:8000/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py http://127.0.0.1:8000/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:58] code 404, message File not found
127.0.0.1 - - [07/Dec/2022 15:08:58] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_06_load_json_argv_with_empty_json_file
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [07/Dec/2022 15:08:58] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
PASSED
Disconnection from http://127.0.0.1:8000/

questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_01_load_json_argv_with_simulated_FileNotFound_answer 
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/json_01_good_format.json
PASSED

questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_02_load_json_argv_with_simulated_success_request_and_fake_data
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_00_Questionnaire_empty_file
Questionnaire( <json data>, json_test_files\json_00_empty.json ) --> None
Error : Incompatible or no data in JSON file json_test_files\json_00_empty.json
--> Wrong arguments, should be test on load_json_argv
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_01_Questionnaire_good_format_file
Questionnaire( <json data>, json_test_files\json_01_good_format.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_02_Questionnaire_without_not_mandatory_category
Questionnaire( <json data>, json_test_files\json_02_without_category.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_03_Questionnaire_with_empty_not_mandatory_category
Questionnaire( <json data>, json_test_files\json_03_with_empty_category.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_04_Questionnaire_without_not_mandatory_difficulty
Questionnaire( <json data>, json_test_files\json_04_without_difficulty.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_05_Questionnaire_with_empty_not_mandatory_difficulty
Questionnaire( <json data>, json_test_files\json_05_with_empty_difficulty.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_06_Questionnaire_without_mandatory_title
Questionnaire( <json data>, json_test_files\json_06_without_title.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_06_without_title.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_07_Questionnaire_with_empty_title
Questionnaire( <json data>, json_test_files\json_07_with_empty_title.json ) --> None
Error : The title of the quizz is missing and mandatory in file json_test_files\json_07_with_empty_title.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_08_Questionnaire_without_mandatory_questions
Questionnaire( <json data>, json_test_files\json_08_without_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_08_without_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_09_Questionnaire_with_empty_questions
Questionnaire( <json data>, json_test_files\json_09_with_empty_questions.json ) --> None
Error : The questions of the quizz are missing and mandatory in file json_test_files\json_09_with_empty_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_10_Questionnaire_with_more_keys
Questionnaire( <json data>, json_test_files\json_10_with_more_keys.json ) --> Questionnaire
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_11_Questionnaire_without_title_in_questions
Questionnaire( <json data>, json_test_files\json_11_without_title_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_11_without_title_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_12_Questionnaire_with_empty_title_in_questions
Questionnaire( <json data>, json_test_files\json_12_with_empty_title_in_questions.json ) --> Questionnaire
Warning : Skipped question : question is empty in question 1 file json_test_files\json_12_with_empty_title_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_13_Questionnaire_without_choice_in_questions
Questionnaire( <json data>, json_test_files\json_13_without_choice_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_13_without_choice_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_14_Questionnaire_with_empty_choice_array_in_questions
Questionnaire( <json data>, json_test_files\json_14_with_empty_choice_array_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_14_with_empty_choice_array_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_15_Questionnaire_with_only_one_choices_in_questions
Questionnaire( <json data>, json_test_files\json_15_with_only_one_choice_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_15_with_only_one_choice_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_16_Questionnaire_without_answer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_16_without_answer_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_16_without_answer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_17_Questionnaire_with_empty_wrong_answer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_17_with_empty_wrong_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped answer : answer is empty in question 1 file json_test_files\json_17_with_empty_wrong_answer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_18_Questionnaire_with_empty_good_answer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped answer : answer is empty in question 1 file json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_18_with_empty_good_answer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_19_Questionnaire_without_boolean_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_19_without_boolean_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_19_without_boolean_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_20_Questionnaire_with_integer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_20_with_integer_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_20_with_integer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_21_Questionnaire_without_no_good_answer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_21_without_no_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_21_without_no_good_answer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_22_Questionnaire_with_more_than_one_good_answer_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_22_with_more_than_one_good_answer_in_choices_in_questions.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_22_with_more_than_one_good_answer_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_23_Questionnaire_with_an_empty_array_in_choices_in_questions
Questionnaire( <json data>, json_test_files\json_23_with_an_empty_array_in_choices_in_questions.json ) --> None
Error : Incompatible Json schema in file json_test_files\json_23_with_an_empty_array_in_choices_in_questions.json
PASSED

questionnaire_unit_test.py::_10_Questionnaire_initialization::test_24_Questionnaire_with_questions_without_good_answer_only
Questionnaire( <json data>, json_test_files\json_24_with_questions_without_good_answer_only.json ) --> Questionnaire
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files\json_24_with_questions_without_good_answer_only.json
Warning : Skipped question : no one or more than one good answers in question 2 file json_test_files\json_24_with_questions_without_good_answer_only.json
PASSED

=================================================================================== 73 passed, 54 deselected in 7.04s ===================================================================================
```

[README.md](./README.md) > [questionnaire_unit_test.md](./questionnaire_unit_test.md)