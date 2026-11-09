import sqlite3

class SQLiteStorage:
    def __init__(self, path= ":memory:"):
        self.conn = sqlite3.connect(path, isolation_level=None)
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
        cursor = self.conn.execute(
                """SELECT name FROM products WHERE id = ?""",
                (product_id,))
        resultado = cursor.fetchone()
        if resultado is None:
            return False
        else:
            return True

    def _insert_product(self, product_id: str, name: str) -> None:
        self.conn.execute(
                """INSERT INTO products (id, name) VALUES (?, ?)""",
                (product_id, name))
        

    def _insert_event(self, product_id: str, event_type: str, quantity: int) -> None:
        self.conn.execute(
                        """INSERT INTO events (product_id, type, quantity) VALUES (?, ?, ?)""",
                        (product_id, event_type, quantity))

    def _begin_write(self) -> None:
        self.conn.execute("BEGIN IMMEDIATE")

    def _commit(self) -> None:
        self.conn.commit()

    def _rollback(self) -> None:
        self.conn.rollback()

    def _calculate_stock(self, product_id: str) -> int:
        cursor = self.conn.execute ("""SELECT COALESCE(SUM(CASE
                                WHEN type = 'IN' THEN quantity
                                ELSE -quantity
                                END), 0)
                                FROM events
                                WHERE product_id = ?""", (product_id,))
        resultado = cursor.fetchone()
        return resultado[0]
        
        