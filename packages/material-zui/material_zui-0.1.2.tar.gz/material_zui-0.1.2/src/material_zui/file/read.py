from collections import defaultdict
import json
from typing import DefaultDict
from pyparsing import Any

from material_zui.string import remove_all
from material_zui.utility import pipe_list


def read_file_to_list(filename: str) -> list[str]:
    with open(filename, "r") as f:
        lines = f.readlines()
    return pipe_list(remove_all('\n'))(lines)


def load_json_object(json_file_path: str) -> DefaultDict[str, str]:
    '''
    Load json file data to dict type
    @json_file_path: json file path
    @return: dict json data
    '''
    with open(json_file_path, encoding='utf-8') as json_data:
        return defaultdict(str, json.load(json_data))


def load_json_array(json_file_path: str) -> list[dict[Any, Any]]:
    '''
    Load json file data to list type
    @json_file_path: json file path
    @return: list json data
    '''
    with open(json_file_path, "r") as f:
        data = json.load(f)
    return list(data)


def read_json(json_file_path: str):
    return json.loads(open(json_file_path, encoding="utf-8").read())
