#Este ejemplo se comporta como si fuera un proyecto externo: Solo importa la biblioteca ya instalada (la que crea el pyproject.toml)
#Es para mostrar como se usaria, y que funciona sin tener que usar archivos internos ni SQL

from pathlib import Path
from inventorykit import Inventory, InsufficientStockError

#Empezamos con una base nueva
DB = Path("demo_negocio.db")
DB.unlink(missing_ok=True)

with Inventory(DB) as inv:
    inv.add("TOR-001", "Tornillos", category="Ferretería", attributes={"location": "B15", "brand": "Genéricos"})
    inv.add("MAR-001", "Martillo", attributes={"location": "A02"})
    inv.receive("TOR-001", 100)
    inv.remove("TOR-001", 25)
    print("Stock de tornillos:", inv.stock("TOR-001")) #Da 75

    #Manejo de error: Una salida mayor al stock falla y no modifica la BD
    try:
        inv.remove("TOR-001", 500)
    except InsufficientStockError as error:
        print("Error esperado:", error)
    print("Historial:")
    for evento in inv.history("TOR-001"):
        print(" ", evento)

    #Ejemplo: Se puede filtrar con Python normal sobre la lista de productos en el inventario
    en_b15 = [p for p in inv.list_products() if p.attributes.get("location") == "B15"]
    print("En la ubicación B15:", en_b15)

#Volvemos a abrir el mismo archivo, para mostrar la persistencia de datos luego de cerrarlo
with Inventory(DB) as inv:
    print("Tras reabrir, stock:", inv.stock("TOR-001"))

DB.unlink()