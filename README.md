# LiliDB
*Lili* ("Small" in Toki Pona) it's a small Key-Value database library.<br>
No third-party dependencies, pure Python and safe to use!<br>

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