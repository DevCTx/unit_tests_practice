[README.md](./README.md) > [questionnaire_unit_tests.md](./questionnaire_unit_tests.md)

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
a [json_file_tests](./json_file_tests) folder is added to the path of the file given in argument

The printed message of test 2 is quite different from the Level 1 since the file path is given in argument.
- `test_02` -> `None, <File_Path>` if receives __no file__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire.```

---
### Level 4 : Same tests but with another name and a file into a folder 

The class derives from the level 2 and 3 and executes the same tests under `test.py` name and with files 
from [json_file_tests](./json_file_tests)

The printed message of test 2 is so quite different from the Level 1 as well.
- `test_02` -> `None, <File_Path>` if receives __no file__ then prints the message :\
```Error : Incorrect extension, add a .json questionnaire.```

---
### Level 5 : Tests with data online 

A free json file is available at the url : https://countwordsfree.com/example.json

- `test_01` -> `<Json_Data>, <File_Path>` if receives __a valid json file on a valid url path__ then prints no message.


- `test_02` -> `None, <File_Path>` if receives __a invalid json file on a valid url path__ then prints the message :\\
```Error : File not found at URL https://countwordsfree.com/non-existant.json```


- `test_03` -> `None, <File_Path>` if receives __a valid json file but on a invalid url path__ then prints the message :\\
```Error : Invalid URL at https://countwordsfre.com/example.json```


- `test_04` -> `None, <File_Path>` if receives __a file without json extension on a valid url path__ then prints the message :\\
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

- `test_05` -> `None, File_Path` if receives __a non-existent file__ then prints the message :\\
```Error : File not found at URL <URL>```


- `test_06` -> `None, File_Path` if receives __an empty json file__ then prints the message :\\
```Error : Incompatible or no data in JSON file at URL <URL>```


---
### Level 7 : Optimized Level 6 with pytest  

Rather than opening and closing an HTTP server for each test, it would be better to open and close it once for all tests
in the class.

This can be done by creating a fixture defined on the `class` scope and using the option `autouse=True` to automatically
applied it to all the tests of the parent class.

The fixture will so open the server, before all the tests run, and will be close the server when it will be called a 
second time after that all tests ran.
```commandline
HTTP Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
...
<tests>
...
HTTP Disconnection from http://127.0.0.1:8000/
```
Note : According to the definition of the fixture used in this test, this class will be executed only using `pytest` and 
will be skipped under `unittests`
```commandline
pytest -v -k questionnaire_unit_test.py -s
```

---
### Level 8 : Optimized Level 6 with unittests built-in `@classmethod` tag

In the same idea as Level 7 with fixtures, it is possible to call the built-in methods `setUpClass` and `tearDownClass` 
at the beginning and at the end of the tests of the class.\
To do this, the `self` argument must be modified to `cls` because these built-in functions are private to the unittest 
class. It is also why it is also necessary to use the built-in `@classmethod` tag in order to access them.

---
### Level 9 : Tests with a patch on network requests

Finally, unit tests should be isolated and not depend on the system or the network in order to be able, for example, to measure 
exactly the time needed to proceed without a external dependency.

It should so better to simulate the answers of the network requests like ``Success (200)`` 
or ``File Not Found (404)`` for example, to get the best knowledge of the program behavior.

This may require to rewrite the tests because the reading of the file from URL must also be simulated, like in this 2 
tests trying to read files from a non-existent URL of the Web.

- `test_01` -> `None, File_Path` if receives __a json file on a non-existent URL with a simulated ``File Not Found (404)`` answer to 
the network request__ then prints the message :\
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/initial_json_test_file.json
```
- `test_02` -> `Json_Data, File_Path` if receives __a json file on a non-existent URL with a simulated ``Success (200)`` answer to the 
network request__ then prints no message.
```commandline
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> Json_Data, File_Path
```
In that case, the property `status_code` of the response must be updated to the code `200 (OK)` and the property `text`
of the response must contain the read json data. This is simulated by the reading of a file from the given path without 
the server part ``./initial_json_test_file.json``

---
### Level 10 : Json Tests


---
### More Unit Tests Documentations

More information and independent tests about marks, fixtures, patchs, local server in thread, json schema, pytest.ini or
conftest.py files, etc ... available in [more_unit_tests_docs](./more_unit_test_docs) folder.

Thank you for reading.

---
### Final results with unittests

```commandline 
python questionnaire_unit_test.py         

