import sys
import traceback
import os
import hashlib
import json
import threading
from typing import Any, Callable


class Database:
    """Database class
    The ``Database`` class handles a JSON file and a dictionary, the JSON content converted.
    """
    def __init__(self, database: str):
        self.__dumping__ = False
        self.__lock__ = threading.Lock()
        self.name = database
        self.file = open(database, 'r')
        self.database = (
            {} if os.path.getsize(database) == 0
            else json.load(self.file)
        )
        sys.excepthook = self.__failure__

        self.file.close()

    def __failure__(self, type, message, trace):
        if self.__dumping__:
            with open(self.file.name, 'w') as file:
                file.write('')
                self.dump()

        self.close()
        print(''.join(traceback.format_tb(trace)))
        print(f'{type}: {message}')

    def __enter__(self):
        return self

    def __exit__(self, type, message, traceback):
        self.close()
        self.dump()

    def __len__(self) -> int:
        return len(self.database)

    def set(self, key: str, value: Any, algo: str = None) -> None:
        """Set a new key
        :param key: Key to create
        :param value: The Key value
        :param algo: (Optional) Hashing algorithm to encrypt the key
        """

        if algo is not None and algo in hashlib.algorithms_available:
            algo = hashlib.__getattribute__(algo)
            value = algo(bytes(value, 'utf-8')).hexdigest()

        with self.__lock__:
            self.database[key] = value

        return None

    def get(self, key: str, default: Any = None, type: None = None) -> (Any | None):
        """Get a existing key
        :param key: Key to retrieve
        :param default: (Optional) A default value to return in case the key does not exists
        :param type: (Optional) Convert the key type into the selected
        """

        value = self.database.get(key, default)

        return value if type is None else type(value)

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
        return [
            (key, value)
            for key, value in self.database.items()
            if func(key, value)
        ]

    def exists(self, key: str) -> bool:
        """Check if a key exists
        :param key: Key to check
        """
        return key in self.database

    def clear(self) -> None:
        """Delete the entire database dictionary"""
        self.database.clear()

        return None

    def close(self) -> None:
        self.file.close()

        return None

    def dump(self, filename: str = None) -> None:
        """Save the database to a file
        :param filename: (Optional) File to save
        """
        self.__dumping__ = True

        with self.__lock__:
            file = self.file.name if filename is None else filename

            with open(file, 'w') as file:
                json.dump(self.database, file, indent=4)

        self.__dumping__ = False

        return None
