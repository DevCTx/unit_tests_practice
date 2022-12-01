import json
import jsonschema
from jsonschema.validators import validate


#Great documentations at https://json-schema.org/understanding-json-schema/reference/array.html#additional-items

# "prefixItems" verifies that the type of the current position is the same as defined,
# "items":False controls that nothing more is added (= "additional-items" previously draft/2020-12)

schema = {
    "$schema": "http://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": [ "categorie", "titre", "questions", "difficulte"],
    "properties": {
        "categorie": {"type": "string"},
        "titre": {"type": "string"},
        "questions": {
            "type": "array",
            "default": [],
            "items": {
                "type": "object",
                "properties": {
                    "titre": {"type": "string"},
                    "choix": {
                        "type": "array",
                        "minItems": 2,
                        "items": {
                            "type": "array",
                            "minItems": 2,
                            "prefixItems": [{"type": "string"}, {"type": "boolean"}],
                            "items": False
                        }
                    }
                }
            }
        }
    }
}

jsondata_test = '{' \
       '"categorie":"TEST",' \
       '"titre":"Question Test",' \
       '"questions":[' \
       '    {"titre":"This is a question ?",' \
       '    "choix":[["Answer 1",true],["Answer 2",false],["Answer 3",false],["Answer 4",false]]},' \
       '    {"titre":"This is another question ?",' \
       '    "choix":[["Answer 5",true],["Answer 6",false],["Answer 7",false],["Answer 8",false]]}' \
       '],' \
       '"difficulte":"intermediaire"' \
       '}'


def validate_json_syntax(d):
    try:
        return json.loads(d)
    except ValueError:
        print('DEBUG: JSON data contains an error')
        return None


json_data = validate_json_syntax(jsondata_test)

if json_data:
    #output will be None
    try:
        validate(json_data, schema)
        print('ok')
    except jsonschema.exceptions.ValidationError:
        print("Schema JSON incorrect")
