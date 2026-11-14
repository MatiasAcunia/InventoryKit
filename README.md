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

- Python 3.10 
- SQLite para almacenar los productos y movimientos.
- `sqlite3` para interactuar con la base de datos.
- JSON para almacenar atributos adicionales de los productos.
- `unittest`' para las pruebas automáticas
- Biblioteca estándar de Python, sin dependencias externas de ejecución.

## 4. Estructura del proyecto


InventoryKit/
├── inventorykit/        # la biblioteca
│   ├── __init__.py
│   ├── inventory.py
│   ├── models.py
│   ├── exceptions.py
│   └── storage.py
├── tests/               # pruebas automáticas
├── examples/            # ejemplos de uso
├── pyproject.toml
└── README.md

El código está organizado dentro del paquete `inventorykit`:

- **__init__.py:** permite importar las clases principales desde el paquete.
- **inventory.py:** contiene la clase `Inventory`, las operaciones públicas y las reglas de negocio.
- **storage.py:** contiene la clase `SQLiteStorage`, encargada de la conexión, las consultas SQL y las transacciones.
- **models.py:** define las clases `Product`, `InventoryEvent` y los tipos de eventos.
- **exceptions.py:** contiene las excepciones propias de la biblioteca.

Separamos la lógica de inventario del acceso a los datos para que cada parte tenga una responsabilidad definida.

## 5. Instalación y uso

Requisito: tener Python 3.10 o superior instalado.

Clonar el repositorio e instalar la biblioteca en un entorno virtual

```bash
git clone https://github.com/MatiasAcunia/InventoryKit.git
cd InventoryKit
python -m venv .venv
.venv\Scripts\activate    #Nota: En Linux: source .venv/bin/activate
pip install -e .
```

Luego se puede importar desde cualquier carpeta, con el entorno activado.
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

## 7. Reglas y errores

Reglas comunes:
- El id y el nombre no pueden estar vacíos
- El id no puede tener espacios al principio o al final (se rechaza, no se corrige)
- Las cantidades son enteros positivos 
- Las claves de `attributes` son textos no vacíos y los valores deben poder guardarse como JSON.

| Excepción | Cuándo se lanza |
| --------- | --------------- |
| `TypeError` | Tipo de argumento incorrecto (por ejemplo, una cantidad decimal o un booleano) |
| `ValueError` | Texto vacío, id con espacios sobrantes, cantidad menor o igual a 0, atributos no serializables |
| `ProductAlreadyExistsError` (es un `ValueError`) | `add` con un id ya usado, incluso por un producto eliminado |
| `ProductNotFoundError` (es un `LookupError`) | No hay un producto **activo** con ese id. `history` es la excepción: acepta productos eliminados y falla solo si el id nunca existió |
| `InsufficientStockError` (es un `ValueError`) | `remove` pide más unidades de las disponibles |
| `StockLeftError` (es un `ValueError`) | `delete` sobre un producto que todavía tiene stock |

Si una operación falla, no queda nada guardado a medias: cada operación de escritura es una transacción que se revierte completa ante cualquier error.

## 8. Concurrencia y límites

- Varias conexiones o procesos pueden usar el **mismo archivo local**. SQLite permite un solo escritor a la vez, así que las escrituras se ordenan: dos salidas simultáneas nunca consumen las mismas existencias.
- Si otra conexión mantiene el candado de escritura por más tiempo del que espera (5 segundos por defecto), la operación **no se realiza** y se propaga `sqlite3.OperationalError: database is locked`. No se convierte en un error de negocio; la aplicación puede reintentar.
- No compartir una misma instancia de `Inventory` entre hilos: cada hilo debe abrir la suya.
- No se garantiza el funcionamiento sobre carpetas de red (NFS/SMB) ni con muchos escritores simultáneos. Está pensada para aplicaciones pequeñas.
- Las fechas de los eventos se guardan en **UTC** y se devuelven como texto (`AAAA-MM-DD HH:MM:SS`).

## 9. Pruebas y ejemplos

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren los contratos de las operaciones, la persistencia al cerrar y reabrir, la reversión ante fallos y la concurrencia entre conexiones.

En `examples/` hay un programa que usa la biblioteca como lo haría un proyecto externo:

- `basic_usage.py`: operaciones básicas con un archivo y reapertura.

## 10. Estado del proyecto

Las ocho operaciones están implementadas, con validaciones, transacciones y pruebas automáticas, y la biblioteca se puede instalar con `pip install -e .`.