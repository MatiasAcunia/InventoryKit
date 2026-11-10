import sqlite3
import json
from typing import Any

class SQLiteStorage:
    def __init__(self, path= ":memory:"):
        self.conn = sqlite3.connect(path, isolation_level=None)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    active INT DEFAULT 1 CHECK(active IN (0, 1)),
                    category TEXT,
                    description TEXT,
                    attributes TEXT;""")
        self.conn.execute(
                    """CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL REFERENCES products(id),
                    type TEXT NOT NULL CHECK (type IN ('IN', 'OUT')),
                    quantity INTEGER NOT NULL CHECK (quantity > 0)
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);""")
        
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

    def _insert_product(self, product_id: str, name: str, category: str | None = None, description: str | None = None, attributes: dict[str, Any] | None = None) -> None:
        attributes_json = json.dumps(attributes) if attributes is not None else None
        self.conn.execute("""
                    INSERT INTO products (id, name, category, description, attributes)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (product_id, name, category, description, attributes_json))
        

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
                                WHERE product_id = ?);""", (product_id,))
        resultado = cursor.fetchone()
        return resultado[0]

    def _get_product(self, product_id: str) -> tuple[str, str, str | None, str | None, str | None] | None:
        cursor = self.conn.execute("""SELECT id, name, category, description, attributes
                                    FROM products
                                    WHERE id = ?
                                    AND active = 1;""", (product_id,))
        resultado = cursor.fetchone()
        return resultado

    def _list_products(self) -> list[tuple[str, str, str | None, str | None, str | None]]:
        cursor = self.conn.execute("""SELECT id, name, category, description, attributes
                                    FROM products
                                    WHERE active = 1
                                    ORDER BY id;""")
        resultado = cursor.fetchall()
        return resultado

    def _get_history(self, product_id: str) -> list[tuple[int, str, str, int, str]]:
        cursor = self.conn.execute("""SELECT id, product_id, type, quantity, timestamp
                                    FROM events
                                    WHERE id = ?
                                    ORDER BY id;""", (product_id,))
        resultado = cursor.fetchall()
        return resultado

    def _deactivate_product(self, product_id: str) -> int:
        cursor = self.conn.execute("""UPDATE products
                                    SET active = 0
                                    WHERE id = ?
                                    AND active = 1;""", 
                                    (product_id,))
        return cursor.rowcount()


    def _activate_product(self, product_id: str) -> int:
        cursor = self.conn.execute("""UPDATE products
                                    SET active = 1
                                    WHERE id = ?
                                    AND active = 0;""", 
                                    (product_id,))
        return cursor.rowcount()
            
        

            
            