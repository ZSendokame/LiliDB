import os
import json
import traceback
from io import TextIOWrapper


def database(path: TextIOWrapper) -> dict:
    if os.path.getsize(path) == 0:
        return {}

    with open(path, 'r') as file:
        return json.load(file)


def error(type, message, trace) -> None:
    print(''.join(traceback.format_tb(trace)))
    print(f'{type}: {message}')