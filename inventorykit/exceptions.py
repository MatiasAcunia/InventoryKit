#Errores propios de la biblioteca.

#Se lanza en add() si el ID dado ya fue usado
class ProductAlreadyExistsError(ValueError):
    pass

#Se lanza si no existe un producto activo con el ID dado
class ProductNotFoundError(LookupError):
    pass

#Se lanza en remove() si se intenta sacar más unidades de las que hay
class InsufficientStockError(ValueError):
    pass