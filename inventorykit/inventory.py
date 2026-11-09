from .storage import SQLiteStorage

class Inventory:
    def __init__(self, path = ":memory:"):
        self._storage = SQLiteStorage(path)