questionnaire.py initial_json_test_file.json -> Json_Data, File_Path
.                                                                                                                        
questionnaire.py -> None, None                                                                                           
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.                                                                                                                        
questionnaire.py initial_json_test_file.json.json second_json_test_file.json -> None, None                               
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.                                                                                                                        
questionnaire.py json_file_without_extension -> None, File_Path                                                          
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json            
.                                                                                                                        
questionnaire.py non-existent-file.json -> None, File_Path                                                               
Error : Invalid permissions or path to non-existent-file.json                                                            
.                                                                                                                        
questionnaire.py empty.json -> None, File_Path                                                                           
Error : Incompatible or no data in JSON file empty.json                                                                  
.                                                                                                                        
test.py initial_json_test_file.json -> Json_Data, File_Path                                                              
.
test.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py initial_json_test_file.json.json second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
.
test.py empty.json -> None, File_Path
Error : Incompatible or no data in JSON file empty.json
.
questionnaire.py json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
.
questionnaire.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_file_tests/initial_json_test_file.json.json json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py json_file_tests/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_file_tests/non-existent-file.json
.
questionnaire.py json_file_tests/empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_file_tests/empty.json
.
test.py json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
.
test.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_file_tests/initial_json_test_file.json.json json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
.
test.py json_file_tests/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_file_tests/non-existent-file.json
.
test.py json_file_tests/empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_file_tests/empty.json
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
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:06] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:8000/
.

Connection to http://127.0.0.1:8000/ in Thread-3 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.

Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json.json http://127.0.0.1:8000/json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.

Connection to http://127.0.0.1:8000/ in Thread-5 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
.

Connection to http://127.0.0.1:8000/ in Thread-6 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/non-existent-file.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:08] code 404, message File not found
127.0.0.1 - - [05/Dec/2022 18:30:08] "GET /json_file_tests/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_file_tests/non-existent-file.json
Disconnection from http://127.0.0.1:8000/
.

Connection to http://127.0.0.1:8000/ in Thread-8 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/empty.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:08] "GET /json_file_tests/empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_file_tests/empty.json
Disconnection from http://127.0.0.1:8000/
.ssssss

Connection to http://127.0.0.1:8000/ in Thread-10 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:09] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
.
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json.json http://127.0.0.1:8000/json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
.
questionnaire.py http://127.0.0.1:8000/json_file_tests/non-existent-file.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:09] code 404, message File not found
127.0.0.1 - - [05/Dec/2022 18:30:09] "GET /json_file_tests/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_file_tests/non-existent-file.json
.
questionnaire.py http://127.0.0.1:8000/json_file_tests/empty.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:09] "GET /json_file_tests/empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_file_tests/empty.json
.Disconnection from http://127.0.0.1:8000/

questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/initial_json_test_file.json
.
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> Json_Data, File_Path
.
----------------------------------------------------------------------
Ran 48 tests in 5.413s

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
collected 102 items / 54 deselected / 48 selected

questionnaire_unit_test.py::_01_load_json_argv::test_01_load_json_argv_with_one_good_json_file                           
questionnaire.py initial_json_test_file.json -> Json_Data, File_Path                                                     
PASSED               
                                                                                                    
questionnaire_unit_test.py::_01_load_json_argv::test_02_load_json_argv_with_no_argv                                      
questionnaire.py -> None, None                                                                                           
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED                                                                                                                   

questionnaire_unit_test.py::_01_load_json_argv::test_03_load_json_argv_with_more_than_one_argv                           
questionnaire.py initial_json_test_file.json.json second_json_test_file.json -> None, None                               
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED                                                                                                                   

questionnaire_unit_test.py::_01_load_json_argv::test_04_load_json_argv_with_argv_without_json_extension                  
questionnaire.py json_file_without_extension -> None, File_Path                                                          
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json            
PASSED                                                                                                                   

questionnaire_unit_test.py::_01_load_json_argv::test_05_load_json_argv_with_non_existent_json_file                       
questionnaire.py non-existent-file.json -> None, File_Path                                                               
Error : Invalid permissions or path to non-existent-file.json                                                            
PASSED

questionnaire_unit_test.py::_01_load_json_argv::test_06_load_json_argv_with_empty_json_file
questionnaire.py empty.json -> None, File_Path
Error : Incompatible or no data in JSON file empty.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_01_load_json_argv_with_one_good_json_file
test.py initial_json_test_file.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_02_load_json_argv_with_no_argv
test.py -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_03_load_json_argv_with_more_than_one_argv
test.py initial_json_test_file.json.json second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_04_load_json_argv_with_argv_without_json_extension
test.py json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_05_load_json_argv_with_non_existent_json_file
test.py non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to non-existent-file.json
PASSED

questionnaire_unit_test.py::_02_load_json_argv_with_another_name::test_06_load_json_argv_with_empty_json_file
test.py empty.json -> None, File_Path
Error : Incompatible or no data in JSON file empty.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_01_load_json_argv_with_one_good_json_file
questionnaire.py json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_02_load_json_argv_with_no_argv
questionnaire.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py json_file_tests/initial_json_test_file.json.json json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py json_file_tests/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_file_tests/non-existent-file.json
PASSED

questionnaire_unit_test.py::_03_load_json_argv_with_file_in_folder::test_06_load_json_argv_with_empty_json_file
questionnaire.py json_file_tests/empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_file_tests/empty.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_01_load_json_argv_with_one_good_json_file
test.py json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_02_load_json_argv_with_no_argv
test.py json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_03_load_json_argv_with_more_than_one_argv
test.py json_file_tests/initial_json_test_file.json.json json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_04_load_json_argv_with_argv_without_json_extension
test.py json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : test.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_05_load_json_argv_with_non_existent_json_file
test.py json_file_tests/non-existent-file.json -> None, File_Path
Error : Invalid permissions or path to json_file_tests/non-existent-file.json
PASSED

