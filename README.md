# LiliDB
*Lili* ("Small" in Toki Pona), uses JSON to storage key-value databases.<br>
*Fail-safe* and *Thread-Safe* key-value database.

# Install
```sh
# GIT+PIP
pip install git+https://github.com/ZSendokame/LiliDB.git

# PIP
pip install LiliDB
```

# How to use
```py
import lilidb

db = lilidb.Database('database.json')

db.set('key', 'value')
db.dump()

with db as db:
    db.set('with': 'Open, save and close file.')

# You can use Threads!
# and make errors... If an exception ocurrs, it automatically saves.
```