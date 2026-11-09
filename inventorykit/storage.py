import sqlite3

class SQLiteStorage:
    def __init__(self, path= ":memory:"):
        self.coneccion = sqlite3.connect(path)