questionnaire_unit_test.py::_04_load_json_argv_with_file_in_folder_and_another_name::test_06_load_json_argv_with_empty_json_file
test.py json_file_tests/empty.json -> None, File_Path
Error : Incompatible or no data in JSON file json_file_tests/empty.json
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
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 18:30:59] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_02_load_json_argv_with_no_argv
Connection to http://127.0.0.1:8000/ in Thread-3 (serve_forever) 
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_03_load_json_argv_with_more_than_one_argv
Connection to http://127.0.0.1:8000/ in Thread-4 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json.json http://127.0.0.1:8000/json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_04_load_json_argv_with_argv_without_json_extension
Connection to http://127.0.0.1:8000/ in Thread-5 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_05_load_json_argv_with_non_existent_json_file
Connection to http://127.0.0.1:8000/ in Thread-6 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/non-existent-file.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:01] code 404, message File not found
127.0.0.1 - - [05/Dec/2022 18:31:01] "GET /json_file_tests/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_file_tests/non-existent-file.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_06_load_json_argv_with_data_via_localhost_8000_in_setup_teardown::test_06_load_json_argv_with_empty_json_file
Connection to http://127.0.0.1:8000/ in Thread-8 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/empty.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:02] "GET /json_file_tests/empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_file_tests/empty.json
Disconnection from http://127.0.0.1:8000/
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_01_load_json_argv_with_one_good_json_file
HTTP Connection to http://127.0.0.1:8000/ in Thread-10 (serve_forever) 
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:02] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_02_load_json_argv_with_no_argv
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json.json http://127.0.0.1:8000/json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py http://127.0.0.1:8000/json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py http://127.0.0.1:8000/json_file_tests/non-existent-file.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:02] code 404, message File not found
127.0.0.1 - - [05/Dec/2022 18:31:02] "GET /json_file_tests/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_file_tests/non-existent-file.json
PASSED

questionnaire_unit_test.py::_07_load_json_argv_with_data_via_localhost_8000_in_fixture::test_06_load_json_argv_with_empty_json_file
questionnaire.py http://127.0.0.1:8000/json_file_tests/empty.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:02] "GET /json_file_tests/empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_file_tests/empty.json
PASSED
HTTP Disconnection from http://127.0.0.1:8000/

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_01_load_json_argv_with_one_good_json_file 
Connection to http://127.0.0.1:8000/ in Thread-14 (serve_forever)
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json -> Json_Data, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:03] "GET /json_file_tests/initial_json_test_file.json HTTP/1.1" 200 -
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_02_load_json_argv_with_no_argv
questionnaire.py http://127.0.0.1:8000/json_file_tests/ -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_03_load_json_argv_with_more_than_one_argv
questionnaire.py http://127.0.0.1:8000/json_file_tests/initial_json_test_file.json.json http://127.0.0.1:8000/json_file_tests/second_json_test_file.json -> None, None
Error : Error in argument, should add a single .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_04_load_json_argv_with_argv_without_json_extension
questionnaire.py http://127.0.0.1:8000/json_file_tests/json_file_without_extension -> None, File_Path
Error : Incorrect extension, add a .json questionnaire. Example : questionnaire.py questionnaire_to_read.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_05_load_json_argv_with_non_existent_json_file
questionnaire.py http://127.0.0.1:8000/json_file_tests/non-existent-file.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:03] code 404, message File not found
127.0.0.1 - - [05/Dec/2022 18:31:03] "GET /json_file_tests/non-existent-file.json HTTP/1.1" 404 -
Error : File not found at URL http://127.0.0.1:8000/json_file_tests/non-existent-file.json
PASSED

questionnaire_unit_test.py::_08_load_json_argv_with_data_via_localhost_8000_in_setupClass_teardownClass::test_06_load_json_argv_with_empty_json_file
questionnaire.py http://127.0.0.1:8000/json_file_tests/empty.json -> None, File_Path
127.0.0.1 - - [05/Dec/2022 18:31:03] "GET /json_file_tests/empty.json HTTP/1.1" 200 -
Error : Incompatible or no data in JSON file at URL http://127.0.0.1:8000/json_file_tests/empty.json
PASSED
Disconnection from http://127.0.0.1:8000/

questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_01_load_json_argv_with_simulated_FileNotFound_answer 
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> None, File_Path
Error : File not found at URL http://non-existent-url.com/initial_json_test_file.json
PASSED

questionnaire_unit_test.py::_09_load_json_argv_with_simulated_server::test_02_load_json_argv_with_simulated_success_request_and_fake_data
questionnaire.py http://non-existent-url.com/initial_json_test_file.json -> Json_Data, File_Path
PASSED

=================================================================================== 48 passed, 54 deselected in 6.70s ===================================================================================
```