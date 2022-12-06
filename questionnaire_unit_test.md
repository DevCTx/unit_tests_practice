[README.md](./README.md) > [questionnaire_unit_tests.md](./questionnaire_unit_tests.md)

# Questionnaire_unit_tests.py

Uses the 'unittest' automated framework but not only to test questionnaire.py

```commandline
python ./questionnaire_unit_tests.py
```
---
### Level 1 : Basic Unit tests about the arguments received by questionnaire.py

the argument are read and handled by the `load_json_argv` function which should return the json data `<Json_Data>`
and the file path `<File_Path>`

`test number`->`returned values` if receives __condition given in argument__ and prints `message`
 
- `test_01` -> `<Json_Data>, <File_Path>` if receives __a good json file__ and prints no message 
```commandline
questionnaire.py initial_json_test_file.json -> Json_Data, File_Path
```

- `test_02` -> `None, None` if receives __no file__ and prints a message.
```commandline
questionnaire.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_03` -> `None, None` if receives __more than one file__ and prints a message.
```commandline
questionnaire.py initial_json_test_file.json.json second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_04` -> `None, <File_Path>` if receives __a file without json extension__ and prints a message.
```commandline
questionnaire.py json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_05` -> `None, <File_Path>` if receives __a non-existent file__ and prints a message.
```commandline
questionnaire.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
```

- `test_06` -> `None, <File_Path>` if receives __an empty json file__ and prints a message.
```commandline
questionnaire.py empty.json -> None, File_Path
Error : Incompatible or no data in JSON file empty.json
```

---
### Level 2 : Same tests but with a different name of program
If the name of the questionnaire.py change, the error messages should adapt.\
The class test is derived from the level 1 but simulates a program named `test.py`

---
### Level 3 : Same tests but with a file into a folder

The class derives from the level 1 and executes the same tests except that 
a [json_file_tests](./json_file_tests) folder is added to the path of the file given in argument

The printed message of test 2 is quite different from the Level 1 since the file path is given in argument.
- `test_02` -> `None, <File_Path>` if receives __no file__ and prints a message
```commandline
questionnaire.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```
---
### Level 4 : Same tests but with another name and a file into a folder 

The class derives from the level 2 and 3 and executes the same tests under `test.py` name and with files 
from [json_file_tests](./json_file_tests)

The printed message of test 2 is so quite different from the Level 1 as well.
- `test_02` -> `None, <File_Path>` if receives __no file__ and prints a message.
```commandline
test.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
```

---
### Level 5 : Tests with data online 

A free json file is available at the url : https://countwordsfree.com/example.json

- `test_01` -> `<Json_Data>, <File_Path>` if receives __a valid json file on a valid url path__ and prints no message.
```commandline
questionnaire.py https://countwordsfree.com/example.json -> Json_Data, File_Path
```

- `test_02` -> `None, <File_Path>` if receives __a invalid json file on a valid url path__ and prints a message.
```commandline
questionnaire.py https://countwordsfree.com/non-existant.json -> None, File_Path
Error : File not found at URL https://countwordsfree.com/non-existant.json
```

- `test_03` -> `None, <File_Path>` if receives __a valid json file but on a invalid url path__ and prints a message.
```commandline
questionnaire.py https://countwordsfre.com/example.json -> None, File_Path
Error : Invalid URL at https://countwordsfre.com/example.json
```

- `test_04` -> `None, <File_Path>` if receives __a file without json extension on a valid url path__ and prints a message.
```commandline
questionnaire.py https://countwordsfree.com/empty_or_uncompleted_file -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

---
### Level 6 : Tests with data on http://localhost 

To go further and test wrong or empty json files, it is necessary to simulate a simple HTTP server 
via localhost(`http://127.0.0.1`) for example.

The simple HTTP server is started through a thread by the `setUp` method and close by the `tearDown` method. Those 
2 `unittest.TestCase` methods are respectively called before and after each test of the class and can be overwritten.

The class derives from the level 1 and therefore executes the same tests but through an HTTP connection.

