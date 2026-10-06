# Clase Usuario
import sqlite3 as sql
import logging 
import os
import re
import shutil
import hashlib
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()

CARPETA_IMAGENES = "Imagenes/Imagenes_Productos"
URL_IMAGEN_DEFAULT = f"{CARPETA_IMAGENES}/imagen_default.png"
def limpiar_nombre(texto):
    return re.sub(r"[^\w-]", "_", texto)

import hashlib

def hashear_contrasena(contrasena):
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), salt, 100_000)
    return salt.hex() + ":" + h.hex()

def verificar_contrasena(contrasena, guardado):
    salt_hex, h_hex = guardado.split(":")
    h = hashlib.pbkdf2_hmac("sha256", contrasena.encode(), bytes.fromhex(salt_hex), 100_000)
    return h.hex() == h_hex


class Usuario():
    def __init__(self, id, nombre, apellido, email, contraseña, rol, alerta):
        self.nombre = nombre
        self.contraseña = contraseña
        self.email = email
        self.id = id
        self.apellido = apellido
        self.rol = rol
        self.alerta = alerta

    @staticmethod
    def iniciar_sesion(email, contrasena):
        email=email.strip()
        contrasena=contrasena.strip()
        if not email or not contrasena:
            return ("ERROR DE INICIO DE SESIÓN", "INGRESE SU CORREO Y CONTRASEÑA")
        else:
            try:
                cursor.execute(
                    "SELECT id_usuario, nombre, apellido, email, contrasena, rol, alerta_activa FROM usuarios WHERE email = ?",
                    (email,),
                )
                resultado = cursor.fetchone()
                if resultado is None:
                    return ("ERROR DE INICIO DE SESIÓN", "USUARIO NO ENCONTRADO")
                else:
                    id, nombre, apellido, email_db, contrasena_db, rol, alerta = resultado
                    if verificar_contrasena(contrasena, contrasena_db):
                        if rol == "admin":
                            return None, Admin(id,nombre,apellido,email_db,contrasena_db,rol,alerta) 
                        elif rol == "cliente":
                            return None, Cliente(id,nombre,apellido,email_db,contrasena_db,rol,alerta) 
                    else:
                        return ("ERROR DE INICIO DE SESIÓN", "CONTRASEÑA INCORRECTA")
            except Exception as e:
                logging.error(f"Error al iniciar sesión: {e}")
                return ("ERROR DE INICIO DE SESIÓN", "HUBO UN ERROR EN LA BASE DE DATOS")

    @staticmethod
    def registrar(nombre, apellido, email, contrasena):
        nombre=nombre.strip()
        apellido=apellido.strip()
        email=email.strip()
        contrasena=contrasena.strip()

        if not nombre or not apellido or not email or not contrasena:
            return ("ERROR DE REGISTRO", "INGRESE TODOS LOS CAMPOS")
        try:
            contrasena_hash = hashear_contrasena(contrasena)
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol, alerta_activa) VALUES (?, ?, ?, ?, 'cliente', 0)",
                (nombre, apellido, email, contrasena_hash),
            )
            conexion.commit()
            logging.info(f"Se registró el usuario {nombre} {apellido} en la base de datos")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al registrar usuario: {e}")
            return ("ERROR DE REGISTRO", "EL USUARIO YA EXISTE O HUBO UN ERROR EN LA BASE DE DATOS")

    @staticmethod
    def registrar_admin(nombre, apellido, email, contrasena):
        nombre=nombre.strip()
        apellido=apellido.strip()
        email=email.strip()
        contrasena=contrasena.strip()

        if not nombre or not apellido or not email or not contrasena:
            return ("ERROR AL AGREGAR ADMINISTRADOR", "INGRESE TODOS LOS CAMPOS")
        try:
            contrasena_hash = hashear_contrasena(contrasena)
            cursor.execute(
                "INSERT INTO usuarios (nombre, apellido, email, contrasena, rol, alerta_activa) VALUES (?, ?, ?, ?, 'admin', 0)",
                (nombre, apellido, email, contrasena_hash),
            )
            conexion.commit()
            logging.info(f"Se registró el administrador {nombre} {apellido} en la base de datos")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al registrar administrador: {e}")
            return ("ERROR AL AGREGAR ADMINISTRADOR", "EL CORREO YA EXISTE O HUBO UN ERROR EN LA BASE DE DATOS")

    @staticmethod
    def agregar_alerta(id_usuario, mensaje, confirmar=True):
        cursor.execute("SELECT alerta_activa FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        fila = cursor.fetchone()
        if fila is None:
            return
        actual = fila[0]
        if actual in (None, "", "0", "None"):
            nueva = mensaje
        else:
            nueva = f"{actual}\n{mensaje}"
        cursor.execute("UPDATE usuarios SET alerta_activa = ? WHERE id_usuario = ?", (nueva, id_usuario))
        if confirmar:
            conexion.commit()

    @staticmethod
    def revisar_alerta(id_usuario):
        cursor.execute("SELECT alerta_activa FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        fila = cursor.fetchone()
        if fila is None or fila[0] in (None, "", "0", "None"):
            return None
        mensaje = fila[0]
        cursor.execute("UPDATE usuarios SET alerta_activa = '0' WHERE id_usuario = ?", (id_usuario,))
        conexion.commit()
        return mensaje

    @staticmethod
    def obtener_datos(id_usuario):
        cursor.execute("SELECT nombre, apellido, email FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        fila = cursor.fetchone()
        if fila is None:
            return None
        return {"nombre": fila[0], "apellido": fila[1], "email": fila[2]}

    @staticmethod
    def modificar_datos(id_usuario, nombre, apellido, email, contrasena_actual="", contrasena_nueva=""):
        nombre = nombre.strip()
        apellido = apellido.strip()
        email = email.strip()
        contrasena_actual = contrasena_actual.strip()
        contrasena_nueva = contrasena_nueva.strip()

        if not nombre or not apellido or not email:
            return ("ERROR AL MODIFICAR DATOS", "INGRESE TODOS LOS CAMPOS")
        try:
            if contrasena_nueva:
                cursor.execute("SELECT contrasena FROM usuarios WHERE id_usuario = ?", (id_usuario,))
                guardado = cursor.fetchone()
                if guardado is None or not verificar_contrasena(contrasena_actual, guardado[0]):
                    return ("ERROR AL MODIFICAR DATOS", "LA CONTRASEÑA ACTUAL ES INCORRECTA")
                cursor.execute(
                    "UPDATE usuarios SET nombre = ?, apellido = ?, email = ?, contrasena = ? WHERE id_usuario = ?",
                    (nombre, apellido, email, hashear_contrasena(contrasena_nueva), id_usuario),
                )
            else:
                cursor.execute(
                    "UPDATE usuarios SET nombre = ?, apellido = ?, email = ? WHERE id_usuario = ?",
                    (nombre, apellido, email, id_usuario),
                )
            conexion.commit()
            logging.info(f"Se modificaron los datos del usuario {id_usuario}")
            return None
        except Exception as e:
            conexion.rollback()
            logging.error(f"Error al modificar datos: {e}")
            return ("ERROR AL MODIFICAR DATOS", "EL CORREO YA ESTÁ EN USO O HUBO UN ERROR EN LA BASE DE DATOS")

    @staticmethod
    def listar_compras(id_usuario):
        cursor.execute(
            """
            SELECT id_compra, metodo_pago, tipo_envio, total, fecha
            FROM compras WHERE id_usuario = ? ORDER BY id_compra DESC
            """,
            (id_usuario,),
        )
        compras = [
            {"id": f[0], "metodo_pago": f[1], "tipo_envio": f[2], "total": f[3], "fecha": f[4], "articulos": []}
            for f in cursor.fetchall()
        ]
        for compra in compras:
            cursor.execute(
                """
                SELECT categoria, marca, nombre, talle, color, cantidad, precio
                FROM articulos_comprados WHERE id_compra = ?
                """,
                (compra["id"],),
            )
            compra["articulos"] = [
                {"categoria": a[0], "marca": a[1], "nombre": a[2], "talle": a[3],
                 "color": a[4], "cantidad": a[5], "precio": a[6]}
                for a in cursor.fetchall()
            ]
        return compras

    @staticmethod
    def listar_usuarios():
        cursor.execute("SELECT id_usuario, nombre, apellido, email, rol FROM usuarios ORDER BY id_usuario")
        return [
            {"id": f[0], "nombre": f[1], "apellido": f[2], "email": f[3], "rol": f[4]}
            for f in cursor.fetchall()
        ]

        
    def __init__(self,id, nombre,apellido, email, contraseña,rol,alerta):
        self.nombre=nombre
        self.contraseña=contraseña
        self.email = email
        self.id= id
        self.apellido=apellido
        self.rol=rol
        self.alerta=alerta

class Admin(Usuario):
    pass

class Cliente(Usuario):
    pass

class Carrito:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario

    def listar_carrito(self):
        cursor.execute(
            """
            SELECT * FROM productos_carrito WHERE id_usuario = ?
        """, (self.id_usuario,)
        )
        return cursor.fetchall()

    def agregar_carrito(self, datos):
            cursor.execute(
                """
                SELECT cantidad FROM productos_carrito 
                WHERE id_usuario = ? AND id_producto = ? AND color = ? AND talle = ?
            """,
                (
                    self.id_usuario,
                    datos["id"],
                    datos["color"],
                    datos["talle"][0],
                ),
            )
            producto_existente = cursor.fetchone() 

            if producto_existente:
                cantidad_actual_en_carrito = producto_existente[0]

                if (cantidad_actual_en_carrito + datos["cantidad"]) > datos["talle"][1]:
                    return ("ERROR DEL CARRITO", "LLEGÓ AL LIMITE DE STOCK")
                else:
                    cursor.execute(
                        """
                        UPDATE productos_carrito 
                        SET cantidad = cantidad + ? 
                        WHERE id_usuario = ? AND id_producto = ? AND color = ? AND talle = ?
                    """,
                        (
                            datos["cantidad"],
                            self.id_usuario,
                            datos["id"],
                            datos["color"],
                            datos["talle"][0],
                        ),
                    )
                    conexion.commit()
                    return None
            else:
                cursor.execute(
                    """
                    INSERT INTO productos_carrito (id_usuario, id_producto, color, talle, cantidad)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        self.id_usuario,
                        datos["id"],
                        datos["color"],
                        datos["talle"][0],
                        datos["cantidad"],
                    ),
                )
                conexion.commit()
                return None

    def eliminar_carrito(self, id):
        cursor.execute("DELETE FROM productos_carrito WHERE id_item = ?", (id,))
        conexion.commit()

    def comprar_carrito(self, datos):
        lista = self.listar_carrito()
        if not lista:
            return None

        inventario = Inventario()

        try:
            cursor.execute(
                "INSERT INTO compras (id_usuario, metodo_pago, tipo_envio, total, fecha) VALUES (?, ?, ?, ?, ?)",
                (self.id_usuario, datos["metodo_pago"], datos["tipo_envio"], datos["total"], datos["fecha"]),
            )
            id_compra = cursor.lastrowid

            filas = []
            for i in lista:
                info = inventario.consultar_producto_especifico(i[2])
                cantidad = int(i[5])

                filas.append((
                    id_compra,
                    info["categoria"],
                    info["marca"],
                    info["nombre"],
                    i[4],           
                    i[3],           
                    cantidad,
                    float(info["precio"]),
                ))

                cursor.execute(
                    """
                    UPDATE stock_variantes
                    SET cantidad_stock = cantidad_stock - ?
                    WHERE id_producto = ?
                      AND id_talle_producto = (SELECT id_talle_producto FROM talles WHERE nombre_talle = ?)
                      AND id_color_producto = (SELECT id_color_producto FROM colores WHERE nombre_color = ?)
                      AND cantidad_stock >= ?
                    """,
                    (cantidad, i[2], i[4], i[3], cantidad),
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"Sin stock suficiente de {info['nombre']} ({i[3]}, talle {i[4]})"
                    )

            cursor.executemany(
                """INSERT INTO articulos_comprados
                   (id_compra, categoria, marca, nombre, talle, color, cantidad, precio)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                filas,
            )

            cursor.execute("DELETE FROM productos_carrito WHERE id_usuario = ?", (self.id_usuario,))

            self._quitar_de_otros_carritos(lista, inventario)

            conexion.commit()
            return id_compra
        except Exception:
            conexion.rollback()
            raise

    def _quitar_de_otros_carritos(self, lista, inventario):
        for i in lista:
            id_producto, color, talle = i[2], i[3], i[4]

            cursor.execute(
                """
                SELECT cantidad_stock FROM stock_variantes
                WHERE id_producto = ?
                  AND id_talle_producto = (SELECT id_talle_producto FROM talles WHERE nombre_talle = ?)
                  AND id_color_producto = (SELECT id_color_producto FROM colores WHERE nombre_color = ?)
                """,
                (id_producto, talle, color),
            )
            fila = cursor.fetchone()
            restante = fila[0] if fila else 0

            cursor.execute(
                """
                SELECT id_item, id_usuario FROM productos_carrito
                WHERE id_producto = ? AND color = ? AND talle = ?
                  AND id_usuario != ? AND cantidad > ?
                """,
                (id_producto, color, talle, self.id_usuario, restante),
            )
            afectados = cursor.fetchall()
            if not afectados:
                continue

            nombre = inventario.consultar_producto_especifico(id_producto)["nombre"]
            mensaje = (
                f"Se quitó de tu carrito \"{nombre}\" (color {color}, talle {talle}) "
                f"porque otra persona compró las últimas unidades."
            )

            for id_item, id_usuario in afectados:
                cursor.execute("DELETE FROM productos_carrito WHERE id_item = ?", (id_item,))
                Usuario.agregar_alerta(id_usuario, mensaje, confirmar=False)


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
    def listar_productos(producto):
        consulta = """
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
        parametros = ()

        if producto is None:
            logging.info("Se van a mostrar todos los productos")
        else:
            logging.info(f"Se van a mostrar los productos con categoria {producto}")
            consulta += """
            WHERE p.id_categoria_producto =
                (SELECT id_categoria_producto FROM categorias
                    WHERE nombre_categoria = ?)
            """
            parametros = (producto,)

        cursor.execute(consulta, parametros)
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
    def listar_stock(id_producto, solo_disponibles=True):
        logging.info(f"Se va a mostrar el stock del producto {id_producto}")

        condicion = "AND s.cantidad_stock > 0" if solo_disponibles else ""

        cursor.execute(
            f"""
            SELECT
                (SELECT nombre_talle FROM talles
                    WHERE id_talle_producto = s.id_talle_producto),
                (SELECT nombre_color FROM colores
                    WHERE id_color_producto = s.id_color_producto),
                s.cantidad_stock,
                (SELECT codigo_hex FROM colores
                    WHERE id_color_producto = s.id_color_producto)
            FROM stock_variantes s
            WHERE s.id_producto = ? {condicion}
            """,
            (id_producto,),
        )
        lista = cursor.fetchall()

        lista_diccionario = []
        for p in lista:
            diccionario = {"color": p[1], "talle": p[0], "cantidad": p[2], "hex": p[3]}
            lista_diccionario.append(diccionario)

        return {"diccionario": lista_diccionario}

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
    def agregar_color(nombre, codigo_hex):
        if not nombre or not nombre.strip():
            return ("ERROR AL AGREGAR COLOR", "EL COLOR DEBE TENER UN NOMBRE")
        codigo = codigo_hex
        if codigo is None:
            return ("ERROR AL AGREGAR COLOR", "SELECCIONE UN COLOR VALIDO")
        try:
            cursor.execute(
                "INSERT INTO colores (nombre_color, codigo_hex) VALUES (?, ?)",
                (nombre.strip(), codigo),
            )
            conexion.commit()
            logging.info(f"Se insertó el color {nombre} ({codigo})")
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
    @staticmethod
    def listar_colores():
        cursor.execute("SELECT nombre_color FROM colores ORDER BY id_color_producto")
        return [fila[0] for fila in cursor.fetchall()]

    @staticmethod
    def listar_talles():
        cursor.execute("SELECT nombre_talle FROM talles ORDER BY id_talle_producto")
        return [fila[0] for fila in cursor.fetchall()]