#Un programa de ejemplo que usa inventory kit
#La gracia: La lógica se encarga casi todo inventory kit, este archivo solo hace la parte "visual"

from pathlib import Path #Simplemente para guardar la bd junto al main.py
import os #Para imprimir lindo
from inventorykit import (Inventory, EventType, ProductAlreadyExistsError, ProductNotFoundError, InsufficientStockError, StockLeftError)

DB = Path(__file__).parent / "ferreteria.db"

# ---------- Funciones visuales ----------

AZUL = "\033[94m"
ROJO = "\033[91m"
RESET = "\033[0m"

def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_titulo_menu():
    texto = "Menú"
    ancho = max(len(opcion[0]) for opcion in OPCIONES.values()) + 6
    linea = "=" * ancho

    print(f"{AZUL}{linea}{RESET}")
    print(f"{AZUL}{texto.center(ancho)}{RESET}")
    print(f"{AZUL}{linea}{RESET}")


def mostrar_opcion(numero, texto):
    color = ROJO if numero == "0" else AZUL
    print(f"{color}[{numero}]{RESET} {texto}")

#La biblioteca devuelve los tipos de evento en inglés; este diccionario los traduce para mostrarlos en el historial.
NOMBRES_EVENTO = {
    EventType.PRODUCT_CREATED: "Producto creado",
    EventType.PRODUCT_DELETED: "Producto eliminado",
    EventType.STOCK_RECEIVED: "Entrada de stock",
    EventType.STOCK_REMOVED: "Salida de stock",
}

#EXP: Datos para la opción 9
DATOS_DE_PRUEBA = [
    ("TOR-001", "Tornillos 3 pulgadas (caja x100)", "Fijaciones", "B15", 40, 12),
    ("CLA-001", "Clavos 2 pulgadas (1 kg)", "Fijaciones", "B16", 25, 5),
    ("MAR-001", "Martillo de carpintero", "Herramientas", "A02", 10, 3),
    ("DES-001", "Destornillador Phillips", "Herramientas", "A03", 15, 15),
    ("PIN-001", "Pintura blanca 4 L", "Pinturas", "C01", 8, 2),
]

# ---------- Funciones para pedir datos ----------

def pedir_texto(mensaje):
    return input(mensaje).strip()


def pedir_opcional(mensaje):
    #Pide un dato opcional: si el usuario aprieta Enter sin escribir nada, devuelve None.
    texto = input(f"{mensaje} (opcional, Enter para omitir): ").strip()
    if texto == "":
        return None
    return texto


def pedir_entero(mensaje):
    texto = input(mensaje).strip()
    try:
        return int(texto)
    except ValueError:
        print("Debe ingresar un número entero.")
        return None


# ---------- Una función por cada opción del menú ----------

#Cada función recibe el inventario abierto (inv) y hace tres cosas: pedir datos, llamar a UNA operación de InventoryKit y mostrar el resultado.
#Los errores no se manejan acá: los atrapa la función ejecutar(), más abajo.

def opcion_registrar(inv):
    codigo = pedir_texto("Código del producto (ej. TOR-001): ")
    nombre = pedir_texto("Nombre: ")
    categoria = pedir_opcional("Categoría")
    descripcion = pedir_opcional("Descripción")
    ubicacion = pedir_opcional("Ubicación en el depósito")
    atributos = {"ubicacion": ubicacion} if ubicacion else {}
    producto = inv.add(codigo, nombre, category=categoria, description=descripcion, attributes=atributos)
    print(f"Producto registrado: {producto.name} ({producto.id}). Stock inicial: 0")

def opcion_recibir(inv):
    codigo = pedir_texto("Código del producto: ")
    cantidad = pedir_entero("Cantidad que ingresa: ")
    if cantidad is None:
        return
    inv.receive(codigo, cantidad)
    print(f"Entrada registrada. Stock actual: {inv.stock(codigo)}")

def opcion_retirar(inv):
    codigo = pedir_texto("Código del producto: ")
    cantidad = pedir_entero("Cantidad que sale: ")
    if cantidad is None:
        return
    #Si no alcanza el stock, la biblioteca lanza InsufficientStockError y no guarda nada.
    inv.remove(codigo, cantidad)
    print(f"Salida registrada. Stock actual: {inv.stock(codigo)}")

def opcion_consultar_stock(inv):
    codigo = pedir_texto("Código del producto: ")
    print(f"Stock de {codigo}: {inv.stock(codigo)} unidades")

