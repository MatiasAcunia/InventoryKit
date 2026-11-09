import sqlite3

class SQLiteStorage:
    def __init__(self, path= ":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL);""")
        self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL REFERENCES products(id),
                    type TEXT NOT NULL CHECK (type IN ('IN', 'OUT')),
                    quantity INTEGER NOT NULL CHECK (quantity > 0));""")
        
    def close(self):
        self.conn.close()

    def _product_exists(self, product_id: str) -> bool:
        raise NotImplementedError

    def _insert_product(self, product_id: str, name: str) -> None:
        raise NotImplementedError

    def _insert_event(self, product_id: str, event_type: str, quantity: int) -> None:
        raise NotImplementedError

    def _begin_write(self) -> None:
        raise NotImplementedError

    def _commit(self) -> None:
        raise NotImplementedError

    def _rollback(self) -> None:
        raise NotImplementedError

    def _calculate_stock(self, product_id: str) -> int:
        raise NotImplementedError