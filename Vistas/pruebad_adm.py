import flet as ft
import logging 
import os
import sys
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario,Cliente,Carrito  

carrito = Carrito(1)

carrito.listar_carrito()
carrito.mostrar_lista_actual()
carrito.guardar_bd()