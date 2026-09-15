import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, agregar_producto, mostrar_productos

logging.basicConfig(level=logging.INFO)




def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500


    def dialogo_box(lista_entrys,boolean,texto_superior,funcion):
        lista_nueva_entrys=[]
        def entrys(texto):
            return ft.TextField(
                      width=800,
                      hint_text=texto,
                      disabled=boolean
        )
        for i in lista_entrys:
            lista_nueva_entrys.append(entrys(i))

        def confirmar_click(e):
            valores = [entry.value for entry in lista_nueva_entrys]
            funcion(valores)
            page.pop_dialog()

        return page.show_dialog(
                        ft.AlertDialog(
                        modal=True,
                        title=ft.Text(texto_superior),
                        content=ft.Column(
                              controls=lista_nueva_entrys
                        ),
                        actions=[
                            ft.Button("CONFIRMAR", on_click=confirmar_click),
                            ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: logging.info("Se cerro la pestaña")))
    
    def agregar():
        dialogo_box(("Nombre", "Precio", "Stock"),False,"AGREGAR PRODUCTO", lambda valores: (agregar_producto(*valores)))

    contenedor_izquierdo=ft.Container(
        content=ft.Column(
               controls=[
                     
                ft.ElevatedButton(
                    "Agregar productos",
                    on_click=agregar , 
                )
               ]
        )
    )

    page.add(
        ft.Row(
            controls=[
                   contenedor_izquierdo
                      ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
    )


ft.app(target=main)