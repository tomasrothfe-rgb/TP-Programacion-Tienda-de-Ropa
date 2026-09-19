import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, mostrar_productos

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    lista_productos=[]
    carrito_letras=0

    def eliminar_del_carrito(p):
        nonlocal lista_productos
        nonlocal carrito_letras
        lista_productos.remove(p)
        carrito_letras-=1
        carrito.value=str(carrito_letras)
        mostrar_carrito()

    def agregar_al_carrito(p):
        nonlocal lista_productos
        nonlocal carrito_letras
        if p in lista_productos:
            print("sumar")
        else:
            lista_productos.append(p)
        carrito_letras+=1
        carrito.value=str(carrito_letras)
        page.update()

    def mostrar_pantalla_productos():
        productos=mostrar_productos()
        lista_derecha.content.controls.clear()
        for producto in productos:
               lista_derecha.content.controls.append(
                      ft.ListTile(title=producto[1], subtitle=(f"Precio: {producto[2]}       Stock: {producto[3]}"),trailing=ft.IconButton(
        icon=ft.Icons.PLUS_ONE,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e, p=producto: agregar_al_carrito(p))
    ))
                      
        page.update()

    def mostrar_carrito():
        nonlocal lista_productos
        productos=lista_productos
        lista_derecha.content.controls.clear()
        for producto in productos:
               lista_derecha.content.controls.append(
                      ft.ListTile(title=producto[1], subtitle=(f"Precio: {producto[2]}       Stock: {producto[3]}"),trailing=ft.IconButton(
        icon=ft.Icons.EXPOSURE_MINUS_1,
        icon_color=ft.Colors.BLACK,
        on_click=lambda e, p=producto: eliminar_del_carrito(p)))
    )
                      
        page.update()

    
    carrito=ft.Text(str(carrito_letras))
    
    lista_derecha= ft.Container(
           content=ft.ListView(expand=1, spacing=10, padding=20,),
           bgcolor= ft.Colors.GREY,
           expand=True
    )

    contenedor_principal=ft.Container(
        content=ft.Column(
               controls=[
                      ft.Text("Panel de Cliente", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.Button(
                    "Ver carrito de compras",
                    on_click=lambda e:mostrar_carrito(), 
                ),
                ft.Button(
                    "Ver tienda",
                    on_click=lambda e:mostrar_pantalla_productos(), 
                ),
                ft.Button(
                    "Comprar",
                    on_click=lambda e:print("Comprar"),
                ),
                ft.Button(
                    "Modificar Datos personales",
                    on_click=lambda e:print("Datos"),
                    ),
                ft.Button(
                    "Historial de compra",
                    on_click=lambda e:print("Historial"),
                )
               ]
        )
    )

    mostrar_pantalla_productos()
    
    page.add(
        ft.Row(
            controls=[
                contenedor_principal,
                lista_derecha,
                ft.Row(
                    controls=[
                    carrito,
                    ft.Icon(ft.Icons.SHOPPING_BAG)
                ]
    ),
                      ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
    )


ft.app(target=main)