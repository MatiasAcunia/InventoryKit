from .storage import SQLiteStorage
from .exceptions import ProductNotFoundError, ProductAlreadyExistsError, StockLeftError, InsufficientStockError
from .models import Product, InventoryEvent, EventType
import json

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

    def _validate_optional_text(self, value, field:str):
        #Para los campos opcionales: Se asegura que sea None o string, otro tipo es TypeError
        if value is None:
            return None
        if type(value) is not str:
            raise TypeError(f"El valor de {field} debe ser un string o None")
        return value

    def _validate_attributes(self, attributes) -> dict:
        if attributes is None: #No le dieron atributos
            return {}
        if type(attributes) is not dict: #No me dieron un diccionario -> Error.
            raise TypeError("Attributes debe ser un diccionario")
        for key in attributes: #Las claves de los atributos deben ser strings no vacios
            if type(key) is not str:
                raise TypeError("Las claves de los atributos deben ser un string")
            if not key.strip():
                raise ValueError("Las claves de los atributos no pueden estar vacías")
        try: #Vemos si se puede guardar como JSON
            json.dumps(attributes, allow_nan = False)  
        except (TypeError, ValueError):
            raise ValueError("Attributes contiene valores que no se pueden guardar como JSON")
        return attributes
    
    def _require_product(self, product_id: str) -> None:
        resultado = self._storage._get_product(product_id)
        if resultado is None:
            raise ProductNotFoundError(f"El producto de id: {product_id} no existe")

    #Convierte una tupla de la BD a un Product
    def _row_to_product(self, row: tuple) -> Product:
        product_id, name, category, description, attributes_json = row
        attributes = json.loads(attributes_json)
        return Product(product_id, name, category, description, attributes)

    #Convierte una tupla de la bd en un InventoryEvent
    def _row_to_event(self, row: tuple) -> InventoryEvent:
        event_id, product_id, event_type, quantity, timestamp = row
        return InventoryEvent(event_id, product_id, event_type, quantity, timestamp)

    def add(self, id: str, name: str, *, category:str | None = None, description: str | None = None, attributes: dict | None = None) -> Product:
        #Primero validamos todo, así si algo está mal no afecta a la BD
        id = self._validate_text(id, "id")
        name = self._validate_text(name, "name")
        category = self._validate_optional_text(category, "category")
        description = self._validate_optional_text(description, "description")
        attributes = self._validate_attributes(attributes)
        #Ahora si, la escritura en BD
        self._storage._begin_write()
        try:
            if self._storage._product_exists(id):
                raise ProductAlreadyExistsError(f"El id {id!r} ya está en uso")
            self._storage._insert_product(id, name, category, description, attributes)
            self._storage._insert_event(id, EventType.PRODUCT_CREATED, 0) #Cuando lo creamos su cantidad es 0
            self._storage._commit()
        except BaseException:
            #Si hubo un error hay que deshacer lo que quedo hecho a medias
            self._storage._rollback()
            raise
        return Product(id, name, category, description, dict(attributes))         

    def receive(self, id: str, quantity: int) -> InventoryEvent:
        #Registra una entrada de mercadería, validando antes de modificar la BD
        id = self._validate_text(id, "id")
        quantity = self._validate_quantity(quantity)
        self._storage._begin_write()
        try:
            self._require_product(id)
            event_id = self._storage._insert_event(id, EventType.STOCK_RECEIVED, quantity)
            self._storage._commit()
        except BaseException:
                 self._storage._rollback()
                 raise   
        return self._row_to_event(self._storage._get_event(event_id))

    def remove(self, id: str, quantity: int) -> InventoryEvent:
        #Registra una salida de mercadería, validando antes de cambiar la BD
        id = self._validate_text(id, "id")
        quantity = self._validate_quantity(quantity)
        #Hacemos write lock para asegurarnos que no hayan errores
        self._storage._begin_write()
        try:
            self._require_product(id)
            available = self._storage._calculate_stock(id)
            #Si se pide quitar más de lo que hay guardado, se rechaza y hace rollback
            if quantity > available:
                raise InsufficientStockError(
                    f"Stock insuficiente para {id!r}: hay {available} y se pidieron {quantity}")
            event_id = self._storage._insert_event(id, EventType.STOCK_REMOVED, quantity)
            self._storage._commit()
        except BaseException:
            self._storage._rollback()
            raise
        return self._row_to_event(self._storage._get_event(event_id))

    def stock(self, id: str) -> int:
        id = self._validate_text(id, "id")
        res = self._storage._get_product(id)
        if res is None:
            raise ProductNotFoundError("El producto no existe en la base de datos.")  
        return self._storage._calculate_stock(id)

    def get(self, id: str) -> Product:
        id = self._validate_text(id, "id")
        #El get solo devuelve productos activos
        row = self._storage._get_product(id)
        if row is None: #No existe en la BD un producto con ese id
            raise ProductNotFoundError(f"El producto de id: {id} no existe")
        return self._row_to_product(row)

    def list_products(self) -> list[Product]:
        #Trae todas las filas de la BD ordenadas por id
        rows = self._storage._list_products()
        products = []
        for row in rows:
            products.append(self._row_to_product(row))
        return products

    def delete(self, id: str) -> InventoryEvent:
        id = self._validate_text(id, "id")
        self._storage._begin_write()
        res = self._storage._get_product(id)
        try:
            self._require_product(id)
            if self._storage._calculate_stock(id) > 0:
                        raise StockLeftError(f"El producto {id!r} todavía tiene stock")
            self._storage._deactivate_product(id)
            event_id = self._storage._insert_event(id, EventType.PRODUCT_DELETED, 0)
            self._storage._commit()
        except BaseException:
            self._storage._rollback()
            raise
        return self._row_to_event(self._storage._get_event(event_id))

                   
    def history(self, id: str) -> list[InventoryEvent]:
        id = self._validate_text(id, "id")
        if not self._storage._product_exists(id):
                    raise ProductNotFoundError(f"El producto de id: {id} nunca existió")  
        rows = self._storage._get_history(id)
        events = []
        for row in rows:
            events.append(self._row_to_event(row))
        return events

    def close(self) -> None:
        self._storage.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()