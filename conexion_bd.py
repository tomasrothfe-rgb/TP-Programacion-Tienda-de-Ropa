import sqlite3 as sql
import logging 
logging.basicConfig(level=logging.INFO)

conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()

# Conexion con la bd y creacion de tablas
def creacion_bd():
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    nombre TEXT UNIQUE NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL, 
    rol TEXT NOT NULL)'''
    )

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

def ingresar_manual():
    email = input("email ")
    nombre = input("nombre ")
    contra = input("contra ")
    rol = input("rol ")

    cursor.execute("INSERT INTO usuarios VALUES (?,?,?,?)", (nombre, email, contra, rol))
    conexion.commit()

