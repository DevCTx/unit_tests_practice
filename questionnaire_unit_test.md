[README.md](./README.md) > [questionnaire_unit_test.md](./questionnaire_unit_test.md)

# Questionnaire_unit_tests.py 

Uses the 'unittest' automated framework but not only to test questionnaire.py

```commandline
python3 -m unittest questionnaire_unit_test

pytest -v -k questionnaire_unit_test.py -s
```
Note : All tests are described following the format :\
`test number`->`returned values` if receives __argument(s)__ then prints `message`

**The tests are orchestrated to be progressive :**
- **Level 1** : Basic Unit tests with argument parsing on a local file
- **Level 2** : Same tests but with a different name of program
- **Level 3** : Same tests but with a file into a folder


---
### Level 1 : Basic Unit tests with argument parsing on a local file

the argument are read and handled by the `load_json_argv` function which should return the json data `<Json_Data>`
and the file path `<File_Path>`
`
 
| Test | What it checks | Msg | json | file_path |
|---|---|---|---|---|
| `test_01` | __a good json file__ | None | Data | Path |
| `test_02` | __no file__ | Error in argument, should add a single .json questionnaire | None | None |
| `test_03` | __more than one file__ | Error in argument, should add a single .json questionnaire | None | None |
| `test_04` | __a file without json extension__ | Incorrect extension, add a .json questionnaire | None | Path |
| `test_05` | __a non-existent file__ | Invalid permissions or path to non-existent-file.json | None | Path |
| `test_06` | __an empty json file__ | Incompatible or no data in JSON file <file> | None | Path |

---
### Level 2 : Same tests but with a different name of program

If the name of the questionnaire.py change, the error messages should adapt.\
Inherits Level 1 and simulates a program named `test.py`

---
### Level 3 : Same tests but with a file into a folder

The class derives from the level 1 and executes the same tests except that 
a [json_test_files](./json_test_files) folder is added to the path of the file given in argument

| Test | What it checks | Msg | json | file_path |
|---|---|---|---|---|
| `test_02` | __a folder (no file)__ | Incorrect extension, add a .json questionnaire | None | Path |

---
### Level 4 : Same tests but with another name and a file into a folder 

Inherits Levels 2 and 3: same as Level 3, with the `test.py` script name in the messages

---
### Level 5 :  Loading from a real URL 

Sample file used: `https://countwordsfree.com/example.json`.
 
| Test | What it checks | Msg | json | file_path |
|---|---|---|---|---|
| `test_01` | __a valid json file on a valid url__ | None | Data | Path |
| `test_02` | __an invalid json file on a valid url__ | File not found at URL <url> | None | Path |
| `test_03` | __a valid json file on an invalid url__ | Invalid URL at <url> | None | Path |
| `test_04` | __a file without json extension on a valid url__ | Incorrect extension, add a .json questionnaire | None | Path |

---
### Level 6 : Loading over a local HTTP server (`setUp` / `tearDown`)

A simple HTTP server is started through a thread with `setUp` and close with `tearDown`.\
Those 2 `unittest.TestCase` methods are respectively called before and after each test of the class and can be overwritten.

The class inherits from Level 1, but served over `http://127.0.0.1`. \
The argument is now a URL, so a few messages change.

| Test | What it checks | Msg | json | file_path |
|---|---|---|---|---|
| `test_01` | __a good json file__ | None | Data | Path |
| `test_02` | __no file (folder url)__ | Incorrect extension, add a .json questionnaire | None | Path |
| `test_03` | __more than one file__ | Error in argument, should add a single .json questionnaire | None | None |
| `test_04` | __a file without json extension__ | Incorrect extension, add a .json questionnaire | None | Path |
| `test_05` | __a non-existent file__ | File not found at URL <url> | None | Path |
| `test_06` | __an empty json file__ | Incompatible or no data in JSON file at URL <url> | None | Path |


---
### Level 7 : Optimizing Level 6 with pytest  

Rather than opening and closing an HTTP server for each test, it would be better to open and close it once for all tests in the class.

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