- `test_01` -> `<Json_Data>, <File_Path>` if receives __a good json file__ and prints no message.
```commandline
questionnaire.py http://127.0.0.1:8000/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [02/Dec/2022 12:11:53] "GET /initial_json_test_file.json HTTP/1.1" 200 -
```

The printed message of test 2 is quite different from the Level 1 since the URL is given in argument.
- `test_02` -> `None, <File_Path>` if receives __no file__ and prints a message
```commandline
questionnaire.py http://127.0.0.1:8000/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_03` -> `None, None` if receives __more than one file__ and prints a message.
```commandline
questionnaire.py http://127.0.0.1:8000/initial_json_test_file.json.json http://127.0.0.1:8000/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_04` -> `None, File_Path` if receives __a file without json extension__ and prints a message.
```commandline
questionnaire.py http://127.0.0.1:8000/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
```

- `test_05` -> `None, File_Path` if receives __a non-existent file__ and prints a message.
```commandline
questionnaire.py http://127.0.0.1:8000/non-existent-file.json -> None, File_Path
Error : File not found at URL http://127.0.0.1:8000/non-existent-file.json
127.0.0.1 - - [02/Dec/2022 12:22:31] code 404, message File not found
127.0.0.1 - - [02/Dec/2022 12:22:31] "GET /non-existent-file.json HTTP/1.1" 404 -
```
- `test_0x` -> `None, File_Path` if receives __an empty json file__ and prints a message.
```commandline
questionnaire.py http://127.0.0.1:8000/empty.json -> None, File_Path
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/empty.json
127.0.0.1 - - [02/Dec/2022 12:22:31] "GET /empty.json HTTP/1.1" 200 -
```
---
### Level 7 : Optimized Level 6 with pytest  

Rather than opening and closing an HTTP server for each test, it would be better to open and close it once for all tests
in the class.

This needs to create a fixture defined on the `class` scope and to use the option `autouse=True`

The fixture will so open the server, before all the tests run, and will be close the server when it will be called a 
second time after that all tests ran.
```commandline
HTTP Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 15:28:35] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
PASSED
questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_02_load_json_argv_with_no_argv
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED
HTTP Disconnection from http://127.0.0.1:8000/
```
According to the definition of the fixture used in this test, this class will be executed only using `pytest` and 
will be skipped under `unittests`
```commandline
pytest -v -k questionnaire_unit_test.py -s
```
---
### Level 8 : Optimized Level 6 with unittests `@classmethod`

In the same idea as Level 7 with fixtures, it is possible to call the built-in methods `setUpClass` and `tearDownClass` 
at the beginning and at the end of the tests of the class.\
To do this, the `self` argument must be modified to `cls` because these built-in functions are private to the unittest 
class. It is also why it is also necessary to use the built-in tag `@classmethod` in order to access them.

---
### Level 9 : Tests with a patch on network requests

Unit tests should be isolated and not depend on the system or the network in order to be able, for example, to measure 
exactly the time needed to proceed without a external dependency.

It should so better to simulate the answers of the network requests like ``Success (200)`` 
or ``File Not Found (404)`` for getting the best knowledge of the program behavior.

This may require to rewrite the tests because the reading of the file from URL must also be simulated, like in this 2 
tests trying to read files from a non-existent URL of the Web.

- `test_01` -> `None, File_Path` if receives __a json file on a non-existent URL with a simulated ``File Not Found (404)`` answer to 
the network request__ and prints a message.
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/initial_json_test_file.json
```
- `test_02` -> `not None` if receives __a json file on a non-existent URL with a simulated ``Success (200)`` answer to the 
network request__ and prints no message.
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> Not None (OK)
```
in that case, the property ``status_code`` of the response must be updated to the code ``200 (OK)``
and the property ``text`` of the response must contain the json data read. This is simulated by the reading of a file 
from the given path without the server part ``./initial_json_test_file.json``

---
### More Unit Tests Documentations

More information and independent tests about marks, fixtures, patchs, local server in thread, json schema, pytest.ini or
conftest.py files, etc ... available in [more_unit_tests_docs](./more_unit_test_docs) folder.

Thank you for reading.