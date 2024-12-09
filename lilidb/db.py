import sys
import json
import threading
from typing import Any, Callable

from . import utils


class Database:
    """Database class
    The ``Database`` class handles a JSON file and a dictionary, the JSON content converted.
    """
    def __init__(self, path: str):
        self.__lock__ = threading.Lock()
        self.name = path
        self.database = utils.database(path)
        sys.excepthook = self.__failure__

    def __failure__(self, type, message, trace):
        with open(self.name, 'w') as file:
            file.write('')
            self.dump()

        utils.error(type, message, trace)

    def __enter__(self):
        return self

    def __exit__(self, type, message, traceback):
        self.dump()

    def __len__(self) -> int:
        return len(self.database)

    def set(self, key: str, value: Any) -> None:
        """Set a new key
        :param key: Key to create
        :param value: The Key value
        """
        with self.__lock__:
            self.database[key] = value

        return None

    def get(self, key: str, default: Any = None) -> (Any | None):
        """Get a existing key
        :param key: Key to retrieve
        :param default: (Optional) A default value to return in case the key does not exists
        """
        return self.database.get(key, default)

    def remove(self, key: str) -> Any:
        """Remove a key
        :param key: Key to remove
        """
        return self.database.pop(key)

    def rename(self, key: str, new: str) -> None:
        """Rename a Key
        :param key: Old key to replace
        :param new: New name
        """
        self.database[new] = self.database.pop(key)

        return None

    def update(self, data: dict) -> int:
        """Merge database with data
        :param data: Data to merge with
        """
        self.database.update(data)

        return len(self)

    def query(self, func: Callable) -> list[tuple]:
        """Filter objects using a callable object
        :param func: Callable object with two parameters (key and value), that returns a bool
        """
        return {
            key: value
            for key, value in self.database.items()
            if func(key, value)
        }

    def clear(self) -> None:
        """Delete the entire database dictionary"""
        self.database.clear()

        return None

    def dump(self) -> None:
        """Save the database to a file
        :param filename: (Optional) File to save
        """
        with self.__lock__:
            with open(self.name, 'w') as file:
                json.dump(self.database, file, indent=4)

        return None