Identical cases to Level 6. The server is opened/closed once per class by a class-scoped
`@pytest.fixture(autouse=True)`. **Skipped under `unittest`** (pytest only).

---
### Level 8 : Optimizing Level 6 with unittests built-in `@classmethod` tag

In the same idea as Level 7 with fixtures, it is possible to call the built-in methods `setUpClass` and `tearDownClass` at the beginning and at the end of the tests of the class.

To do this, the `self` argument must be modified to `cls` because these built-in functions are private to the unittest class, and the built-in `@classmethod` tag must be added over the class in order to force the access to them.

This class is identical cases to Level 6, using the `unittest` built-in class methods to start the server once for the whole class.

---
### Level 9 : Tests with a patch on network requests

Finally, unit tests should be isolated and not depend on the system or the network in order to be able, for example, to measure 
exactly the time needed to proceed without a external dependency.

It should so better to simulate the answers of the network requests like ``Success (200)`` 
or ``File Not Found (404)`` for example, to get the best knowledge of the program behavior.

This may require to rewrite the tests because the reading of the file from URL must also be simulated, like in this 2 
tests trying to read files from a non-existent Web URL.

| Test | What it checks | Msg | json | file_path |
|---|---|---|---|---|
| `test_01` | __a json file on a non-existent url with a simulated 404 answer__ | File not found at URL <url> | None | Path |
| `test_02` | __a json file on a non-existent url with a simulated 200 answer + fake data__ | None | Data | Path |

---
### Level 10 : Json Tests

These tests are prepared to know if a `Questionnaire` instance is created or not according to the json file received in argument. 

