from storage import SQLiteStorage

class Inventory:
    def __init__(self, path = ":memory:"):
        self._storage = SQLiteStorage(path)

    def _validate_text(self, value: str, field: str) -> str:
        raise NotImplementedError

    def _validate_quantity(self, quantity: int) -> int:
        raise NotImplementedError

    def _require_product(self, product_id: str) -> None:
        raise NotImplementedError

    def add(self, id: str, name: str) -> None:
        raise NotImplementedError

    def receive(self, id: str, quantity: int) -> None:
        raise NotImplementedError

    def stock(self, id: str) -> int:
        raise NotImplementedError

    def remove(self, id: str, quantity: int) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
