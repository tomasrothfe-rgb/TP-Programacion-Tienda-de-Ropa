# Clase Usuario
import sqlite3 as sql
import logging 
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()

class Cliente():
    def __init__(self, nombre, email, contraseña):
        self.nombre=nombre
        self.contraseña=contraseña
        self.email = email

class Admin():
    def __init__(self, nombre, email, contraseña):
        self.nombre=nombre
        self.contraseña=contraseña
        self.email = email

class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class Inventario:

    @staticmethod
    def listar_productos():
        logging.info("Se va a mostrar los productos")
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        return [Producto(*fila) for fila in filas]

    @staticmethod
    def agregar_producto(categoria, marca, imagen):
        if imagen==None:
           imagen="Imagenes/Imagenes_Productos/imagen_default.png"


    @staticmethod
    def modificar_producto(id, nombre, precio):
        cursor.execute("UPDATE productos SET nombre_producto = ?, precio = ? WHERE id_producto = ?",(nombre, precio, id))
        logging.info(f"Nuevos valores de {nombre} en la base de datos")
        conexion.commit()

    @staticmethod
    def eliminar_producto(id, nombre):
        cursor.execute("DELETE FROM productos WHERE id_producto = ?",(id,))
        logging.info(f"Se eliminó el producto {nombre} de la base de datos")
        conexion.commit()


    @staticmethod
    def agregar_stock(id, nombre, cantidad):
        cursor.execute("UPDATE productos SET stock = stock + ? WHERE id_producto = ?",(cantidad, id))
        logging.info(f"Se agregó {cantidad} más de stock a {nombre} en la base de datos")
        conexion.commit()

    @staticmethod
    def agregar_categoria(nombre):
        try:
            cursor.execute("INSERT INTO categorias (nombre_categoria) VALUES (?)", (nombre.strip(),))
            conexion.commit()
            logging.info(f"Se insertó la categoría {nombre}")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al insertar categoría: {e}")
            return ("ERROR AL AGREGAR CATEGORÍA", "ASEGURESE DE QUE LA CATEGORIA NO EXISTA EN LA BASE DE DATOS")
        
    @staticmethod
    def agregar_marca(nombre):
        try:
            cursor.execute("INSERT INTO marcas (nombre_marca) VALUES (?)", (nombre.strip(),))
            conexion.commit()
            logging.info(f"Se insertó la marca {nombre}")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al insertar marca: {e}")
            return ("ERROR AL AGREGAR MARCA", "ASEGURESE DE QUE LA MARCA NO EXISTA EN LA BASE DE DATOS")

    @staticmethod
    def agregar_color(nombre):
        try:
            cursor.execute("INSERT INTO colores (nombre_color) VALUES (?)", (nombre.strip(),))
            conexion.commit()
            logging.info(f"Se insertó el color {nombre}")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al insertar color: {e}")
            return ("ERROR AL AGREGAR COLOR", "ASEGURESE DE QUE EL COLOR NO EXISTA EN LA BASE DE DATOS")

    @staticmethod
    def agregar_talle(nombre):
        try:
            cursor.execute("INSERT INTO talles (nombre_talle) VALUES (?)", (nombre.strip(),))
            conexion.commit()
            logging.info(f"Se insertó el talle {nombre}")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al insertar talle: {e}")
            return ("ERROR AL AGREGAR TALLE", "ASEGURESE DE QUE EL TALLE NO EXISTA EN LA BASE DE DATOS")

    @staticmethod
    def listar_elementos_producto():
        logging.info("Se van a mostrar los elementos para un producto")

        cursor.execute("SELECT nombre_categoria FROM categorias")
        categorias = [fila[0] for fila in cursor.fetchall()]

        cursor.execute("SELECT nombre_marca FROM marcas")
        marcas = [fila[0] for fila in cursor.fetchall()]

        return [categorias, marcas]