According to the [expected json format](./questionnaire.md#expected-json-schema), the properties `categorie` and `difficulté` are not required, so they will be saved as unknown (`inconnue`) if they are non-existent or empty and won't disturb the good behavior of the application.

| Test | What it checks | Msg | Result |
|---|---|---|---|
| `test_00` | __empty file__ | Incompatible or no data in JSON file <file> — Wrong arguments, should be test on load_json_argv | None |
| `test_01` | __a good format file__ | None | Questionnaire |
| `test_02` | __a file without not-mandatory category__ | None | Questionnaire |
| `test_03` | __a file with empty not-mandatory category__ | None | Questionnaire |
| `test_04` | __a file without not-mandatory difficulty__ | None | Questionnaire |
| `test_05` | __a file with empty not-mandatory difficulty__ | None | Questionnaire |
| `test_06` | __a file without mandatory title__ | Incompatible Json schema in file <file> | None |
| `test_07` | __a file with empty title__ | The title of the quizz is missing and mandatory in file <file> | None |
| `test_08` | __a file without mandatory questions__ | Incompatible Json schema in file <file> | None |
| `test_09` | __a file with empty questions__ | The questions of the quizz are missing and mandatory in file <file> | None |
| `test_10` | __a file with more keys__ | None | Questionnaire |
| `test_11` | __a file without title in questions__ | Incompatible Json schema in file <file> | None |
| `test_12` | __a file with an empty title in a question__ | ⚠ Skipped question : question is empty in question <n> | Questionnaire |
| `test_13` | __a file without choice in questions__ | Incompatible Json schema in file <file> | None |
| `test_14` | __a file with an empty choice array in questions__ | Incompatible Json schema in file <file> | None |
| `test_15` | __a file with only one choice in questions__ | Incompatible Json schema in file <file> | None |
| `test_16` | __a file without answer in choices in questions__ | Incompatible Json schema in file <file> | None |
| `test_17` | __a file with an empty wrong answer in choices__ | ⚠ Skipped answer : answer is empty in question <n> | Questionnaire |
| `test_18` | __a file with an empty good answer in choices__ | ⚠ Skipped answer : answer is empty… — ⚠ Skipped question : no one or more than one good answers… | Questionnaire |
| `test_19` | __a file without boolean in choices__ | Incompatible Json schema in file <file> | None |
| `test_20` | __a file with an integer instead of the boolean__ | Incompatible Json schema in file <file> | None |
| `test_21` | __a file without good answer in choices__ | ⚠ Skipped question : no one or more than one good answers in question <n> | Questionnaire |
| `test_22` | __a file with more than one good answer in choices__ | ⚠ Skipped question : no one or more than one good answers in question <n> | Questionnaire |
| `test_23` | __a file with an empty array in choices__ | Incompatible Json schema in file <file> | None |
| `test_24` | __a file with questions without good answer only__ | every question is dropped, so at run time the quiz prints "Not compatible questions" and is skipped entirely | None |



---
### More Unit Tests and Documentations

More information and independent tests about marks, fixtures, patch, local server in thread, json schema, pytest.ini or
conftest.py files, etc ... are available in [more_unit_tests_methods](./more_unit_tests_methods) folder.

Thank you for reading.

---
### Final results with unittests

```bash
python3 -m unittest questionnaire_unit_test -v 
```
```commandline
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._01_load_json_argv.test_01_load_json_argv_with_one_good_json_file) ... 
questionnaire.py json_01_good_format.json -> Json_Data, File_Path
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._01_load_json_argv.test_02_load_json_argv_with_no_argv) ... 
questionnaire.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._01_load_json_argv.test_03_load_json_argv_with_more_than_one_argv) ... 
questionnaire.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._01_load_json_argv.test_04_load_json_argv_with_argv_without_json_extension) ... 
questionnaire.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._01_load_json_argv.test_05_load_json_argv_with_non_existent_json_file) ... 
questionnaire.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._01_load_json_argv.test_06_load_json_argv_with_empty_json_file) ... 
questionnaire.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
ok
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._02_load_json_argv_with_another_name.test_01_load_json_argv_with_one_good_json_file) ... 
test.py json_01_good_format.json -> Json_Data, File_Path
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._02_load_json_argv_with_another_name.test_02_load_json_argv_with_no_argv) ... 
test.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._02_load_json_argv_with_another_name.test_03_load_json_argv_with_more_than_one_argv) ... 
test.py json_01_good_format.json json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._02_load_json_argv_with_another_name.test_04_load_json_argv_with_argv_without_json_extension) ... 
test.py json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._02_load_json_argv_with_another_name.test_05_load_json_argv_with_non_existent_json_file) ... 
test.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._02_load_json_argv_with_another_name.test_06_load_json_argv_with_empty_json_file) ... 
test.py json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_00_empty.json
ok
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_01_load_json_argv_with_one_good_json_file) ... 
questionnaire.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_02_load_json_argv_with_no_argv) ... 
questionnaire.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_03_load_json_argv_with_more_than_one_argv) ... 
questionnaire.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_04_load_json_argv_with_argv_without_json_extension) ... 
questionnaire.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_05_load_json_argv_with_non_existent_json_file) ... 
questionnaire.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._03_load_json_argv_with_file_in_folder.test_06_load_json_argv_with_empty_json_file) ... 
questionnaire.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
ok
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_01_load_json_argv_with_one_good_json_file) ... 
test.py json_test_files/json_01_good_format.json -> Json_Data, File_Path
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_02_load_json_argv_with_no_argv) ... 
test.py json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_03_load_json_argv_with_more_than_one_argv) ... 
test.py json_test_files/json_01_good_format.json json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_04_load_json_argv_with_argv_without_json_extension) ... 
test.py json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_05_load_json_argv_with_non_existent_json_file) ... 
test.py json_test_files/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_test_files/non-existent-file.json
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._04_load_json_argv_with_file_in_folder_and_another_name.test_06_load_json_argv_with_empty_json_file) ... 
test.py json_test_files/json_00_empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
ok
test_01_load_json_argv_with_json_file_sample_online (questionnaire_unit_test._05_load_json_argv_with_data_online.test_01_load_json_argv_with_json_file_sample_online) ... 
questionnaire.py https://countwordsfree.com/example.json -> Json_Data, File_Path
ok
test_02_load_json_argv_with_invalid_json_file_sample_online (questionnaire_unit_test._05_load_json_argv_with_data_online.test_02_load_json_argv_with_invalid_json_file_sample_online) ... 
questionnaire.py https://countwordsfree.com/non-existant.json -> None, File_Path
Error : File not found at URL https://countwordsfree.com/non-existant.json
ok
test_03_load_json_argv_with_invalid_url (questionnaire_unit_test._05_load_json_argv_with_data_online.test_03_load_json_argv_with_invalid_url) ... 
questionnaire.py https://countwordsfre.com/example.json -> None, File_Path
Error : Invalid URL at https://countwordsfre.com/example.json
ok
test_04_load_json_argv_with_empty_or_uncompleted_file_online (questionnaire_unit_test._05_load_json_argv_with_data_online.test_04_load_json_argv_with_empty_or_uncompleted_file_online) ... 
questionnaire.py https://countwordsfree.com/empty_or_uncompleted_file -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_01_load_json_argv_with_one_good_json_file) ... 

Connection to http://127.0.0.1:50967/ in Thread-1 (serve_forever) 
questionnaire.py http://127.0.0.1:50967/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:23] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:50967/
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_02_load_json_argv_with_no_argv) ... 

Connection to http://127.0.0.1:55735/ in Thread-3 (serve_forever) 
questionnaire.py http://127.0.0.1:55735/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:55735/
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_03_load_json_argv_with_more_than_one_argv) ... 

Connection to http://127.0.0.1:55233/ in Thread-4 (serve_forever) 
questionnaire.py http://127.0.0.1:55233/json_test_files/json_01_good_format.json http://127.0.0.1:55233/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:55233/
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_04_load_json_argv_with_argv_without_json_extension) ... 

Connection to http://127.0.0.1:54449/ in Thread-5 (serve_forever) 
questionnaire.py http://127.0.0.1:54449/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:54449/
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_05_load_json_argv_with_non_existent_json_file) ... 

Connection to http://127.0.0.1:47915/ in Thread-6 (serve_forever) 
questionnaire.py http://127.0.0.1:47915/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:25] code 404, message File not found
127.0.0.1 - - [30/Jun/2026 15:21:25] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:47915/json_test_files/non-existent-file.json
Disconnection from http://127.0.0.1:47915/
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown.test_06_load_json_argv_with_empty_json_file) ... 

Connection to http://127.0.0.1:48385/ in Thread-8 (serve_forever) 
questionnaire.py http://127.0.0.1:48385/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:25] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:48385/json_test_files/json_00_empty.json
Disconnection from http://127.0.0.1:48385/
ok
test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_01_load_json_argv_with_one_good_json_file) ... skipped 'requires pytest'
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_02_load_json_argv_with_no_argv) ... skipped 'requires pytest'
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_03_load_json_argv_with_more_than_one_argv) ... skipped 'requires pytest'
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_04_load_json_argv_with_argv_without_json_extension) ... skipped 'requires pytest'
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_05_load_json_argv_with_non_existent_json_file) ... skipped 'requires pytest'
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._07_load_json_argv_with_data_via_localhost_8000_in_fixture.test_06_load_json_argv_with_empty_json_file) ... skipped 'requires pytest'


Connection to http://127.0.0.1:48907/ in Thread-10 (serve_forever)test_01_load_json_argv_with_one_good_json_file (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_01_load_json_argv_with_one_good_json_file) ...  
questionnaire.py http://127.0.0.1:48907/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:26] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
ok
test_02_load_json_argv_with_no_argv (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_02_load_json_argv_with_no_argv) ... 
questionnaire.py http://127.0.0.1:48907/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_03_load_json_argv_with_more_than_one_argv (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_03_load_json_argv_with_more_than_one_argv) ... 
questionnaire.py http://127.0.0.1:48907/json_test_files/json_01_good_format.json http://127.0.0.1:48907/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_04_load_json_argv_with_argv_without_json_extension (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_04_load_json_argv_with_argv_without_json_extension) ... 
questionnaire.py http://127.0.0.1:48907/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
ok
test_05_load_json_argv_with_non_existent_json_file (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_05_load_json_argv_with_non_existent_json_file) ... 
questionnaire.py http://127.0.0.1:48907/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:26] code 404, message File not found
127.0.0.1 - - [30/Jun/2026 15:21:26] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:48907/json_test_files/non-existent-file.json
ok
test_06_load_json_argv_with_empty_json_file (questionnaire_unit_test._08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass.test_06_load_json_argv_with_empty_json_file) ... 
questionnaire.py http://127.0.0.1:48907/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:21:26] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:48907/json_test_files/json_00_empty.json
ok
Disconnection from http://127.0.0.1:48907/
test_01_load_json_argv_with_simulated_FileNotFound_answer (questionnaire_unit_test._09_load_json_argv_with_simulated_server.test_01_load_json_argv_with_simulated_FileNotFound_answer) ... 
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/json_01_good_format.json
ok
test_02_load_json_argv_with_simulated_success_request_and_fake_data (questionnaire_unit_test._09_load_json_argv_with_simulated_server.test_02_load_json_argv_with_simulated_success_request_and_fake_data) ... 
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> Json_Data, File_Path
ok
test_00_Questionnaire_empty_file (questionnaire_unit_test._10_Questionnaire_initialization.test_00_Questionnaire_empty_file) ... 
Questionnaire( <json data>, json_test_files/json_00_empty.json ) --> None 
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
--> Wrong arguments, should be test on load_json_argv
ok
test_01_Questionnaire_good_format_file (questionnaire_unit_test._10_Questionnaire_initialization.test_01_Questionnaire_good_format_file) ... 
Questionnaire( <json data>, json_test_files/json_01_good_format.json ) --> Questionnaire 
ok
test_02_Questionnaire_without_not_mandatory_category (questionnaire_unit_test._10_Questionnaire_initialization.test_02_Questionnaire_without_not_mandatory_category) ... 
Questionnaire( <json data>, json_test_files/json_02_without_category.json ) --> Questionnaire 
ok
test_03_Questionnaire_with_empty_not_mandatory_category (questionnaire_unit_test._10_Questionnaire_initialization.test_03_Questionnaire_with_empty_not_mandatory_category) ... 
Questionnaire( <json data>, json_test_files/json_03_with_empty_category.json ) --> Questionnaire 
ok
test_04_Questionnaire_without_not_mandatory_difficulty (questionnaire_unit_test._10_Questionnaire_initialization.test_04_Questionnaire_without_not_mandatory_difficulty) ... 
Questionnaire( <json data>, json_test_files/json_04_without_difficulty.json ) --> Questionnaire 
ok
test_05_Questionnaire_with_empty_not_mandatory_difficulty (questionnaire_unit_test._10_Questionnaire_initialization.test_05_Questionnaire_with_empty_not_mandatory_difficulty) ... 
Questionnaire( <json data>, json_test_files/json_05_with_empty_difficulty.json ) --> Questionnaire 
ok
test_06_Questionnaire_without_mandatory_title (questionnaire_unit_test._10_Questionnaire_initialization.test_06_Questionnaire_without_mandatory_title) ... 
Questionnaire( <json data>, json_test_files/json_06_without_title.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_06_without_title.json
ok
test_07_Questionnaire_with_empty_title (questionnaire_unit_test._10_Questionnaire_initialization.test_07_Questionnaire_with_empty_title) ... 
Questionnaire( <json data>, json_test_files/json_07_with_empty_title.json ) --> None 
Error : The title of the quizz is missing and mandatory in file json_test_files/json_07_with_empty_title.json
ok
test_08_Questionnaire_without_mandatory_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_08_Questionnaire_without_mandatory_questions) ... 
Questionnaire( <json data>, json_test_files/json_08_without_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_08_without_questions.json
ok
test_09_Questionnaire_with_empty_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_09_Questionnaire_with_empty_questions) ... 
Questionnaire( <json data>, json_test_files/json_09_with_empty_questions.json ) --> None 
Error : The questions of the quizz are missing and mandatory in file json_test_files/json_09_with_empty_questions.json
ok
test_10_Questionnaire_with_more_keys (questionnaire_unit_test._10_Questionnaire_initialization.test_10_Questionnaire_with_more_keys) ... 
Questionnaire( <json data>, json_test_files/json_10_with_more_keys.json ) --> Questionnaire 
ok
test_11_Questionnaire_without_title_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_11_Questionnaire_without_title_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_11_without_title_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_11_without_title_in_questions.json
ok
test_12_Questionnaire_with_empty_title_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_12_Questionnaire_with_empty_title_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_12_with_empty_title_in_questions.json ) --> Questionnaire 
Warning : Skipped question : question is empty in question 1 file json_test_files/json_12_with_empty_title_in_questions.json
ok
test_13_Questionnaire_without_choice_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_13_Questionnaire_without_choice_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_13_without_choice_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_13_without_choice_in_questions.json
ok
test_14_Questionnaire_with_empty_choice_array_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_14_Questionnaire_with_empty_choice_array_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_14_with_empty_choice_array_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_14_with_empty_choice_array_in_questions.json
ok
test_15_Questionnaire_with_only_one_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_15_Questionnaire_with_only_one_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_15_with_only_one_choice_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_15_with_only_one_choice_in_questions.json
ok
test_16_Questionnaire_without_answer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_16_Questionnaire_without_answer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_16_without_answer_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_16_without_answer_in_choices_in_questions.json
ok
test_17_Questionnaire_with_empty_wrong_answer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_17_Questionnaire_with_empty_wrong_answer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_17_with_empty_wrong_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped answer : answer is empty in question 1 file json_test_files/json_17_with_empty_wrong_answer_in_choices_in_questions.json
ok
test_18_Questionnaire_with_empty_good_answer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_18_Questionnaire_with_empty_good_answer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped answer : answer is empty in question 1 file json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json
ok
test_19_Questionnaire_without_boolean_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_19_Questionnaire_without_boolean_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_19_without_boolean_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_19_without_boolean_in_choices_in_questions.json
ok
test_20_Questionnaire_with_integer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_20_Questionnaire_with_integer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_20_with_integer_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_20_with_integer_in_choices_in_questions.json
ok
test_21_Questionnaire_without_no_good_answer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_21_Questionnaire_without_no_good_answer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_21_without_no_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_21_without_no_good_answer_in_choices_in_questions.json
ok
test_22_Questionnaire_with_more_than_one_good_answer_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_22_Questionnaire_with_more_than_one_good_answer_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_22_with_more_than_one_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_22_with_more_than_one_good_answer_in_choices_in_questions.json
ok
test_23_Questionnaire_with_an_empty_array_in_choices_in_questions (questionnaire_unit_test._10_Questionnaire_initialization.test_23_Questionnaire_with_an_empty_array_in_choices_in_questions) ... 
Questionnaire( <json data>, json_test_files/json_23_with_an_empty_array_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_23_with_an_empty_array_in_choices_in_questions.json
ok
test_24_Questionnaire_with_questions_without_good_answer_only (questionnaire_unit_test._10_Questionnaire_initialization.test_24_Questionnaire_with_questions_without_good_answer_only) ... 
Questionnaire( <json data>, json_test_files/json_24_with_questions_without_good_answer_only.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_24_with_questions_without_good_answer_only.json
Warning : Skipped question : no one or more than one good answers in question 2 file json_test_files/json_24_with_questions_without_good_answer_only.json
ok

----------------------------------------------------------------------
Ran 73 tests in 4.908s

OK (skipped=6)
```
---
### Final results with pytest

```bash
pytest -v -k questionnaire_unit_test.py -s
```

```python
============================================================================================================ test session starts =============================================================================================================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- ~/unit_tests_practice/venv/bin/python3
cachedir: .pytest_cache
rootdir: ~/unit_tests_practice
configfile: pytest.ini
collecting ... ok
collected 126 items / 53 deselected / 73 selected                                                                                                                                                                                            

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

Connection to http://127.0.0.1:60393/ in Thread-1 (serve_forever) 
questionnaire.py http://127.0.0.1:60393/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:15] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:60393/
PASSED
questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_02_load_json_argv_with_no_argv 

Connection to http://127.0.0.1:55809/ in Thread-3 (serve_forever) 
questionnaire.py http://127.0.0.1:55809/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:55809/
PASSED
questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_03_load_json_argv_with_more_than_one_argv 

Connection to http://127.0.0.1:40861/ in Thread-4 (serve_forever) 
questionnaire.py http://127.0.0.1:40861/json_test_files/json_01_good_format.json http://127.0.0.1:40861/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:40861/
PASSED
questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_04_load_json_argv_with_argv_without_json_extension 

Connection to http://127.0.0.1:40203/ in Thread-5 (serve_forever) 
questionnaire.py http://127.0.0.1:40203/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:40203/
PASSED
questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_05_load_json_argv_with_non_existent_json_file 

Connection to http://127.0.0.1:58481/ in Thread-6 (serve_forever) 
questionnaire.py http://127.0.0.1:58481/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:17] code 404, message File not found
127.0.0.1 - - [30/Jun/2026 15:14:17] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:58481/json_test_files/non-existent-file.json
Disconnection from http://127.0.0.1:58481/
PASSED
questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_06_load_json_argv_with_empty_json_file 

Connection to http://127.0.0.1:49833/ in Thread-8 (serve_forever) 
questionnaire.py http://127.0.0.1:49833/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:17] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:49833/json_test_files/json_00_empty.json
Disconnection from http://127.0.0.1:49833/
PASSED
questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_01_load_json_argv_with_one_good_json_file 

HTTP Connection to http://127.0.0.1:8000/ in Thread-10 (serve_forever) 
questionnaire.py http://127.0.0.1:8000/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
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
127.0.0.1 - - [30/Jun/2026 15:14:18] code 404, message File not found
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_test_files/non-existent-file.json
PASSED
questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_06_load_json_argv_with_empty_json_file 
questionnaire.py http://127.0.0.1:8000/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_test_files/json_00_empty.json
PASSEDHTTP Disconnection from http://127.0.0.1:8000/

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_01_load_json_argv_with_one_good_json_file 

Connection to http://127.0.0.1:47413/ in Thread-14 (serve_forever) 
questionnaire.py http://127.0.0.1:47413/json_test_files/json_01_good_format.json -> Json_Data, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/json_01_good_format.json HTTP/1.1" 200 -
PASSED
questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_02_load_json_argv_with_no_argv 
questionnaire.py http://127.0.0.1:47413/json_test_files/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED
questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_03_load_json_argv_with_more_than_one_argv 
questionnaire.py http://127.0.0.1:47413/json_test_files/json_01_good_format.json http://127.0.0.1:47413/json_test_files/json_01_another_good_format.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED
questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_04_load_json_argv_with_argv_without_json_extension 
questionnaire.py http://127.0.0.1:47413/json_test_files/json_00_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED
questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_05_load_json_argv_with_non_existent_json_file 
questionnaire.py http://127.0.0.1:47413/json_test_files/non-existent-file.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:18] code 404, message File not found
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:47413/json_test_files/non-existent-file.json
PASSED
questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_06_load_json_argv_with_empty_json_file 
questionnaire.py http://127.0.0.1:47413/json_test_files/json_00_empty.json -> None, File_Path
127.0.0.1 - - [30/Jun/2026 15:14:18] "GET /json_test_files/json_00_empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:47413/json_test_files/json_00_empty.json
PASSEDDisconnection from http://127.0.0.1:47413/

questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_01_load_json_argv_with_simulated_FileNotFound_answer 
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/json_01_good_format.json
PASSED
questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_02_load_json_argv_with_simulated_success_request_and_fake_data 
questionnaire.py http://non-existent-url.com/json_01_good_format.json -> Json_Data, File_Path
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_00_Questionnaire_empty_file 
Questionnaire( <json data>, json_test_files/json_00_empty.json ) --> None 
Error : Incompatible or no data in JSON file json_test_files/json_00_empty.json
--> Wrong arguments, should be test on load_json_argv
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_01_Questionnaire_good_format_file 
Questionnaire( <json data>, json_test_files/json_01_good_format.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_02_Questionnaire_without_not_mandatory_category 
Questionnaire( <json data>, json_test_files/json_02_without_category.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_03_Questionnaire_with_empty_not_mandatory_category 
Questionnaire( <json data>, json_test_files/json_03_with_empty_category.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_04_Questionnaire_without_not_mandatory_difficulty 
Questionnaire( <json data>, json_test_files/json_04_without_difficulty.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_05_Questionnaire_with_empty_not_mandatory_difficulty 
Questionnaire( <json data>, json_test_files/json_05_with_empty_difficulty.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_06_Questionnaire_without_mandatory_title 
Questionnaire( <json data>, json_test_files/json_06_without_title.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_06_without_title.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_07_Questionnaire_with_empty_title 
Questionnaire( <json data>, json_test_files/json_07_with_empty_title.json ) --> None 
Error : The title of the quizz is missing and mandatory in file json_test_files/json_07_with_empty_title.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_08_Questionnaire_without_mandatory_questions 
Questionnaire( <json data>, json_test_files/json_08_without_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_08_without_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_09_Questionnaire_with_empty_questions 
Questionnaire( <json data>, json_test_files/json_09_with_empty_questions.json ) --> None 
Error : The questions of the quizz are missing and mandatory in file json_test_files/json_09_with_empty_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_10_Questionnaire_with_more_keys 
Questionnaire( <json data>, json_test_files/json_10_with_more_keys.json ) --> Questionnaire 
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_11_Questionnaire_without_title_in_questions 
Questionnaire( <json data>, json_test_files/json_11_without_title_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_11_without_title_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_12_Questionnaire_with_empty_title_in_questions 
Questionnaire( <json data>, json_test_files/json_12_with_empty_title_in_questions.json ) --> Questionnaire 
Warning : Skipped question : question is empty in question 1 file json_test_files/json_12_with_empty_title_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_13_Questionnaire_without_choice_in_questions 
Questionnaire( <json data>, json_test_files/json_13_without_choice_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_13_without_choice_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_14_Questionnaire_with_empty_choice_array_in_questions 
Questionnaire( <json data>, json_test_files/json_14_with_empty_choice_array_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_14_with_empty_choice_array_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_15_Questionnaire_with_only_one_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_15_with_only_one_choice_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_15_with_only_one_choice_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_16_Questionnaire_without_answer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_16_without_answer_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_16_without_answer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_17_Questionnaire_with_empty_wrong_answer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_17_with_empty_wrong_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped answer : answer is empty in question 1 file json_test_files/json_17_with_empty_wrong_answer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_18_Questionnaire_with_empty_good_answer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped answer : answer is empty in question 1 file json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_18_with_empty_good_answer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_19_Questionnaire_without_boolean_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_19_without_boolean_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_19_without_boolean_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_20_Questionnaire_with_integer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_20_with_integer_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_20_with_integer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_21_Questionnaire_without_no_good_answer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_21_without_no_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_21_without_no_good_answer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_22_Questionnaire_with_more_than_one_good_answer_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_22_with_more_than_one_good_answer_in_choices_in_questions.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_22_with_more_than_one_good_answer_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_23_Questionnaire_with_an_empty_array_in_choices_in_questions 
Questionnaire( <json data>, json_test_files/json_23_with_an_empty_array_in_choices_in_questions.json ) --> None 
Error : Incompatible Json schema in file json_test_files/json_23_with_an_empty_array_in_choices_in_questions.json
PASSED
questionnaire_unit_test.py::_10_Questionnaire_initialization::test_24_Questionnaire_with_questions_without_good_answer_only 
Questionnaire( <json data>, json_test_files/json_24_with_questions_without_good_answer_only.json ) --> Questionnaire 
Warning : Skipped question : no one or more than one good answers in question 1 file json_test_files/json_24_with_questions_without_good_answer_only.json
Warning : Skipped question : no one or more than one good answers in question 2 file json_test_files/json_24_with_questions_without_good_answer_only.json
PASSED

===================================================================================================== 73 passed, 53 deselected in 6.33s ======================================================================================================
```

[README.md](./README.md) > [questionnaire_unit_test.md](./questionnaire_unit_test.md)