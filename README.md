# InventoryKit

## 1. Descripción del proyecto

Proyecto desarrollado en Python para Samsung Innovation Campus.

InventoryKit es una biblioteca para gestionar productos, existencias y movimientos de inventario. Está pensada para ser utilizada desde otros programas de Python, sin necesidad de implementar nuevamente toda la lógica de inventario.

La idea es ofrecer operaciones sencillas para registrar productos, ingresar o retirar unidades, consultar el stock disponible y mantener un historial de los movimientos realizados.

Los datos se almacenan mediante SQLite, por lo que no es necesario instalar ni configurar un servidor de base de datos.

El proyecto está orientado a aplicaciones pequeñas y se encuentra en desarrollo.

## 2. Funcionalidades

La biblioteca está diseñada para ofrecer ocho operaciones principales:

- **add():** registrar un producto con su identificador y nombre, además de información opcional.
- **get():** consultar los datos de un producto.
- **list_products():** obtener una lista de los productos activos.
- **delete():** desactivar un producto sin eliminar su historial.
- **receive():** registrar una entrada de unidades.
- **remove():** retirar unidades, comprobando que exista stock suficiente.
- **stock():** consultar la cantidad disponible de un producto.
- **history():** consultar los movimientos registrados de un producto.

Cada producto puede tener una categoría, una descripción y un diccionario de atributos adicionales. Esto permite guardar información particular, como una marca, ubicación o características, sin modificar las tablas.

También se contempla la validación de datos, el manejo de errores y el uso de transacciones para evitar operaciones incompletas.

## 3. Tecnologías utilizadas

- Python 3.
- SQLite para almacenar los productos y movimientos.
- `sqlite3` para interactuar con la base de datos.
- JSON para almacenar atributos adicionales de los productos.
- Biblioteca estándar de Python, sin dependencias externas de ejecución.

## 4. Estructura del proyecto

El código está organizado dentro del paquete `inventorykit`:

- **__init__.py:** permite importar las clases principales desde el paquete.
- **inventory.py:** contiene la clase `Inventory`, las operaciones públicas y las reglas de negocio.
- **storage.py:** contiene la clase `SQLiteStorage`, encargada de la conexión, las consultas SQL y las transacciones.
- **models.py:** define las clases `Product`, `InventoryEvent` y los tipos de eventos.
- **exceptions.py:** contiene las excepciones propias de la biblioteca.

Separamos la lógica de inventario del acceso a los datos para que cada parte tenga una responsabilidad definida.

## 5. Instalación y uso

Requisito: tener Python 3 instalado.

Para clonar el repositorio:

```bash
git clone https://github.com/MatiasAcunia/InventoryKit.git
```

Ingresar a la carpeta del proyecto:

```bash
cd InventoryKit
```

Actualmente se puede utilizar el paquete directamente desde la carpeta del repositorio. El empaquetado para instalación independiente todavía está pendiente.

Ejemplo básico de las operaciones implementadas:

```python
from inventorykit import Inventory

inventario = Inventory()

inventario.add(
    "P001",
    "Teclado",
    category="Periféricos",
    attributes={"marca": "Logitech"}
)

print(inventario.get("P001"))
print(inventario.stock("P001"))
```

En este ejemplo se crea un inventario temporal en memoria, se registra un producto y se consulta su información. Como todavía no se ingresaron unidades, el stock inicial es cero.

También está previsto trabajar con archivos SQLite, de modo que los datos se conserven entre ejecuciones.

## 6. Funcionamiento del inventario

Una decisión importante del proyecto es que el stock no se almacena directamente como un número en la tabla de productos.

En su lugar, se calcula a partir de los movimientos registrados.

Por ejemplo, si un producto recibe 100 unidades y después se retiran 30, su stock disponible es de 70 unidades.

El historial contempla eventos de creación y eliminación de productos, además de entradas y salidas de stock.

Los productos se eliminan de manera lógica: se marcan como inactivos, pero sus registros permanecen en la base de datos. Para eliminarlos, primero deben tener stock cero. Sus identificadores tampoco pueden reutilizarse.

La biblioteca no incluye interfaz gráfica ni servidor HTTP. Su objetivo es que otras aplicaciones puedan utilizar directamente sus funciones de Python.

## 7. Estado del proyecto

InventoryKit se encuentra en desarrollo.

Ya se implementó una parte de la estructura, los modelos, las operaciones de almacenamiento y varios métodos públicos.

Todavía queda completar y revisar las operaciones restantes, integrar correctamente el manejo de transacciones, realizar pruebas y preparar la instalación como biblioteca independiente.

El objetivo es terminar una versión pequeña, funcional y reutilizable, manteniendo una implementación sencilla y sin agregar características que no sean necesarias para el alcance del proyecto.
