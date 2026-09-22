# Clase Usuario
import sqlite3 as sql
import logging 
import os
import re
import shutil
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()
CARPETA_IMAGENES = "Imagenes/Imagenes_Productos"
URL_IMAGEN_DEFAULT = f"{CARPETA_IMAGENES}/imagen_default.png"

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
    def __init__(self, id, categoria, marca,precio, imagen):
        self.id = id
        self.categoria = categoria
        self.marca = marca
        self.precio= precio
        self.imagen = imagen

class Inventario:

    @staticmethod
    def listar_productos():
        logging.info("Se va a mostrar los productos")
        cursor.execute(
            """
            SELECT p.id_producto,
                (SELECT nombre_categoria FROM categorias
                    WHERE id_categoria_producto = p.id_categoria_producto),
                (SELECT nombre_marca FROM marcas
                    WHERE id_marca_producto = p.id_marca_producto),
                p.precio,
                p.url_imagen
            FROM productos p
            """
        )
        filas = cursor.fetchall()
        return [Producto(*fila) for fila in filas]

    @staticmethod
    def agregar_producto(categoria, marca, precio, imagen):
        def limpiar_nombre(texto):
            return re.sub(r"[^\w-]", "_", texto)
        
        url_imagen = URL_IMAGEN_DEFAULT

        try:
            valor_precio = float(precio.replace(",", "."))
            if valor_precio <= 0:
                raise ValueError
        except ValueError:
            return("PRECIO INVÁLIDO", "INGRESE UN PRECIO NUMÉRICO MAYOR A 0")
            
            
        try:
            cursor.execute(
                """
                INSERT INTO productos (id_categoria_producto, id_marca_producto, precio, url_imagen)
                VALUES (
                    (SELECT id_categoria_producto FROM categorias WHERE nombre_categoria = ?),
                    (SELECT id_marca_producto FROM marcas WHERE nombre_marca = ?),
                    ?, ?
                )
                """,
                (categoria, marca, precio, url_imagen),
            )
            id_producto = cursor.lastrowid          
            if imagen != None:
                extension = os.path.splitext(imagen)[1].lower()    
                nombre = f"{limpiar_nombre(categoria)}_{limpiar_nombre(marca)}_{id_producto}{extension}"
                url_imagen = f"{CARPETA_IMAGENES}/{nombre}"
                cursor.execute(
                    "UPDATE productos SET url_imagen = ? WHERE id_producto = ?",
                    (url_imagen, id_producto),
                )

            conexion.commit()
            logging.info(f"Se insertó el producto {categoria, marca, url_imagen} en la base de datos")

        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al insertar en la base de datos: {e}")
            return ("ERROR", "EL PRODUCTO YA EXISTE O HUBO UN ERROR EN LA BASE DE DATOS")

        if imagen != None:
            try:
                os.makedirs(CARPETA_IMAGENES, exist_ok=True)
                shutil.copy(imagen, url_imagen)
            except Exception as e:
                logging.error(f"Error al copiar la imagen: {e}")
                return ("ERROR", "EL PRODUCTO SE GUARDÓ, PERO NO SE PUDO COPIAR LA IMAGEN")

        return id_producto 

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
    def agregar_stock(datos):
        try:
            cursor = conexion.cursor()

            print("DATOS RECIBIDOS:", datos)

            for dato in datos:

                print("PROCESANDO:", dato)

                cursor.execute("""
                    SELECT id_talle_producto
                    FROM talles
                    WHERE nombre_talle = ?
                """, (dato["talle"],))

                talle = cursor.fetchone()

                print("ID TALLE:", talle)

                cursor.execute("""
                    SELECT id_color_producto
                    FROM colores
                    WHERE nombre_color = ?
                """, (dato["color"],))

                color = cursor.fetchone()

                print("ID COLOR:", color)

                if talle is None or color is None:
                    raise ValueError("El talle o color no existe")

                id_talle = talle[0]
                id_color = color[0]

                cursor.execute("""
                    UPDATE stock_variantes
                    SET cantidad_stock = cantidad_stock + ?
                    WHERE id_producto = ?
                    AND id_talle_producto = ?
                    AND id_color_producto = ?
                """, (
                    int(dato["cantidad"]),
                    dato["id"],
                    id_talle,
                    id_color
                ))

                print("FILAS ACTUALIZADAS:", cursor.rowcount)

                if cursor.rowcount == 0:

                    print("NO EXISTE, INSERTANDO...")

                    cursor.execute("""
                        INSERT INTO stock_variantes (
                            id_producto,
                            id_talle_producto,
                            id_color_producto,
                            cantidad_stock
                        )
                        VALUES (?, ?, ?, ?)
                    """, (
                        dato["id"],
                        id_talle,
                        id_color,
                        int(dato["cantidad"])
                    ))

                    print("INSERTADO")

            conexion.commit()

            print("COMMIT REALIZADO")

            logging.info("Se agregó stock correctamente")

            return None

        except Exception as e:
            conexion.rollback()

            print("ERROR:", e)

            logging.error(f"Error al ingresar stock: {e}")

            return (
                "ERROR AL INGRESAR STOCK",
                "ASEGURESE DE INGRESAR BIEN LOS DATOS DE STOCK"
            )
    @staticmethod
    def listar_stock(id_producto):
        logging.info(f"Se va a mostrar el stock del producto {id_producto}")
        cursor.execute(
            """
            SELECT
                (SELECT nombre_talle FROM talles
                    WHERE id_talle_producto = s.id_talle_producto),
                (SELECT nombre_color FROM colores
                    WHERE id_color_producto = s.id_color_producto),
                s.cantidad_stock
            FROM stock_variantes s
            WHERE s.id_producto = ?
            """,
            (id_producto,),
        )
        lista=cursor.fetchall()

        cursor.execute("SELECT nombre_talle FROM talles")
        talles = [fila[0] for fila in cursor.fetchall()]

        cursor.execute("SELECT nombre_color FROM colores")
        colores = [fila[0] for fila in cursor.fetchall()]

         
        lista_diccionario=[]
        for p in lista:
            diccionario={"color":p[1],"talle":p[0],"cantidad":p[2]}
            lista_diccionario.append(diccionario)

        return {"diccionario":lista_diccionario,"talles":talles,"colores":colores}

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