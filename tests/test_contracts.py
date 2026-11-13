#Pruebas automáticas de las operaciones de Inventory
import unittest
from inventorykit import (Inventory, ProductAlreadyExistsError, ProductNotFoundError, InsufficientStockError, StockLeftError)

class TestInventory(unittest.TestCase):
    def setUp(self):
        #Vamos a crear un inventario nuevo en cada prueba asi son independientes
        self.inv = Inventory()

    def tearDown(self):
        self.inv.close()

    def test_new_product_has_zero_stock(self):
        self.inv.add("TOR-001", "Tornillos")
        self.assertEqual(self.inv.stock("TOR-001"), 0)

    def test_receive_and_remove_update_stock(self):
        self.inv.add("TOR-001", "Tornillos")
        self.inv.receive("TOR-001", 100)
        self.inv.remove("TOR-001", 25)
        self.assertEqual(self.inv.stock("TOR-001"), 75)

    def test_add_duplicate_id_fails(self):
        self.inv.add("TOR-001", "Tornillos")
        with self.assertRaises(ProductAlreadyExistsError):
            self.inv.add("TOR-001", "Tornillos mejores")

    def test_remove_more_than_stock_fails_and_changes_nothing(self):
        self.inv.add("TOR-001", "Tornillos")
        self.inv.receive("TOR-001", 10)
        with self.assertRaises(InsufficientStockError):
            self.inv.remove("TOR-001", 11)
        #Luego del error, no debe cambiar ni el stock ni el historial, chequeamos:
        self.assertEqual(self.inv.stock("TOR-001"), 10)
        self.assertEqual(len(self.inv.history("TOR-001")), 2) #El add y el receive

    def test_invalid_quantities_are_rejected(self):
        self.inv.add("TOR-001", "Tornillos")
        casos = [(0, ValueError), (-5, ValueError), (2.5, TypeError), (True, TypeError), ("10", TypeError)]
        #Debe ser un int >0 lo que se le pasa en receive
        for cantidad, tipo_error in casos:
            with self.subTest(cantidad = cantidad):
                with self.assertRaises(tipo_error):
                    self.inv.receive("TOR-001", cantidad)

    def test_delete_requires_zero_stock(self):
        self.inv.add("TOR-001", "Tornillos")
        self.inv.receive("TOR-001", 5)
        with self.assertRaises(StockLeftError):
            self.inv.delete("TOR-001")

    def test_deleted_product_is_hidden_but_keeps_in_history(self):
        self.inv.add("TOR-001", "Tornillos")
        self.inv.delete("TOR-001")
        with self.assertRaises(ProductNotFoundError):
            self.inv.get("TOR-001")
        self.assertEqual(self.inv.list_products(), []) #No tengo productos
        self.assertEqual(len(self.inv.history("TOR-001")), 2) #Aunque elimine los productos conservo su historial (add y delete)
        with self.assertRaises(ProductAlreadyExistsError):
            self.inv.add("TOR-001", "Nuevos tornillos") #Aunque elimine el TOR-001, el id sigue inválido para siempre

if __name__ == "__main__":
    unittest.main()