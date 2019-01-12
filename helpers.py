# -*- coding: utf-8 -*-
"""
TenantBase Backend
Helper classes for main.py

class KeyValueHelper()
helper class for sqlite3 interaction.

class Color()
helper class for formatting terminal colors
"""

import sqlite3
from collections import MutableMapping as DictMixin

class KeyValueHelper(DictMixin):
    """Sqlite3 helper class. Allows for easy interaction with sqlite db"""

    def __init__(self, filename=None):
        self.conn = sqlite3.connect(filename)
        self.conn.execute("CREATE TABLE IF NOT EXISTS key_value (key text unique, value text)")
        self.c = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def __len__(self):
        self.c.execute('SELECT COUNT(*) FROM key_value')
        rows = self.c.fetchone()[0]
        return rows if rows is not None else 0

    def iterkeys(self):
        c1 = self.conn.cursor()
        for row in c1.execute('SELECT key FROM key_value'):
            yield row[0]

    def itervalues(self):
        c2 = self.conn.cursor()
        for row in c2.execute('SELECT value FROM key_value'):
            yield row[0]

    def iteritems(self):
        c3 = self.conn.cursor()
        for row in c3.execute('SELECT key, value FROM key_value'):
            yield row[0], row[1]

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def __contains__(self, key):
        self.c.execute('SELECT 1 FROM key_value WHERE key = ?', (key,))
        return self.c.fetchone() is not None

    def __getitem__(self, key):
        self.c.execute('SELECT value FROM key_value WHERE key = ?', (key,))
        item = self.c.fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        self.c.execute('REPLACE INTO key_value (key, value) VALUES (?,?)', (key, value))
        self.conn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        self.c.execute('DELETE FROM key_value WHERE key = ?', (key,))
        self.conn.commit()

    def __iter__(self):
        return self.iteritems()

class Color_Helper:
    """
    Data class containing escape codes to modify text properties. To use, place
    modifier before text you wish to modify, and the end code after. Escape
    codes can be stacked.
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
