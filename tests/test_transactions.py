#Pruebas automáticas de las transacciones (Si algo falla a mitad de la operación, NO debe quedar en la BD)
import os
import sqlite3
import tempfile
import threading
import unittest
from unittest import mock
from inventorykit import Inventory, ProductNotFoundError, InsufficientStockError

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()

    def tearDown(self):
        self.inv.close()

    def test_add_rolls_back_if_event_insert_fails(self):
        with mock.patch.object(self.inv._storage, "_insert_event", side_effect = RuntimeError("fallo simulado")):
        #Lo que hace el mock.patch.object es reemplazar _insert_event por un error solo dentro del bloque with
        #Asi simulamos que falla el add
            with self.assertRaises(RuntimeError):
                self.inv.add("TOR-001", "Tornillos")
        self.assertEqual(self.inv.list_products(), []) #Hubo rollback por el mock, no se guardaron los TOR-001
        with self.assertRaises(ProductNotFoundError):
            self.inv.history("TOR-001")
        #Como no se crearon el id está libre, puedo crearlos:
        self.inv.add("TOR-001", "Tornillos")
        self.assertEqual(len(self.inv.history("TOR-001")), 1) #add

    def test_deleted_rolls_back_if_event_insert_fails(self):
        self.inv.add("TOR-001", "Tornillos")
        with mock.patch.object(self.inv._storage, "_insert_event", side_effect = RuntimeError("Fallo simulado")):
            with self.assertRaises(RuntimeError):
                self.inv.delete("TOR-001")
        #No se pudo eliminar TOR-001, sigue activo
        self.assertEqual(self.inv.get("TOR-001").name, "Tornillos")
        self.assertEqual(len(self.inv.history("TOR-001")), 1) #add

#Pruebas con 2 o más conexiones al mismo archivo
class TestConcurrency(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "test.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_second_writer_cannot_start_while_first_holds_the_lock(self):
        #Si hay un write lock, otro no puede hacer nada basicamente
        with Inventory(self.path) as inv1, Inventory(self.path) as inv2:
            inv1.add("TOR-001", "Tornillos")
            inv1.receive("TOR-001", 10)
            #Bajamos el tiempo de espera de inv2 a 100 ms (el default es 5 segundos, demoran una vida los test)
            inv2._storage.conn.execute("PRAGMA busy_timeout = 100") 
            inv1._storage._begin_write() #inv1 hace el writelock
            try:
                #inv2 intenta escribir pero no puede por el lock de inv1
                with self.assertRaises(sqlite3.OperationalError): #Notar que el error es de sqllite3, no nuestro
                    inv2.remove("TOR-001", 5)
            finally:
                inv1._storage._rollback() #Saca el writelock de inv1
            #El intento fallido no afecto a mi stock:
            self.assertEqual(inv2.stock("TOR-001"), 10)
            #Y ahora si puedo eliminar que no esta el writelock
            inv2.remove("TOR-001", 5)
            self.assertEqual(inv2.stock("TOR-001"), 5)

    def test_concurrent_removes_never_oversell(self):
        with Inventory(self.path) as inv:
            inv.add("TOR-001", "Tornillos")
            inv.receive("TOR-001", 10)
        threads_count = 5
        #Me creo 5 hilos, en cada uno voy a pedir 3 unidades, como solo tengo 10, solamente 3 pueden tener exito
        #El barrier hace que todos empiecen a la vez
        barrier = threading.Barrier(threads_count)
        res = []

        def worker():
            #Cada hilo abre su propia conexión
            with Inventory(self.path) as inv:
                barrier.wait()
                try:
                    inv.remove("TOR-001", 3)
                    res.append("ok")
                except InsufficientStockError:
                    res.append("insufficient")
                except Exception as error:
                    #No deberia pasar esto, otro tipo de error
                    #pero si llega a pasar y no esta explota el test
                    res.append(f"Error: {error!r}")

        threads = [threading.Thread(target = worker) for _ in range(threads_count)]
        for thread in threads:
            thread.start()
        for thread in threads:
            #El join espera a que el hilo termine, el timeout es por si falló que no se cuelge la prueba
            thread.join(timeout = 30) 
        self.assertEqual(sorted(res), ["insufficient", "insufficient", "ok", "ok", "ok"])
        with Inventory(self.path) as inv:
            #Me deberia quedar 1 tornillo aun
            self.assertEqual(inv.stock("TOR-001"), 1)
            self.assertEqual(len(inv.history("TOR-001")), 5)# add receive remove remove remove

if __name__ == "__main__":
    unittest.main()