import argparse
import json
import os
from typing import Dict, Any


def appendify_dot_json_filename(filename: str) -> str:
    """This function is used to append .json to filename if it doesn't end with .json"""
    return filename if filename.endswith(".json") else f"{filename}.json"


def flatten_json(nested_json: Dict[str, Any]) -> Dict[str, Any]:
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    sniffed_json_keys_as_dict = {}

    def flatten(current_json_value_iteration, name=''):
        if type(current_json_value_iteration) is dict:
            for inner_key in current_json_value_iteration:
                flatten(current_json_value_iteration[inner_key], name + inner_key + '_')
        elif type(current_json_value_iteration) is list:
            check_items_are_object = [isinstance(inner_key, dict) for inner_key in current_json_value_iteration]
            if all(check_items_are_object):
                sniffed_json_keys_as_dict[name[:-1]] = {"tag": "", "description": "", "type": "ARRAY", "required": False}
            else:
                sniffed_json_keys_as_dict[name[:-1]] = {"tag": "", "description": "", "type": "ENUM", "required": False}
        else:
            sniffed_json_keys_as_dict[name[:-1]] = {"tag": "", "description": "", "type": "INTEGER" if isinstance(current_json_value_iteration, int) else "STRING", "required": False}

    flatten(nested_json)
    return sniffed_json_keys_as_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Data2BotJSONSniffer", description="This tool is a solution that reads a json file and sniff the output to another file")
    parser.add_argument("-a", "--input", required=True, type=str, help="Name of file input to read json file from")
    parser.add_argument("-r", "--output", required=True, type=str, help="Name of the file to use to store output of parsed JSON")
    parser.add_argument("-i", "--indent", default=4, type=int, help="Number of indents to use to format the JSON")
    args_as_kwargs = vars(parser.parse_args())
    input_args, output_args, indent_args = args_as_kwargs.pop("input"), args_as_kwargs.pop("output"), args_as_kwargs.pop("indent")
    open_root_directory = "data"
    output_root_directory = "schema"
    with open(appendify_dot_json_filename(f"{open_root_directory}/{input_args}")) as file_name:
        open_json_file_as_dict = json.load(file_name)
    message_attributes = open_json_file_as_dict.get("message")
    json_string = flatten_json(message_attributes)
    with open(appendify_dot_json_filename(f"{output_root_directory}/{output_args}"), "w") as output_file:
        json.dump(json_string, output_file, indent=indent_args)