def opcion_ver_producto(inv):
    codigo = pedir_texto("Código del producto: ")
    producto = inv.get(codigo)
    print(f"Código:      {producto.id}")
    print(f"Nombre:      {producto.name}")
    print(f"Categoría:   {producto.category or '-'}")
    print(f"Descripción: {producto.description or '-'}")
    print(f"Atributos:   {producto.attributes or '-'}")
    print(f"Stock:       {inv.stock(producto.id)}")

def opcion_listar(inv):
    productos = inv.list_products()
    if not productos:
        print("No hay productos registrados.")
        return
    for producto in productos:
        print(f"{producto.id:<12} {producto.name:<25} stock: {inv.stock(producto.id)}")

def opcion_historial(inv):
    codigo = pedir_texto("Código del producto: ")
    print("Fecha (UTC)          Movimiento")
    for evento in inv.history(codigo):
        detalle = f"{evento.quantity} unidades" if evento.quantity > 0 else ""
        print(f"{evento.timestamp}  {NOMBRES_EVENTO[evento.type]} {detalle}")

def opcion_eliminar(inv):
    codigo = pedir_texto("Código del producto a eliminar: ")
    confirmacion = input("¿Seguro? El producto dejará de aparecer, pero su historial se conserva (s/n): ")
    if confirmacion.strip().lower() != "s":
        print("Operación cancelada.")
        return
    #La biblioteca solo permite eliminar productos con stock 0.
    inv.delete(codigo)
    print("Producto eliminado.")

def opcion_cargar_datos_de_prueba(inv):
    #Registra varios productos con movimientos de ejemplo, para probar el menú sin cargar todo a mano.
    #Es solo una cómoda secuencia de llamadas a InventoryKit: add, receive y remove.
    cargados = 0
    for codigo, nombre, categoria, ubicacion, entrada, salida in DATOS_DE_PRUEBA:
        try:
            inv.add(codigo, nombre, category=categoria, attributes={"ubicacion": ubicacion})
        except ProductAlreadyExistsError:
            #Si el código ya existe (los datos ya se cargaron antes), se salta ese producto y no se repiten sus movimientos, así que se puede apretar 9 varias veces sin romper nada.
            print(f"  {codigo}: ya existía, se omite")
            continue
        inv.receive(codigo, entrada)
        inv.remove(codigo, salida)
        cargados += 1
        print(f"  {codigo}: {nombre} (stock {inv.stock(codigo)})")
    print(f"Datos de prueba cargados: {cargados} productos nuevos.")

OPCIONES = {
    "1": ("Registrar un producto nuevo", opcion_registrar),
    "2": ("Recibir mercadería (entrada de stock)", opcion_recibir),
    "3": ("Retirar mercadería (salida de stock)", opcion_retirar),
    "4": ("Consultar el stock de un producto", opcion_consultar_stock),
    "5": ("Ver los datos de un producto", opcion_ver_producto),
    "6": ("Listar todos los productos", opcion_listar),
    "7": ("Ver el historial de un producto", opcion_historial),
    "8": ("Eliminar un producto", opcion_eliminar),
    "9": ("Cargar datos de prueba", opcion_cargar_datos_de_prueba),
}

def ejecutar(accion, inv):
    #Ejecuta la opción elegida y traduce los errores de la biblioteca a mensajes claros.
    #El orden importa: ProductAlreadyExistsError, InsufficientStockError y StockLeftError son tipos de ValueError, así que van ANTES que ValueError; si no, este los atraparía primero.
    try:
        accion(inv)
    except ProductAlreadyExistsError:
        print("Error: ya existe un producto con ese código (un código eliminado tampoco se puede reutilizar).")
    except ProductNotFoundError:
        print("Error: no se encontró el producto con ese código.")
    except InsufficientStockError as error:
        print(f"Error: {error}")
    except StockLeftError:
        print("Error: el producto todavía tiene stock. Retire las unidades antes de eliminarlo.")
    except (TypeError, ValueError) as error:
        print(f"Datos inválidos: {error}")

def main():
    #"with" abre el inventario y lo cierra solo al salir del programa, aunque haya un error.
    with Inventory(DB) as inv:
        while True:
            limpiar_consola()
            print("=== Ferretería: sistema de inventario ===\n")
            mostrar_titulo_menu()
            for numero, (texto, _) in OPCIONES.items():
                mostrar_opcion(numero, texto)
            print(f"{ROJO}[0]{RESET} Salir")
            eleccion = input("\nElija una opción: ").strip()
            if eleccion == "0":
                limpiar_consola()
                print("¡Hasta luego!")
                break
            if eleccion not in OPCIONES:
                print("\nOpción no válida.")
                input("Presione Enter para continuar...")
                continue
            ejecutar(OPCIONES[eleccion][1], inv)
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()