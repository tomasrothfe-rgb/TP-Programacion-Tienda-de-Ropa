import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario  

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    inventario = Inventario()
    producto_en_seleccion = None

    def ventana_de_alerta(texto_superior, erratas):

        def diseño_entradas(erratas):
                    return ft.Text(
                        erratas,
                    )

        return page.show_dialog(
                    ft.AlertDialog(
                            modal=True,
                            title=ft.Text(texto_superior),
                            content=ft.Column(
                                diseño_entradas(erratas)
                            ),
                            actions=[
                                    ft.Button("CONFIRMAR",on_click=lambda e: page.pop_dialog()),
                                    ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                                ],
                            actions_alignment=ft.MainAxisAlignment.END,))

    def ventana_de_dialogo(entradas,texto_superior,funcion):
        entradas_ventana=[]

        def confirmar_entradas():
            entradas= [diseño_entradas.value for diseño_entradas in entradas_ventana]
            retorno_funcion=funcion(*entradas)
            if retorno_funcion is None:
                 page.pop_dialog()
            else:
                 ventana_de_alerta(*retorno_funcion)

        def diseño_entradas(variable):
            return ft.TextField(
                hint_text=variable
            )

        for entrada in entradas:
            entradas_ventana.append(diseño_entradas(entrada))

        
        return page.show_dialog(
            ft.AlertDialog(
                    modal=True,
                    title=ft.Text(texto_superior),
                    content=ft.Column(
                        entradas_ventana
                    ),
                    actions=[
                            ft.Button("CONFIRMAR",on_click=lambda e: confirmar_entradas()),
                            ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                        ],
                    actions_alignment=ft.MainAxisAlignment.END,))


    def agregar():
        logging.info("Se desea agregar un producto")
        ventana_de_dialogo(("Nombre","Precio","Stock"),"AGREGAR PRODUCTO", inventario.agregar_producto)


    lista_derecha = ft.Container(
        content=ft.ListView(expand=1, spacing=10, padding=20),
        bgcolor=ft.Colors.GREY,
        expand=True
    )

    contenedor_izquierdo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Panel de Administrador", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.Button("Agregar productos", on_click=agregar),
                #ft.Button("Eliminar productos", on_click=eliminar),
                #ft.Button("Mostrar productos", on_click=mostrar),
                #ft.Button("Modificar productos", on_click=modificar),
                #ft.Button("Agregar stock", on_click=agregar_stock),
                #ft.Button("Consultar estadisticas", on_click=estadisticas),
                #ft.Button("Ver historial de compras productos", on_click=historial),
            ]
        )
    )

    page.add(
        ft.Row(
            controls=[contenedor_izquierdo, lista_derecha],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )


ft.app(target=main)