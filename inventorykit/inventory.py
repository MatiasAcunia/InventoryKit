from .storage import SQLiteStorage
from .exceptions import ProductNotFoundError

class Inventory:
    def __init__(self, path = ":memory:"):
        self._storage = SQLiteStorage(path)

    def _validate_text(self, value: str, field: str) -> str:
        if type(value) is not str:
            raise TypeError(f"El valor de {field} no es/son strings")
        if not value.strip():
            raise ValueError(f"El valor de {field} es/son campos vacios")
        if value != value.strip():
            raise ValueError(f"El valor de {field} tiene/tienen espacio/s al inicio o final")
        return value

        
    def _validate_quantity(self, quantity: int) -> int:
         if type(quantity) is not int:
             raise TypeError("La cantidad no es de tipo int")
         if quantity <= 0:
             raise ValueError("La cantidad es igual o menor a 0")
         return quantity
    
    def _require_product(self, product_id: str) -> None:
        resultado = self._storage._get_product(product_id)
        if resultado is None:
            raise ProductNotFoundError(f"El producto de id: {product_id} no existe")

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
