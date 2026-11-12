#Clases que le presentamos al usuario (Product, InventoryEvent)

#Los tipos de evento como constante
class EventType:
    PRODUCT_CREATED = "PRODUCT_CREATED"
    PRODUCT_DELETED = "PRODUCT_DELETED"
    PRODUCT_REACTIVATED = "PRODUCT_REACTIVATED"
    STOCK_RECEIVED = "STOCK_RECEIVED"
    STOCK_REMOVED = "STOCK_REMOVED"

class Product:
    def __init__(self, id, name, category = None, description = None, attributes = None):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        if attributes is None:
            self.attributes = {} #Creo un diccionario vacio
        else:
            self.attributes = attributes

    #Como se ve Product al hacer print()
    def __repr__(self):
        return (f"Product(id={self.id!r}, name={self.name!r}, category={self.category!r}, "
                f"description={self.description!r}, attributes={self.attributes!r})")
        #El !r le dice a python que muestre el texto como repr() y no como str()

    #Define cuando 2 Product son iguales (todos los datos coinciden)
    def __eq__(self, other):
        if not isinstance(other, Product): #Si lo que me dan NO es un producto
            return NotImplemented #Prueba a hacer el eq al reves (other en lugar de self y viceversa), si tambien da NotImplemented, retorna False
            #Podriamos poner directamente return false para este trabajo (creo)
        return (self.id == other.id and self.name == other.name and self.category == other.category and self.description == other.description 
                and self.attributes == other.attributes)

class InventoryEvent:
    def __init__(self, id, product_id, type, quantity, timestamp):
        self.id = id
        self.product_id = product_id
        self.type = type
        self.quantity = quantity
        self.timestamp = timestamp

    def __repr__(self):
        return (f"InventoryEvent(id={self.id!r}, product_id={self.product_id!r}, "
                f"type={self.type!r}, quantity={self.quantity!r}, timestamp={self.timestamp!r})")

    def __eq__(self, other):
        if not isinstance(other, InventoryEvent):
            return NotImplemented
        return (self.id == other.id and self.product_id == other.product_id and self.type == other.type and self.quantity == other.quantity
                and self.timestamp == other.timestamp)