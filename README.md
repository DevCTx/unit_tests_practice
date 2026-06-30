[README.md](./README.md)

# Unit Tests Practice

This repo explores a wide range of testing techniques — mocking, fixtures, test-class inheritance, a simulated HTTP server and continuous integration — using simple multiple-choice quizzes stored as JSON, and compares the automated tests through `unittest` and `pytest`.

It was also my first steps with Markdown documentation.

### Overview
 
| Program | Role |
|---|---|
| `questionnaire.py` | Loads a JSON quiz, displays it in the terminal and counts the score. |
| `questionnaire_import.py` | Downloads quizzes from an online source and converts them to the project [json format](./questionnaire.md#expected-json-schema). |
| `questionnaire_unit_test.py` | Automated test suite for `questionnaire.py`. |
 
The test suite is the heart of the project: it stacks several techniques on a single use case.

---

### Installation

Clone the repository :
```bash
git clone https://github.com/DevCTx/unit_tests_practice
```

Into the cloned folder :
```bash
python -m venv venv
source venv/bin/activate              # Linux / macOS  (venv\Scripts\activate on Windows)
pip install -r requirements.txt       # to use questionnaire.py only
pip install -r requirements-dev.txt   # to use questionnaire_unit_tests.py
```

### Import and convert online quizzes into json_questionnaires
```bash
python3 ./questionnaire_import.py 
```

More info about the original conversion : [questionnaire_import.md](./questionnaire_import.md)

---

### Displays the quiz in argument and counts the number of good answers
```bash
python3 ./questionnaire.py ./json_questionnaires/<questionnaire.json>
```

More info about the JSON format expected and Error messages : [questionnaire.md](./questionnaire.md)

---

### Run the tests with `unittest` or `pytest` 

```bash
python3 -m unittest questionnaire_unit_test
```
```bash
pytest -v questionnaire_unit_test.py -s
```
or use ./json_test_files folder to check 25 intentionally broken quizzes targeting error cases
```bash
python3 questionnaire.py json_test_files/json_00_empty.json
```

More info : [questionnaire_unit_test.md](./questionnaire_unit_test.md)

### Explanation

```load_json_argv()``` is the entry point. It receives ```sys.argv```, validates that there is exactly one ```.json``` argument, detects whether it is a ```URL``` or a local ```file```, and delegates to ```load_json_data_from_URL()``` or ```load_json_data_from_file()```. It always returns a tuple ```(json_data, file_path)```.


### Testing highlights
The objective was to test these various characteristics and methods:

- **Test-class inheritance** to reuse base cases by changing a single parameter.
- **Mocking** with `unittest.mock.patch` to simulate `sys.argv`.
- **Threaded local HTTP server** (`ThreadingMixIn` + `SimpleHTTPRequestHandler`) to test
  remote loading without relying on the internet.
- **`setUp`/`tearDown` (unittest) vs `@pytest.fixture` (pytest)** for the same need, to
  compare both frameworks directly.


### Continuous integration
 
GitHub Actions runs on every push and pull request to `master`: dependency install
(Python 3.10), `flake8` lint, then the test suite under both `unittest` and `pytest`.

---

### [Requirements](./requirements.txt)
- Python 3.10+
- jsonschema==4.17.0
- parameterized==0.8.1
- requests==2.28.1
- validators==0.20.0

### [Requirements-dev](./requirements-dev.txt)
- pytest==8.0.0
- flake8==6.0.0


