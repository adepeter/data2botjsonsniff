import json
import unittest

from data2bot_solution import appendify_dot_json_filename, flatten_json


class TestData2BotSolution(unittest.TestCase):
    def test_flatten_json_function(self):
        expected_input = {
            "name": {
                "first_name": "Peter",
                "last_name": "Seun"
            },
            "age": 10,
            "hobbies": ["coding", "music"]
        }
        expected_result_as_string = '''{
  "age": {
    "description": "",
    "required": false,
    "tag": "",
    "type": "INTEGER"
  },
  "hobbies": {
    "description": "",
    "required": false,
    "tag": "",
    "type": "ENUM"
  },
  "name_first_name": {
    "description": "",
    "required": false,
    "tag": "",
    "type": "STRING"
  },
  "name_last_name": {
    "description": "",
    "required": false,
    "tag": "",
    "type": "STRING"
  }
}
        '''
        expected_result_as_dict = json.loads(expected_result_as_string)
        self.assertEqual(flatten_json(expected_input), expected_result_as_dict)

    def test_dot_json_is_appended_to_file_name(self):
        self.assertEqual(appendify_dot_json_filename("name"), "name.json")

    def test_filename_which_ends_with_dot_json_is_unchanged(self):
        self.assertEqual(appendify_dot_json_filename("hello.json"), "hello.json")


if __name__ == "__main__":
    unittest.main()
