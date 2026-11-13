#Convierte la carpeta (inventorykit) en un paquete y decide que se puede importar
from .inventory import Inventory
from .models import Product, InventoryEvent, EventType
from .exceptions import (ProductAlreadyExistsError, ProductNotFoundError, InsufficientStockError, StockLeftError)

#Permite que el usuario haga: from inventorykit import Inventory , en vez de: from inventorykit.inventory import Inventory , por ejemplo.