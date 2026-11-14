#Pruebas automáticas de persistencia (la BD)
import os
import tempfile
import unittest
from inventorykit import Inventory, ProductAlreadyExistsError, ProductNotFoundError

class TestPersitence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory() #Para que no queden los archivos en disco los hacemos temporal
        self.path = os.path.join(self.tmp.name, "test.db")

    def tearDown(self):
        self.tmp.cleanup() #Borramos la carpeta temporal y todo lo que tenga

    def test_data_survives_close_and_reopen(self):
        with Inventory(self.path) as inv:
            inv.add("TOR-001", "Tornillos", category = "Ferretería", attributes={"location": "B15", "brand": "Genérica"})
            inv.receive("TOR-001", 100)
            inv.remove("TOR-001", 25)
        #El with cierra la conexión al terminar, la reabrimos (sobre el mismo archivo):
        with Inventory(self.path) as inv:
            producto = inv.get("TOR-001")
            self.assertEqual(producto.name, "Tornillos")
            self.assertEqual(producto.category, "Ferretería")
            self.assertEqual(producto.attributes, {"location": "B15", "brand": "Genérica"})
            self.assertEqual(inv.stock("TOR-001"), 75)
            self.assertEqual(len(inv.history("TOR-001")), 3) #add, receive, remove

    def test_history_order_survives_reopen(self):
        with Inventory(self.path) as inv:
            inv.add("TOR-001", "Tornillos")
            inv.receive("TOR-001", 100)
            inv.remove("TOR-001", 25)
        #Cerramos y reabrimos
        with Inventory(self.path) as inv:
            tipos_eventos = [evento.type for evento in inv.history("TOR-001")]
            self.assertEqual(tipos_eventos, ["PRODUCT_CREATED", "STOCK_RECEIVED", "STOCK_REMOVED"])

    def test_deleted_product_stays_deleted_after_reopen(self):
        with Inventory(self.path) as inv:
            inv.add("TOR-001", "Tornillos")
            inv.delete("TOR-001")
        #Cierro abro
        with Inventory(self.path) as inv:
            with self.assertRaises(ProductNotFoundError):
                inv.get("TOR-001")
            self.assertEqual(len(inv.history("TOR-001")), 2) #add y delete
            with self.assertRaises(ProductAlreadyExistsError):
                inv.add("TOR-001", "Tornillos 2")

    def test_reopening_does_not_duplicate_nor_lose_tables(self):
        with Inventory(self.path) as inv:
            inv.add("TOR-001", "Tornillos")
        for i in range(3):
            with Inventory(self.path):
                pass
        #Abri y cerre varias veces
        with Inventory(self.path) as inv:
            self.assertEqual(len(inv.list_products()), 1)

    def test_in_memory_inventores_are_independent(self):
        #Probamos que cada instancia de Inventory() tiene su propia base vacía
        with Inventory() as inv1, Inventory() as inv2:
            inv1.add("TOR-001", "Tornillos")
            self.assertEqual(inv2.list_products(), [])

if __name__ == "__main__":
    unittest.main()
