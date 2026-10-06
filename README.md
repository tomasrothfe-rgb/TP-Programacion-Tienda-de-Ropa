# Jupiter — Tienda de Ropa

Aplicación de escritorio para gestionar una tienda de ropa, con inicio de sesión y dos tipos de usuario: **clientes**, que recorren el catálogo y compran, y **administradores**, que gestionan productos, stock y cuentas.

Trabajo Práctico Integrador de **Programación I**, Tecnicatura Superior en Desarrollo de Software, ITEC "El Molino".
Docente: Francisco Yackel.

## Integrantes

- _Tomás Roth_
- _Facundo Carabajal_

## Tecnologías

- **Python** 3.10 o superior (desarrollado con 3.13)
- **Flet**: interfaz gráfica
- **flet-color-pickers**: selector de color en el panel de administración
- **email-validator**: validación de correos en el registro
- **SQLite**: base de datos local (incluida en Python)

## Instalación

1. Instalar Python desde [python.org](https://www.python.org/downloads/). En Windows, marcar la opción **"Add Python to PATH"** durante la instalación.
2. Descargar o clonar el repositorio:

   ```bash
   git clone https://github.com/tomasrothfe-rgb/TP-Programacion-Tienda-de-Ropa.git
   cd TP-Programacion-Tienda-de-Ropa
   ```
3. Instalar las dependencias (Flet, el selector de color y el validador de correos):

   ```bash
   pip install -r requerimientos.txt
   ```

   O una por una:

   ```bash
   pip install flet
   pip install flet-color-pickers
   pip install email-validator
   ```

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
python main.py
```

> Hay que ejecutarlo **desde la carpeta del proyecto**, porque la base de datos y las imágenes se buscan con rutas relativas.

Si la base de datos `Base_de_datos_Tienda_Ropa.db` no existe, se crea al iniciar con las categorías, marcas, talles y colores iniciales.

### Usuario administrador de prueba

| Correo                      | Contraseña  |
| --------------------------- | ------------ |
| `admin@novusprestige.com` | `admin123` |

Para entrar como cliente, crear una cuenta desde la pestaña **Registrarse**.

## Funcionalidades

**Cliente**

- Registro e inicio de sesión (contraseñas guardadas con hash).
- Catálogo de productos con filtro por categoría.
- Detalle de producto con elección de color, talle y cantidad según el stock.
- Carrito de compras guardado en la base de datos.
- Compra con retiro en local o envío a domicilio, y pago con tarjeta o transferencia.
- Historial de compras y modificación de datos personales.
- Avisos cuando un producto del carrito se queda sin stock o se elimina.

**Administrador**

- Alta, modificación y baja de productos, con imagen PNG.
- Carga de stock por talle y color.
- Alta de categorías, marcas y colores (con selector de color).
- Listado de cuentas y alta de nuevos administradores.

## Estructura del proyecto

```
TP-Programacion-Tienda-de-Ropa/
├── main.py              # Punto de entrada: navegación entre pantallas
├── clases.py            # Lógica y acceso a datos: Usuario, Carrito, Inventario, Producto
├── conexion_bd.py       # Creación de tablas y datos iniciales
├── estilos.py           # Colores, fuentes y componentes visuales reutilizables
├── requerimientos.txt     # Dependencias
├── Vistas/
│   ├── login.py         # Inicio de sesión y registro
│   ├── cliente.py       # Tienda: inicio, catálogo, producto, carrito y perfil
│   ├── compra.py        # Finalizar compra
│   └── admin.py         # Panel de administración
└── Imagenes/
    ├── Imagenes_Productos/   # Imágenes de los productos cargados
    └── Imagenes_UI/          # Imágenes de la interfaz
```

## Base de datos

Tablas principales: `usuarios`, `productos`, `categorias`, `marcas`, `colores`, `talles`, `stock_variantes`, `productos_carrito`, `compras` y `articulos_comprados`.

Los artículos comprados guardan una copia del nombre, la marca y el precio al momento de la compra, para que el historial no cambie si después se modifica o elimina el producto.

## Gestión del proyecto

Las tareas, con sus criterios de aceptación, se organizan en el GitHub Project del repositorio.
