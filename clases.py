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
def limpiar_nombre(texto):
    return re.sub(r"[^\w-]", "_", texto)

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
    def __init__(self, id, categoria, marca, nombre, precio, imagen):
        self.id = id
        self.categoria = categoria
        self.marca = marca
        self.nombre = nombre
        self.precio= precio
        self.imagen = imagen

class Inventario:
    @staticmethod
    def consultar_producto_especifico(id):
        logging.info(f"Se va a mostrar el producto con id {id}")
        cursor.execute(
            """
            SELECT
            s.id_producto,
                (SELECT nombre_categoria FROM categorias
                    WHERE id_categoria_producto = s.id_categoria_producto),
                (SELECT nombre_marca FROM marcas
                    WHERE id_marca_producto = s.id_marca_producto),
                s.nombre_producto,
                s.precio,
                s.url_imagen
            FROM productos s
            WHERE s.id_producto = ?
            """,
            (id,),
        )
        datos=cursor.fetchall()[0]
        return {
            "id":datos[0],
            "categoria":datos[1],
            "marca":datos[2],
            "nombre":datos[3],
            "precio":datos[4],
            "url":datos[5],
        }

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
                p.nombre_producto,
                p.precio,
                p.url_imagen
            FROM productos p
            """
        )
        filas = cursor.fetchall()
        return [Producto(*fila) for fila in filas]

    @staticmethod
    def agregar_producto(categoria, marca, nombre_producto, precio, imagen):
        
        url_imagen = URL_IMAGEN_DEFAULT

        nombre_producto = nombre_producto.strip()
        if not nombre_producto:
            return ("NOMBRE INVÁLIDO", "INGRESE UN NOMBRE PARA EL PRODUCTO")

        try:
            valor_precio = float(precio.replace(",", "."))
            if valor_precio <= 0:
                raise ValueError
        except ValueError:
            return("PRECIO INVÁLIDO", "INGRESE UN PRECIO NUMÉRICO MAYOR A 0")
            
            
        try:
            cursor.execute(
                """
                INSERT INTO productos (id_categoria_producto, id_marca_producto, nombre_producto, precio, url_imagen)
                VALUES (
                    (SELECT id_categoria_producto FROM categorias WHERE nombre_categoria = ?),
                    (SELECT id_marca_producto FROM marcas WHERE nombre_marca = ?),
                    ?,
                    ?, 
                    ?
                )
                """,
                (categoria, marca, nombre_producto, precio, url_imagen),
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
            logging.info(f"Se insertó el producto {categoria, marca,nombre_producto} en la base de datos")

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
    def modificar_producto(id,categoria,marca,nombre,precio,url):
        logging.info(f"{id},{categoria},{marca},{nombre},{precio},{url}")
 
        nombre = nombre.strip()
        if not nombre:
            return ("NOMBRE INVÁLIDO", "INGRESE UN NOMBRE PARA EL PRODUCTO")
 
        try:
            valor_precio = float(str(precio).replace(",", "."))
            if valor_precio <= 0:
                raise ValueError
        except ValueError:
            return ("PRECIO INVÁLIDO", "INGRESE UN PRECIO NUMÉRICO MAYOR A 0")
 
        viejos_elementos = cursor.execute(
            """
            SELECT 
            (SELECT nombre_categoria FROM categorias WHERE id_categoria_producto = s.id_categoria_producto),
            (SELECT nombre_marca FROM marcas WHERE id_marca_producto = s.id_marca_producto),
            nombre_producto,
            precio,
            url_imagen
            FROM productos s WHERE id_producto=?
            """,
            (id,)
        ).fetchone()
 
        if viejos_elementos is None:
            return ("ERROR", "EL PRODUCTO NO EXISTE")
 
        url_vieja = viejos_elementos[4]
        url_imagen = url_vieja
        imagen_nueva = url is not None and url != url_vieja
        if imagen_nueva:
            extension = os.path.splitext(url)[1].lower()
            nombre_archivo = f"{limpiar_nombre(categoria)}_{limpiar_nombre(marca)}_{id}{extension}"
            url_imagen = f"{CARPETA_IMAGENES}/{nombre_archivo}"

        try:
            precio_viejo = float(str(viejos_elementos[3]).replace(",", "."))
        except ValueError:
            precio_viejo = None
        viejos = (viejos_elementos[0], viejos_elementos[1], viejos_elementos[2], precio_viejo, url_vieja)
        nuevos = (categoria, marca, nombre, valor_precio, url_imagen)
        if viejos == nuevos:
            logging.info("No hubo cambios en el producto")
            return None

        if imagen_nueva:
            try:
                os.makedirs(CARPETA_IMAGENES, exist_ok=True)
                shutil.copy(url, url_imagen)
            except Exception as e:
                logging.error(f"Error al copiar la imagen: {e}")
                return ("ERROR", "NO SE PUDO COPIAR LA IMAGEN NUEVA")

        try:
            cursor.execute(
                """
                UPDATE productos
                SET id_categoria_producto = (SELECT id_categoria_producto FROM categorias WHERE nombre_categoria = ?),
                    id_marca_producto = (SELECT id_marca_producto FROM marcas WHERE nombre_marca = ?),
                    nombre_producto = ?,
                    precio = ?,
                    url_imagen = ?
                WHERE id_producto = ?
                """,
                (categoria, marca, nombre, valor_precio, url_imagen, id),
            )
            conexion.commit()
            logging.info(f"Se modificó el producto {id}")
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al modificar producto: {e}")
            return ("ERROR", "EL PRODUCTO YA EXISTE O HUBO UN ERROR EN LA BASE DE DATOS")

        if (
            imagen_nueva
            and url_vieja
            and url_vieja != url_imagen
            and url_vieja != URL_IMAGEN_DEFAULT
            and os.path.exists(url_vieja)
        ):
            os.remove(url_vieja)
 
        return None
         
        
    @staticmethod
    def eliminar_producto(id):
        try:
            cursor.execute(
                "SELECT url_imagen FROM productos WHERE id_producto = ?",
                (id,)
            )

            resultado = cursor.fetchone()

            if resultado is None:
                return (
                    "ERROR AL ELIMINAR PRODUCTO",
                    "EL PRODUCTO NO EXISTE"
                )

            url_imagen = resultado[0]

            cursor.execute(
                "DELETE FROM stock_variantes WHERE id_producto = ?",
                (id,)
            )

            cursor.execute(
                "DELETE FROM productos WHERE id_producto = ?",
                (id,)
            )

            conexion.commit()

            if (
                url_imagen
                and url_imagen != URL_IMAGEN_DEFAULT
                and os.path.exists(url_imagen)
            ):
                os.remove(url_imagen)

            logging.info("Se eliminó el producto de la base de datos")

            return None

        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al eliminar producto: {e}")

            return (
                "ERROR AL ELIMINAR PRODUCTO",
                "NO SE PUDO ELIMINAR EL PRODUCTO"
            )

    @staticmethod
    def agregar_stock(datos):
        try:
            cursor = conexion.cursor()

            for dato in datos:

                if int(dato["cantidad"]) < 0:
                    raise ValueError("El valor de la cantidad debe ser mayor o igual 0")
                
                cursor.execute("""
                    SELECT id_talle_producto
                    FROM talles
                    WHERE nombre_talle = ?
                """, (dato["talle"],))
                talle = cursor.fetchone()

                cursor.execute("""
                    SELECT id_color_producto
                    FROM colores
                    WHERE nombre_color = ?
                """, (dato["color"],))

                color = cursor.fetchone()

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

                if cursor.rowcount == 0:
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

            conexion.commit()
            logging.info("Se agregó stock correctamente")
            return None

        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al ingresar stock: {e}")
            return ("ERROR AL INGRESAR STOCK","ASEGURESE DE INGRESAR BIEN LOS DATOS DE STOCK")
        
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