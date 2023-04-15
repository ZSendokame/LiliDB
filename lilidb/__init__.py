"""Small database library
How to use:
    >>> import lilidb
    >>> db = lilidb.Database('filename.json')
    >>> db.set('this is a key', True)
    >>> db.database
    {
        'this is a key': True
    }
    >>> db.get('this is a key')
    True
"""
from .db import Database
