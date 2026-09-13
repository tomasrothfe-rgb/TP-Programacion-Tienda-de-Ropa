import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, agregar_producto, mostrar_productos

productos= mostrar_productos()
print(productos)
for producto in productos:
    print (producto)