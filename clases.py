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
    def agregar_producto(nombre, precio, stock):
        
        if nombre=="" or precio=="" or stock=="":
            return ("DATOS INCOMPLETOS", "POR FAVOR, COMPLETE TODOS LOS CAMPOS") 
        try:
            precio_val = float(precio)
            stock_val = int(stock)
        except:
            return ("VALORES INCORRECTOS", "LOS DATOS DE PRECIO O STOCK SON INCORRECTOS")
        
        try:
            cursor.execute(
                "INSERT INTO productos (nombre_producto, precio, stock) VALUES (?, ?, ?)",
                (nombre.strip(), precio_val, stock_val)
            )
            conexion.commit()
            logging.info(f"Se inserto el producto {nombre} en la base de datos")
            return None
            
        except Exception as e:
            conexion.rollback() 
            logging.error(f"Error al insertar en la base de datos: {e}")
            return "EL PRODUCTO YA EXISTE O HUBO UN ERROR EN LA BASE DE DATOS"

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

