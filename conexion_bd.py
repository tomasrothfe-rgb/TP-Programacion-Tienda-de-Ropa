import sqlite3 as sql
import hashlib
import os


def creacion_bd():  # Crea todas las tablas y carga datos iniciales (solo si no existen)
    conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
    cursor = conexion.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS marcas (
            id_marca_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_marca TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS colores (
            id_color_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_color TEXT NOT NULL UNIQUE,
            codigo_hex TEXT
        );

        CREATE TABLE IF NOT EXISTS talles (
            id_talle_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_talle TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_categoria_producto INTEGER,
            id_marca_producto INTEGER,
            nombre_producto TEXT,
            precio REAL NOT NULL,
            url_imagen TEXT,
            FOREIGN KEY (id_categoria_producto) REFERENCES categorias(id_categoria_producto),
            FOREIGN KEY (id_marca_producto) REFERENCES marcas(id_marca_producto)
        );

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

        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente' CHECK (rol IN ('cliente', 'admin')),
            alerta_activa TEXT NOT NULL DEFAULT '0'
        );

        CREATE TABLE IF NOT EXISTS productos_carrito (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            color TEXT NOT NULL,
            talle TEXT NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad > 0),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
            UNIQUE (id_usuario, id_producto, color, talle)
        );

        CREATE TABLE IF NOT EXISTS compras (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            metodo_pago TEXT NOT NULL CHECK (metodo_pago IN ('tarjeta', 'transferencia')),
            tipo_envio TEXT NOT NULL CHECK (tipo_envio IN ('retiro', 'envio')),
            total REAL NOT NULL,
            fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        );

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
        );

        CREATE TABLE IF NOT EXISTS alertas_usuarios (
            id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_alerta TEXT NOT NULL UNIQUE,
            descripcion_alerta TEXT NOT NULL
        );

        INSERT OR IGNORE INTO categorias (nombre_categoria) VALUES
        ('Remera'),
        ('Pantalón'),
        ('Buzo'),
        ('Campera');

        INSERT OR IGNORE INTO marcas (nombre_marca) VALUES
        ('Nike'),
        ('Adidas'),
        ('Puma'),
        ('Levi''s'),
        ('Tommy Hilfiger');

        INSERT OR IGNORE INTO talles (nombre_talle) VALUES
        ('XS'),
        ('S'),
        ('M'),
        ('L'),
        ('XL'),
        ('XXL');

        INSERT OR IGNORE INTO colores (nombre_color, codigo_hex) VALUES
        ('Rojo', '#DC2626'),
        ('Azul', '#2563EB'),
        ('Negro', '#0D1117'),
        ('Verde', '#16A34A'),
        ('Gris', '#9CA3AF'),
        ('Blanco', '#F8FAFC'),
        ('Amarillo', '#D59E0B');

        INSERT OR IGNORE INTO alertas_usuarios (titulo_alerta, descripcion_alerta) VALUES
        ('CARRITO', 'ALGUNOS ELEMENTOS DE SU CARRITO FUERON COMPRADOS'),
        ('ERROR DE CUENTA', 'SU CUENTA SE DESACTIVO POR INACTIVIDAD');
    ''')

    salt = os.urandom(16)  # Genera la sal para hashear la contraseña del admin por defecto
    h = hashlib.pbkdf2_hmac("sha256", "admin123".encode(), salt, 100_000)
    contrasena_hash = salt.hex() + ":" + h.hex()
    cursor.execute(  # Crea el admin inicial (si ya existe, lo ignora)
        """
        INSERT OR IGNORE INTO usuarios (nombre, apellido, email, contrasena, rol)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Admin", "Jupiter", "admin@jupiter.com", contrasena_hash, "admin"),
    )

    conexion.commit()
    conexion.close()