import sys
import traceback
import os
import hashlib
import json
import threading
from typing import Any, Callable


class Database:
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

    def set(self, key: str, value: Any, algo: str = None) -> None:
        if algo is not None and algo in hashlib.algorithms_available:
            algo = hashlib.__getattribute__(algo)
            value = algo(bytes(value, 'utf-8')).hexdigest()

        with self.__lock__:
            self.database[key] = value

        return None

    def get(self, key: str) -> Any:
        if self.exists(key):
            return self.database[key]

        return None

    def remove(self, key: str) -> Any:
        return self.database.pop(key)

    def rename(self, key: str, new: str) -> None:
        self.database[new] = self.database.pop(key)

        return None

    def query(self, func: Callable) -> list[tuple]:
        return [
            (key, value)
            for key, value in self.database.items()
            if func(key, value)
        ]

    def exists(self, key: str) -> bool:
        return key in self.database

    def clear(self) -> None:
        self.database.clear()

        return None

    def close(self) -> None:
        self.file.close()

        return None

    def length(self, key: str = None) -> int:
        if key is not None and self.exists(key):
            return len(self.get(key))

        return len(self.database)

    def dump(self, filename: str = None) -> None:
        self.__dumping__ = True

        if filename is not None:
            mode = 'r' if os.path.exists(filename) else 'x'
            self.file = open(filename, mode=mode)

        with self.__lock__:
            with open(self.file.name, 'w') as file:
                json.dump(self.database, file, indent=4)

        self.__dumping__ = False

        return None
