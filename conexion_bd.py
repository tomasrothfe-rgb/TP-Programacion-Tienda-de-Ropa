import sqlite3 as sql
import logging 
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()

# Conexion con la bd y creacion de tablas
def creacion_bd():
    cursor.executescript('''
        -- Creación de la tabla de categorías (con nombre único)
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL UNIQUE
        );

        -- Creación de la tabla de marcas (con nombre único)
        CREATE TABLE IF NOT EXISTS marcas (
            id_marca_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_marca TEXT NOT NULL UNIQUE
        );

        -- Creación de la tabla de colores (con nombre único)
        CREATE TABLE IF NOT EXISTS colores (
            id_color_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_color TEXT NOT NULL UNIQUE
        );

        -- Creación de la tabla de talles (con nombre único)
        CREATE TABLE IF NOT EXISTS talles (
            id_talle_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_talle TEXT NOT NULL UNIQUE
        );

        -- Creación de la tabla principal de productos
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_categoria_producto INTEGER,
            id_marca_producto INTEGER,
            precio REAL NOT NULL,
            url_imagen TEXT,
            FOREIGN KEY (id_categoria_producto) REFERENCES categorias(id_categoria_producto),
            FOREIGN KEY (id_marca_producto) REFERENCES marcas(id_marca_producto)
        );

        -- Creación de la tabla de stock por variantes
        CREATE TABLE IF NOT EXISTS stock_variantes (
            id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            id_talle_producto INTEGER NOT NULL,
            id_color_producto INTEGER NOT NULL,
            cantidad_stock INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY (id_talle_producto) REFERENCES talles(id_talle_producto),
            FOREIGN KEY (id_color_producto) REFERENCES colores(id_color_producto)
        );

        -- Inserción de registros de ejemplo en categorias
        INSERT INTO categorias (nombre_categoria) VALUES 
        ('Remera'),
        ('Pantalón'),
        ('Buzo'),
        ('Campera');

        -- Inserción de registros de ejemplo en marcas
        INSERT INTO marcas (nombre_marca) VALUES 
        ('Nike'),
        ('Adidas'),
        ('Puma'),
        ('Levi''s');

        -- Inserción de registros de ejemplo en colores
        INSERT INTO colores (nombre_color) VALUES 
        ('Rojo'),
        ('Azul'),
        ('Negro'),
        ('Verde'),
        ('Gris'),
        ('Blanco');

        -- Inserción de registros de ejemplo en talles
        INSERT INTO talles (nombre_talle) VALUES 
        ('XS'),
        ('S'),
        ('M'),
        ('L'),
        ('XL'),
        ('XXL');
    ''')
# Funcion para comprobar si un usuario existe
def comprobar_usuarios(email):
    logging.info(f"Se recibio {email}")
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()
    if fila:
        logging.info("Se encontro el usuario, procediendo a devolver los datos como un arreglo")
        return [fila[0],fila[1],fila[2], fila[3]]
    else:
        logging.info("El usuario no existe en la base de datos")
        return None

# Funcion para insertar nuevos usuarios a la base de datos
def ingresar_usuarios(email, nombre, contraseña, rol): 
    cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)",(nombre, email, contraseña, rol))
    logging.info(f"Se insterto el usuario {email} a la base de datos")
    conexion.commit()

creacion_bd()