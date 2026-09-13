import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, agregar_producto

logging.basicConfig(level=logging.INFO)

creacion_bd()

def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    nombre_producto=ft.TextField()
    precio=ft.TextField()
    stock=ft.TextField()

    def agregar():
        logging.info("Se desea agregar productos")
        agregar_producto(nombre_producto.value, precio.value, stock.value)

    def modificar():
        logging.info("Se desea modificar productos")

    def mostrar():
        logging.info("Se desea mostar productos")

    def eliminar():
        logging.info("Se desea elimnar productos")

    def agregar_stock():
        logging.info("Se desea agregar stock")

    def estadisticas():
        logging.info("Se desea ver estadisticas")

    def historial():
        logging.info("Se desea ver historial")


    page.add(
        ft.Text("Panel de Administrador", size=30, weight="bold", color=ft.Colors.BLUE),
        ft.ElevatedButton(
            "Agregar productos",
            on_click=agregar,
        ),
        nombre_producto,
        precio,
        stock,
        ft.ElevatedButton(
            "Eliminar productos",
            on_click=eliminar,
        ),
        ft.ElevatedButton(
            "Mostrar productos",
                on_click= mostrar,
            ),
        ft.ElevatedButton(
            "Modificar productos",
            on_click=modificar,
        ),
        ft.ElevatedButton(
            "Agregar stock",
                on_click=agregar_stock,
            ),
        ft.ElevatedButton(
            "Consultar estadisticas",
            on_click=estadisticas,
        ),
        ft.ElevatedButton(
            "Ver historial de compras productos",
                on_click=historial,
            ),
    )


ft.app(target=main)