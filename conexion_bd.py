import sqlite3 as sql
import logging 
import hashlib
import os
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()

def hashear_contrasena(contrasena):
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, 100_000)
    return salt.hex() + ":" + h.hex()

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
            nombre_color TEXT NOT NULL UNIQUE,
            codigo_hex TEXT
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
            nombre_producto,
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
        INSERT INTO colores (nombre_color, codigo_hex) VALUES 
        ('Rojo', '#DC2626'),
        ('Azul', '#2563EB'),
        ('Negro', '#0D1117'),
        ('Verde', '#16A34A'),
        ('Gris', '#9CA3AF'),
        ('Blanco', '#F8FAFC');

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
def insertar():
    cursor.execute(
    """
    INSERT INTO stock_variantes (id_producto, id_talle_producto, id_color_producto, cantidad_stock)
    VALUES (
        ?,
        (SELECT id_talle_producto FROM talles WHERE nombre_talle = ?),
        (SELECT id_color_producto FROM colores WHERE nombre_color = ?),
        ?
    )
    """,
    (1, "XL", "Azul", 1),
    )
    conexion.commit()  


def carrito():
    cursor.execute(
        """ CREATE TABLE productos_carrito (
    id_item         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario     INTEGER NOT NULL,
    id_producto     INTEGER NOT NULL,
    color           TEXT NOT NULL,
    talle           TEXT NOT NULL,
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    UNIQUE (id_usuario, id_producto, color, talle)
);"""
    )

def compras():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            metodo_pago TEXT NOT NULL CHECK (metodo_pago IN ('tarjeta', 'transferencia')),
            tipo_envio TEXT NOT NULL CHECK (tipo_envio IN ('retiro', 'envio')),
            total REAL NOT NULL,
            fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulos_comprados (
            id_articulo_comprado INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            marca TEXT NOT NULL,
            nombre TEXT NOT NULL,
            talle TEXT,
            color TEXT,
            cantidad INTEGER NOT NULL DEFAULT 1,
            precio REAL NOT NULL,
            FOREIGN KEY (id_compra) REFERENCES compras(id_compra)
        )
    """)

    conexion.commit()



def usuarios():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente' CHECK (rol IN ('cliente', 'admin')),
            alerta_activa TEXT NOT NULL DEFAULT None
            )""")
def eliminar():
    cursor.execute(
        """
    DROP TABLE usuarios;
    """
    )
    conexion.commit()

def instertar_admin():
    cursor.execute(
        """
        INSERT INTO usuarios (nombre, apellido, email, contrasena, rol)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Admin", "Novus", "admin@novusprestige.com", hashear_contrasena("admin123"), "admin"),
    )
    conexion.commit()

def alertas():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alertas_usuarios(
            id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_alerta TEXT NOT NULL UNIQUE,
            descripcion_alerta TEXT NOT NULL
        )
        """
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO alertas_usuarios (titulo_alerta, descripcion_alerta)
        VALUES (?, ?)
        """,
        [
            ("CARRITO", "ALGUNOS ELEMENTOS DE SU CARRITO FUERON COMPRADOS"),
            ("ERROR DE CUENTA", "SU CUENTA SE DESACTIVO POR INACTIVIDAD"),
        ],
    )
    conexion.commit()

def borrar():
    cursor.execute(
        """DROP TABLE alertas_usuarios"""
    )