[README.md](./README.md)

# Unit Tests Practice

<<<<<<< HEAD
This repo explores a wide range of testing techniques — mocking, fixtures, test-class inheritance, a simulated HTTP server and continuous integration — using simple multiple-choice quizzes stored as JSON, and compares the automated tests through `unittest` and `pytest`.
=======
This repo explores a wide range of testing techniques 
— mocking, fixtures, test-class inheritance, a simulated HTTP server and continuous integration — 
using simple multiple-choice quizzes stored as JSON, and compares the automated tests through unittest and pytest.
>>>>>>> a94885a091e1ba526cedbcafdef488142a86d952

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
 
```bash
python -m venv venv
source venv/bin/activate              # Linux / macOS  (venv\Scripts\activate on Windows)
pip install -r requirements.txt       # to use questionnaire.py only
pip install -r requirements-dev.txt   # to use questionnaire_unit_tests.py
```

### Import and convert online quizzes into json_questionnaires
>python3 ./questionnaire_import.py 

More info : [questionnaire_import.md](./questionnaire_import.md)

---

### Displays the quiz in argument and counts the number of good answers
>python3 ./questionnaire.py ./json_questionnaires/<questionnaire.json>

More info : [questionnaire.md](./questionnaire.md)

---

### Run the tests with `unittest` or `pytest` 
use ./json_test_files folder to check 25 intentionally broken quizzes targeting error cases
>python3 -m unittest questionnaire_unit_test.py ./json_test_files/<questionnaire.json>
>pytest -v questionnaire_unit_test.py -s ./json_test_files/<questionnaire.json>

More info : [questionnaire_unit_test.md](./questionnaire_unit_test.md)


### Testing highlights
 
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
- pytest==7.2.0
- flake8==6.0.0


