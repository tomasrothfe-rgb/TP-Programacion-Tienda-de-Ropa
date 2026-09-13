import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, agregar_producto, mostrar_productos

logging.basicConfig(level=logging.INFO)

creacion_bd()

def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    def mostrar():
        productos=mostrar_productos()
        lista_derecha.content.controls.clear()
        for producto in productos:
               lista_derecha.content.controls.append(
                      ft.Text(f"Nombre: {producto[1]}       Precio: {producto[2]}       Stock: {producto[3]}")
                    )
        page.update()

    def agregar():
        agregar_producto(nombre_producto.value, precio.value, stock.value)
        mostrar()
            
    def modificar():
            logging.info("Se desea modificar productos")
    def eliminar():
            logging.info("Se desea elimnar productos")
    
    def agregar_stock():
            logging.info("Se desea agregar stock")
    
    def estadisticas():
            logging.info("Se desea ver estadisticas")
    
    def historial():
            logging.info("Se desea ver historial")

    nombre_producto=ft.TextField()
    precio=ft.TextField()
    stock=ft.TextField()

    lista_derecha= ft.Container(
           content=ft.ListView(expand=1, spacing=10, padding=20,),
           bgcolor= ft.Colors.GREY,
           expand=True
    )

    mostrar()

    contenedor_izquierdo=ft.Container(
        content=ft.Column(
               controls=[
                      ft.Text("Panel de Administrador", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.ElevatedButton(
                    "Agregar productos",
                    on_click=agregar , 
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
               ]
        )
    )

    page.add(
        ft.Row(
            controls=[
                   contenedor_izquierdo,
                   lista_derecha
                      ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
    )


ft.app(target=main)